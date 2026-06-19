"""退款执行节点。调用 Shopify API（或 Mock）执行退款。"""
from api_adapters.shopify import create_shopify_adapter


class RefundResult:
    def __init__(self):
        self.success: bool = False
        self.error: str = ""


def execute_refund(order_id: str, amount: float, reason: str) -> RefundResult:
    result = RefundResult()
    if amount <= 0:
        result.error = "Invalid refund amount"
        return result
    try:
        shopify = create_shopify_adapter()
        ok = shopify.process_refund(order_id, amount, reason)
        result.success = ok
        if not ok:
            result.error = "Refund API returned failure"
    except Exception as e:
        result.success = False
        result.error = str(e)
    return result
