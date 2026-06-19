"""物流追踪数据模型"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TrackingEvent(BaseModel):
    location: str = ""
    description: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


class TrackingInfo(BaseModel):
    """物流查询结果"""
    tracking_number: str
    carrier: str = ""
    valid: bool = True
    status: str = "unknown"          # in_transit | delivered | stuck | expired
    last_update: Optional[datetime] = None
    estimated_delivery: Optional[datetime] = None
    days_since_last_update: int = 0
    events: list[TrackingEvent] = []
    raw_data: dict = {}
