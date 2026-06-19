"""17Track API 适配器。DEMO_MODE=true 时返回 Mock 数据。"""
from typing import Optional
import config
from api_adapters.base import Track17Adapter
from api_adapters.mock_data import MOCK_TRACKING
from models.tracking import TrackingInfo


class MockTrack17Adapter(Track17Adapter):
    """模拟 17Track 适配器（用于 Demo）"""

    def track(self, tracking_number: str, carrier: str = "") -> Optional[TrackingInfo]:
        return MOCK_TRACKING.get(tracking_number)


class RealTrack17Adapter(Track17Adapter):
    """真实 17Track API 适配器（预留）"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def track(self, tracking_number: str, carrier: str = "") -> Optional[TrackingInfo]:
        # TODO: 调用 17Track.io API
        # resp = httpx.post(
        #     "https://api.17track.net/track/v2.2/gettrackinfo",
        #     headers={"17token": self.api_key},
        #     json=[{"number": tracking_number, "carrier": carrier}],
        # )
        raise NotImplementedError("Real 17Track adapter — implement when going live")


def create_track17_adapter() -> Track17Adapter:
    if config.DEMO_MODE:
        return MockTrack17Adapter()
    return RealTrack17Adapter(api_key="")
