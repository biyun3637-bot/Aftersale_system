"""退款决策引擎。

根据意图 + 订单状态 + 物流状态 + 金额，判断：
  全额自动退款 | 部分自动退款 | 人工审核 | 仅回复
"""
from math import ceil
from typing import Optional

import config
from models.intent import IntentResult, IntentType, RiskLevel
from models.order import Order, DeliveryStatus
from models.tracking import TrackingInfo


class Decision:
    def __init__(self):
        self.action: str = "no_action"
        self.amount: Optional[float] = None
        self.reason: str = ""
        self.risk: RiskLevel = RiskLevel.MEDIUM


def decide(intent: IntentResult, order: Optional[Order],
           tracking: Optional[TrackingInfo]) -> Decision:
    d = Decision()
    if order is None:
        d.action = "human_review"
        d.reason = "Order not found"
        d.risk = RiskLevel.HIGH
        return d

    amount = order.amount
    delivery = order.delivery_status
    risk = _reassess_risk(intent, order, tracking)
    d.risk = risk

    if risk == RiskLevel.HIGH:
        d.action = "human_review"
        d.reason = f"High risk ({intent.intent.value}/{intent.subtype})"
        return d

    # ── 低金额兜底：无论什么原因，$20 以下直接退 ──
    if amount <= config.AUTO_REFUND_MAX:
        d.action = "auto_full_refund"
        d.amount = amount
        d.reason = f"Low value ${amount} ≤ ${config.AUTO_REFUND_MAX} — auto refund"
        return d

    # ── Intent-specific rules ──
    if intent.intent == IntentType.REFUND:
        if intent.subtype == "not_received":
            if delivery == DeliveryStatus.STUCK and tracking:
                if tracking.days_since_last_update >= config.PARTIAL_REFUND_DAYS:
                    partial = ceil(amount * config.PARTIAL_REFUND_PERCENT * 100) / 100
                    d.action = "auto_partial_refund"
                    d.amount = partial
                    d.reason = f"Stuck {tracking.days_since_last_update}d, partial 50%"
                else:
                    d.action = "auto_full_refund"
                    d.amount = amount
                    d.reason = f"Delivery stuck, auto refund"
            else:
                d.action = "auto_full_refund"
                d.amount = amount
                d.reason = f"Not received, auto refund"
        elif intent.subtype == "duplicate_charge":
            d.action = "auto_full_refund"
            d.amount = amount
            d.reason = "Duplicate charge"
        else:
            d.action = "human_review"
            d.reason = f"Refund {intent.subtype} — manual review"

    elif intent.intent == IntentType.ORDER_ISSUE:
        if intent.subtype == "not_shipped":
            d.action = "auto_full_refund"
            d.amount = amount
            d.reason = "Not shipped"
        elif intent.subtype == "tracking_stuck":
            if tracking and tracking.days_since_last_update >= config.PARTIAL_REFUND_DAYS:
                partial = ceil(amount * config.PARTIAL_REFUND_PERCENT * 100) / 100
                d.action = "auto_partial_refund"
                d.amount = partial
                d.reason = f"Stuck {tracking.days_since_last_update}d"
            else:
                d.action = "auto_full_refund"
                d.amount = amount
                d.reason = "Tracking issue, auto refund"
        elif intent.subtype == "no_update":
            d.action = "auto_full_refund"
            d.amount = amount
            d.reason = "No tracking, auto refund"

    elif intent.intent == IntentType.AFTER_SALES:
        if intent.subtype == "damaged":
            partial = ceil(amount * config.PARTIAL_REFUND_PERCENT * 100) / 100
            d.action = "auto_partial_refund"
            d.amount = partial
            d.reason = "Item damaged"
        elif intent.subtype == "wrong_item":
            d.action = "human_review"
            d.reason = "Wrong item — arrange return"
        elif intent.subtype == "quality_issue":
            d.action = "human_review"
            d.reason = "Quality complaint"

    if d.action == "no_action":
        d.action = "human_review"
        d.reason = "No matching rule"
    return d


def _reassess_risk(intent, order, tracking):
    if order.amount >= config.HUMAN_REVIEW_MIN:
        return RiskLevel.HIGH
    if (intent.intent == IntentType.REFUND
            and intent.subtype == "not_received"
            and order.delivery_status == DeliveryStatus.DELIVERED):
        return RiskLevel.HIGH
    if order.amount <= config.AUTO_REFUND_MAX:
        return RiskLevel.LOW
    return RiskLevel.MEDIUM
