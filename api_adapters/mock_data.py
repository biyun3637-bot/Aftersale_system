"""模拟数据集。

7 个订单覆盖所有测试场景。
"""
from datetime import datetime, timedelta

from models.order import Order, OrderItem, OrderStatus, DeliveryStatus
from models.tracking import TrackingInfo, TrackingEvent
from models.intent import IntentType

_now = datetime.now()

# ═══════════════════════════════════════
# 模拟订单数据集
# ═══════════════════════════════════════

MOCK_ORDERS: dict[str, Order] = {

    # ── 场景 1: 自动全额退款 ──
    "ORD-001": Order(
        id="ORD-001",
        customer_email="alice@example.com",
        customer_name="Alice",
        amount=15.00,
        status=OrderStatus.SHIPPED,
        delivery_status=DeliveryStatus.UNKNOWN,
        tracking_number="TRACK001",
        carrier="USPS",
        items=[OrderItem(sku="SKU-A", name="Basic T-Shirt", quantity=1, price=15.00)],
        created_at=_now - timedelta(days=3),
    ),

    # ── 场景 2: 部分退款（物流卡住 12 天）─
    "ORD-002": Order(
        id="ORD-002",
        customer_email="bob@example.com",
        customer_name="Bob",
        amount=80.00,
        status=OrderStatus.SHIPPED,
        delivery_status=DeliveryStatus.STUCK,
        tracking_number="TRACK002",
        carrier="FedEx",
        items=[OrderItem(sku="SKU-B", name="Wireless Mouse", quantity=1, price=80.00)],
        created_at=_now - timedelta(days=20),
    ),

    # ── 场景 3: 人工审核（金额高 + 已送达却声称未收到）─
    "ORD-003": Order(
        id="ORD-003",
        customer_email="carol@example.com",
        customer_name="Carol",
        amount=150.00,
        status=OrderStatus.DELIVERED,
        delivery_status=DeliveryStatus.DELIVERED,
        tracking_number="TRACK003",
        carrier="UPS",
        items=[OrderItem(sku="SKU-C", name="Bluetooth Speaker", quantity=1, price=150.00)],
        created_at=_now - timedelta(days=15),
    ),

    # ── 场景 4: API 查不到 → RPA 兜底 ──
    "ORD-004": Order(
        id="ORD-004",
        customer_email="dave@example.com",
        customer_name="Dave",
        amount=18.00,
        status=OrderStatus.SHIPPED,
        delivery_status=DeliveryStatus.UNKNOWN,
        tracking_number="TRACK004",
        carrier="Unknown",
        items=[OrderItem(sku="SKU-D", name="Phone Case", quantity=1, price=25.00)],
        created_at=_now - timedelta(days=7),
    ),

    # ── 场景 5: 售后损坏 ──
    "ORD-005": Order(
        id="ORD-005",
        customer_email="eve@example.com",
        customer_name="Eve",
        amount=50.00,
        status=OrderStatus.DELIVERED,
        delivery_status=DeliveryStatus.DELIVERED,
        tracking_number="TRACK005",
        carrier="USPS",
        items=[OrderItem(sku="SKU-E", name="Ceramic Mug Set", quantity=1, price=50.00)],
        created_at=_now - timedelta(days=5),
    ),

    # ── 场景 6: 未发货 ──
    "ORD-006": Order(
        id="ORD-006",
        customer_email="frank@example.com",
        customer_name="Frank",
        amount=35.00,
        status=OrderStatus.PENDING,
        delivery_status=DeliveryStatus.NOT_SHIPPED,
        tracking_number=None,
        carrier=None,
        items=[OrderItem(sku="SKU-F", name="Stainless Water Bottle", quantity=1, price=35.00)],
        created_at=_now - timedelta(days=2),
    ),

    # ── 场景 7: 错发货 ──
    "ORD-007": Order(
        id="ORD-007",
        customer_email="grace@example.com",
        customer_name="Grace",
        amount=45.00,
        status=OrderStatus.DELIVERED,
        delivery_status=DeliveryStatus.DELIVERED,
        tracking_number="TRACK007",
        carrier="FedEx",
        items=[OrderItem(sku="SKU-G", name="Yoga Mat", quantity=1, price=45.00)],
        created_at=_now - timedelta(days=8),
    ),
}

