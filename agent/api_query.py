"""API 查询节点。

优先查 Shopify API + 17Track 物流。
查不到 → api_available=False，触发 RPA 兜底。
"""
from typing import Optional
from api_adapters.shopify import create_shopify_adapter
from api_adapters.track17 import create_track17_adapter
from models.order import Order
from models.tracking import TrackingInfo


class QueryResult:
    def __init__(self):
        self.order: Optional[Order] = None
        self.tracking: Optional[TrackingInfo] = None
        self.api_available: bool = False
        self.error: str = ""


def query_order(order_id: str) -> QueryResult:
    result = QueryResult()
    if not order_id:
        result.error = "No order_id provided"
        return result

    shopify = create_shopify_adapter()
    order = shopify.get_order(order_id)
    if order is None:
        result.error = f"Order {order_id} not found via API"
        return result

    result.order = order

    if order.tracking_number:
        track17 = create_track17_adapter()
        tracking = track17.track(order.tracking_number, order.carrier or "")
        if tracking is not None:
            result.tracking = tracking
            result.api_available = True
        else:
            result.error = f"Tracking {order.tracking_number} not found"
    else:
        result.api_available = True

    return result
