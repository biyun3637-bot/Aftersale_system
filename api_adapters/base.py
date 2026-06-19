"""API 适配器抽象接口。所有外部平台适配器继承此接口。"""
from abc import ABC, abstractmethod
from typing import Optional

from models.order import Order
from models.tracking import TrackingInfo


class ShopifyAdapter(ABC):
    """Shopify API 适配器接口"""

    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Order]:
        ...

    @abstractmethod
    def process_refund(self, order_id: str, amount: float, reason: str) -> bool:
        ...


class Track17Adapter(ABC):
    """17Track 物流查询适配器接口"""

    @abstractmethod
    def track(self, tracking_number: str, carrier: str = "") -> Optional[TrackingInfo]:
        ...
