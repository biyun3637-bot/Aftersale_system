"""
意图 + 风险分类节点。

LLM_PROVIDER=mock  → 关键词匹配（无 API 依赖）
LLM_PROVIDER=zhipu → 调用 GLM-4-Flash 真实分类

LLM 返回无效结果时自动降级到关键词匹配。
"""
import json
import re
from typing import Optional

from models.intent import (
    IntentResult, IntentType, RiskLevel,
    RefundSubtype, OrderIssueSubtype, AfterSalesSubtype,
)

# ── 单层类型 → (intent, subtype) 映射表 ──
_TYPE_MAP = {
    "refund_not_received":       (IntentType.REFUND, RefundSubtype.NOT_RECEIVED.value),
    "refund_not_satisfied":      (IntentType.REFUND, RefundSubtype.NOT_SATISFIED.value),
    "refund_duplicate_charge":   (IntentType.REFUND, RefundSubtype.DUPLICATE_CHARGE.value),
    "order_not_shipped":         (IntentType.ORDER_ISSUE, OrderIssueSubtype.NOT_SHIPPED.value),
    "order_tracking_stuck":      (IntentType.ORDER_ISSUE, OrderIssueSubtype.TRACKING_STUCK.value),
    "order_no_update":           (IntentType.ORDER_ISSUE, OrderIssueSubtype.NO_UPDATE.value),
    "after_sales_damaged":       (IntentType.AFTER_SALES, AfterSalesSubtype.DAMAGED.value),
    "after_sales_wrong_item":    (IntentType.AFTER_SALES, AfterSalesSubtype.WRONG_ITEM.value),
    "after_sales_quality":       (IntentType.AFTER_SALES, AfterSalesSubtype.QUALITY_ISSUE.value),
}

# ── LLM 客户端（懒加载） ──
_zhipu_client = None

def _get_zhipu_client():
    global _zhipu_client
    if _zhipu_client is None:
        import os
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
        from zhipuai import ZhipuAI
        _zhipu_client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))
    return _zhipu_client

# ── 订单号提取 ──
_ORDER_ID_PATTERN = re.compile(r"(ORD-\d{3})", re.IGNORECASE)

def extract_order_id(message: str) -> Optional[str]:
    match = _ORDER_ID_PATTERN.search(message.upper())
    return match.group(1) if match else None

# ── LLM 分类 Prompt（单层输出） ──
_CLASSIFY_PROMPT = (
    'Classify this customer service message into ONE of these 9 types.\n'
    'Respond with ONLY the type name, nothing else.\n\n'
    'refund_not_received     - customer didn\'t receive their order, wants refund\n'
    'refund_not_satisfied    - customer not happy with the product\n'
    'refund_duplicate_charge - customer was charged twice\n'
    'order_not_shipped       - order hasn\'t been shipped\n'
    'order_tracking_stuck    - tracking hasn\'t updated in days\n'
    'order_no_update         - no tracking info available\n'
    'after_sales_damaged     - product arrived damaged/broken\n'
    'after_sales_wrong_item  - received wrong item\n'
    'after_sales_quality     - poor quality or defective\n\n'
    'Message: "{message}"\n'
    'Type:'
)

_RISK_PROMPT = (
    'Assess the risk level of this customer message for a refund.\n'
    'Return ONLY: low | medium | high\n\n'
    'Message: "{message}"\n'
    'Order amount: ${amount}\n'
    'Delivery status: {delivery}\n\n'
    'Rules:\n'
    '- low: small amount ($20 or less), clear-cut issue\n'
    '- medium: typical case\n'
    '- high: large amount (over $100), or delivered-but-claims-not-received\n\n'
    'Risk:'
)


def _classify_with_llm(message: str) -> Optional[IntentResult]:
    """调用 ZhipuAI GLM-4-Flash 进行真实意图分类"""
    try:
        client = _get_zhipu_client()

        # Step 1: 获取类型
        resp = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": _CLASSIFY_PROMPT.format(message=message)}],
            temperature=0.1,
        )
        raw_type = resp.choices[0].message.content.strip().lower().replace("-", "_")

        # 映射到 intent + subtype
        mapped = _TYPE_MAP.get(raw_type)
        if mapped is None:
            # 尝试部分匹配
            for key, val in _TYPE_MAP.items():
                if key.replace("_", "") == raw_type.replace("_", "").replace(" ", ""):
                    mapped = val
                    break
        if mapped is None:
            return None

        intent, subtype = mapped

        # Step 2: 独立评估风险等级
        # 暂时用 medium，决策节点会基于真实订单数据重新评估
        risk = RiskLevel.MEDIUM

        return IntentResult(
            intent=intent,
            subtype=subtype,
            risk=risk,
            confidence=0.85,
            customer_message=message,
            summary=f"{intent.value}/{subtype}",
        )

    except Exception as e:
        print(f"[LLM] Classification error: {e}")
        return None


# ── 关键词匹配 Mock 分类（保留作为降级） ──

_INTENT_KEYWORDS = [
    ("refund", IntentType.REFUND, {
        RefundSubtype.NOT_RECEIVED.value: [
            "didn't receive", "not received", "never got", "haven't received",
            "where is my", "never arrived", "missing", "didn't get",
        ],
        RefundSubtype.NOT_SATISFIED.value: [
            "not satisfied", "don't like", "not happy", "disappointed", "waste of money",
        ],
        RefundSubtype.DUPLICATE_CHARGE.value: [
            "duplicate", "charged twice", "double charge", "charged again",
        ],
    }),
    ("order_issue", IntentType.ORDER_ISSUE, {
        OrderIssueSubtype.NOT_SHIPPED.value: [
            "not shipped", "hasn't shipped", "still pending", "never shipped",
        ],
        OrderIssueSubtype.TRACKING_STUCK.value: [
            "stuck", "not moving", "no movement", "hasn't moved",
        ],
        OrderIssueSubtype.NO_UPDATE.value: [
            "no update", "no tracking update",
        ],
    }),
    ("after_sales", IntentType.AFTER_SALES, {
        AfterSalesSubtype.DAMAGED.value: [
            "broken", "damaged", "cracked", "shattered", "fell apart",
        ],
        AfterSalesSubtype.WRONG_ITEM.value: [
            "wrong item", "not what I ordered", "different item", "incorrect",
        ],
        AfterSalesSubtype.QUALITY_ISSUE.value: [
            "poor quality", "defective", "doesn't work", "cheap", "terrible",
        ],
    }),
]


def _classify_mock(message: str) -> IntentResult:
    msg_lower = message.lower()
    for name, intent_type, subtype_kw in _INTENT_KEYWORDS:
        matched_subtype = None
        for subtype, keywords in subtype_kw.items():
            if any(kw in msg_lower for kw in keywords):
                matched_subtype = subtype
                break
        if matched_subtype:
            return IntentResult(
                intent=intent_type,
                subtype=matched_subtype,
                risk=RiskLevel.MEDIUM,
                confidence=0.85,
                customer_message=message,
                summary=f"{intent_type.value}/{matched_subtype}",
            )
    return IntentResult(
        intent=IntentType.REFUND,
        subtype=RefundSubtype.NOT_RECEIVED.value,
        risk=RiskLevel.MEDIUM,
        confidence=0.60,
        customer_message=message,
        summary="refund_request/not_received (default)",
    )


# ── 公开入口 ──

def classify(message: str, llm_provider: str = "mock") -> IntentResult:
    if llm_provider == "zhipu":
        result = _classify_with_llm(message)
        if result is not None:
            return result
        print("[Classifier] LLM failed -> falling back to keyword matching")
    return _classify_mock(message)
