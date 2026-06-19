"""Shopify API 适配器。DEMO_MODE=true 时返回 Mock 数据。"""
from typing import Optional
import config
from api_adapters.base import ShopifyAdapter
from api_adapters.mock_data import MOCK_ORDERS
from models.order import Order


class MockShopifyAdapter(ShopifyAdapter):
    """模拟 Shopify 适配器（用于 Demo）"""

    def get_order(self, order_id: str) -> Optional[Order]:
        return MOCK_ORDERS.get(order_id)

    def process_refund(self, order_id: str, amount: float, reason: str) -> bool:
        # Demo 模式总是成功
        print(f"[MockShopify] Refund {order_id}: ${amount} — {reason}")
        return True


class RealShopifyAdapter(ShopifyAdapter):
    """真实 Shopify API 适配器（预留）"""

    def __init__(self, access_token: str, store_domain: str):
        self.token = access_token
        self.domain = store_domain

    def get_order(self, order_id: str) -> Optional[Order]:
        # TODO: 调用 Shopify Admin GraphQL API
        # headers = {"X-Shopify-Access-Token": self.token}
        # resp = httpx.get(f"https://{self.domain}/admin/api/2024-01/orders/{order_id}.json", headers=headers)
        raise NotImplementedError("Real Shopify adapter — implement when going live")

    def process_refund(self, order_id: str, amount: float, reason: str) -> bool:
        raise NotImplementedError("Real Shopify adapter — implement when going live")


def create_shopify_adapter() -> ShopifyAdapter:
    if config.DEMO_MODE:
        return MockShopifyAdapter()
    return RealShopifyAdapter(
        access_token="",  # 从环境变量读取
        store_domain="",
    )