# ═══════════════════════════════════════
# 模拟物流数据
# ═══════════════════════════════════════
MOCK_TRACKING: dict[str, TrackingInfo] = {
    "TRACK001": TrackingInfo(
        tracking_number="TRACK001",
        carrier="USPS",
        valid=False,
        status="unknown",
        last_update=None,
        days_since_last_update=0,
        events=[],
    ),
    "TRACK002": TrackingInfo(
        tracking_number="TRACK002",
        carrier="FedEx",
        valid=True,
        status="stuck",
        last_update=_now - timedelta(days=12),
        days_since_last_update=12,
        events=[
            TrackingEvent(location="Memphis, TN", description="Package in transit", timestamp=_now - timedelta(days=12)),
        ],
    ),
    "TRACK003": TrackingInfo(
        tracking_number="TRACK003",
        carrier="UPS",
        valid=True,
        status="delivered",
        last_update=_now - timedelta(days=3),
        days_since_last_update=3,
        events=[
            TrackingEvent(location="Los Angeles, CA", description="Delivered", timestamp=_now - timedelta(days=3)),
        ],
    ),
    # TRACK004 removed: triggers RPA fallback when not found
    "TRACK005": TrackingInfo(
        tracking_number="TRACK005",
        carrier="USPS",
        valid=True,
        status="delivered",
        last_update=_now - timedelta(days=2),
        days_since_last_update=2,
        events=[
            TrackingEvent(location="New York, NY", description="Delivered", timestamp=_now - timedelta(days=2)),
        ],
    ),
    "TRACK007": TrackingInfo(
        tracking_number="TRACK007",
        carrier="FedEx",
        valid=True,
        status="delivered",
        last_update=_now - timedelta(days=4),
        days_since_last_update=4,
        events=[
            TrackingEvent(location="Chicago, IL", description="Delivered", timestamp=_now - timedelta(days=4)),
        ],
    ),
}

# ═══════════════════════════════════════
# 场景与预期系统行为映射
# ═══════════════════════════════════════
DEMO_SCENARIOS = [
    {
        "name": "自动退款",
        "customer_message": "I didn't receive my order, want refund",
        "order_id": "ORD-001",
        "expect": "auto_full_refund",
        "description": "金额<$20 + 无物流信息 → 全额自动退款",
    },
    {
        "name": "部分退款",
        "customer_message": "My package has been stuck for weeks, I want a refund",
        "order_id": "ORD-002",
        "expect": "auto_partial_refund",
        "description": "物流卡住12天 → 部分退款50%",
    },
    {
        "name": "人工审核",
        "customer_message": "I didn't receive my order but it says delivered, I want my money back",
        "order_id": "ORD-003",
        "expect": "human_review",
        "description": "高金额$150 + 已送达争议 → 人工审核",
    },
    {
        "name": "RPA 兜底",
        "customer_message": "Where is my order? I haven't received anything",
        "order_id": "ORD-004",
        "expect": "auto_full_refund",
        "description": "API查不到物流 → RPA兜底 → 自动退款 (amount=$18)",
    },
    {
        "name": "售后损坏",
        "customer_message": "The mug arrived broken, I need a refund",
        "order_id": "ORD-005",
        "expect": "auto_partial_refund",
        "description": "物品损坏 → 部分退款",
    },
    {
        "name": "未发货",
        "customer_message": "I ordered 2 days ago and it still hasn't shipped",
        "order_id": "ORD-006",
        "expect": "auto_full_refund",
        "description": "未发货 → 全额自动退款",
    },
    {
        "name": "错发货",
        "customer_message": "I received a yoga mat but I ordered a water bottle",
        "order_id": "ORD-007",
        "expect": "human_review",
        "description": "错发货 → 人工审核（需要确认退货）",
    },
]
