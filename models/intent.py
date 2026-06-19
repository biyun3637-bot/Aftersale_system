"""
意图分类数据结构。

3 大类 × 3 子类 分类体系：

refund_request (退款请求)
  - not_received      未收到货
  - not_satisfied     产品不满意
  - duplicate_charge  重复扣款

order_issue (订单异常)
  - not_shipped       未发货
  - tracking_stuck    物流卡住
  - no_update         无物流更新

after_sales (售后问题)
  - damaged           损坏
  - wrong_item        错发货
  - quality_issue     质量问题
"""
from enum import Enum
from pydantic import BaseModel, Field


class IntentType(str, Enum):
    REFUND = "refund_request"
    ORDER_ISSUE = "order_issue"
    AFTER_SALES = "after_sales"


class RefundSubtype(str, Enum):
    NOT_RECEIVED = "not_received"
    NOT_SATISFIED = "not_satisfied"
    DUPLICATE_CHARGE = "duplicate_charge"


class OrderIssueSubtype(str, Enum):
    NOT_SHIPPED = "not_shipped"
    TRACKING_STUCK = "tracking_stuck"
    NO_UPDATE = "no_update"


class AfterSalesSubtype(str, Enum):
    DAMAGED = "damaged"
    WRONG_ITEM = "wrong_item"
    QUALITY_ISSUE = "quality_issue"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IntentResult(BaseModel):
    """意图分类结果"""
    intent: IntentType
    subtype: str
    risk: RiskLevel
    confidence: float = Field(ge=0.0, le=1.0)
    customer_message: str = ""
    summary: str = ""
