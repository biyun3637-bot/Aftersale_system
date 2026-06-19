"""订单、退款、工单数据模型"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from .intent import IntentResult


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class DeliveryStatus(str, Enum):
    NOT_SHIPPED = "not_shipped"
    IN_TRANSIT = "in_transit"
    STUCK = "stuck"
    DELIVERED = "delivered"
    UNKNOWN = "unknown"


class RefundType(str, Enum):
    FULL = "full"
    PARTIAL = "partial"


class RefundStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"
    REJECTED = "rejected"


class TicketStatus(str, Enum):
    OPEN = "open"
    AUTO_PROCESSED = "auto_processed"
    PENDING_REVIEW = "pending_review"
    RESOLVED = "resolved"


class OrderItem(BaseModel):
    sku: str
    name: str
    quantity: int
    price: float


class Order(BaseModel):
    """模拟订单数据"""
    id: str
    customer_email: str
    customer_name: str
    amount: float
    currency: str = "USD"
    status: OrderStatus
    delivery_status: DeliveryStatus
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    shipping_address: str = ""
    items: list[OrderItem] = []
    created_at: datetime = Field(default_factory=datetime.now)
    platform: str = "shopify"  # shopify | amazon


class RefundAction(BaseModel):
    """退款动作记录"""
    order_id: str
    refund_type: RefundType
    amount: float
    currency: str = "USD"
    reason: str = ""
    status: RefundStatus = RefundStatus.PENDING
    executed_at: Optional[datetime] = None
    approved_by: str = "auto"  # auto | human_{id}


class Ticket(BaseModel):
    """售后工单（全链路记录）"""
    id: str
    order_id: str
    customer_message: str
    intent: IntentResult
    status: TicketStatus = TicketStatus.OPEN
    refund_action: Optional[RefundAction] = None
    response: str = ""
    rpa_screenshot: Optional[str] = None
    sla_seconds: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    notes: str = ""

    def to_summary(self) -> dict:
        return {
            "ticket_id": self.id,
            "order_id": self.order_id,
            "intent": self.intent.intent.value if self.intent.intent else None,
            "subtype": self.intent.subtype,
            "risk": self.intent.risk.value if self.intent.risk else None,
            "status": self.status.value if self.status else None,
            "refund_amount": self.refund_action.amount if self.refund_action else None,
            "response_preview": self.response[:100] if self.response else "",
        }
