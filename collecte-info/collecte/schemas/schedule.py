from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, Field


class ScheduleEventSchema(BaseModel):
    """Pydantic: Time series data for schedule availability tracking"""
    date: str  # Format: "09/09/2025"
    event_type: str = Field(alias="type")
    slots: int
    schedules: Dict[str, int]  # {"09h00": 1, "09h15": 2, ...}

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class ScheduleSnapshotSchema(BaseModel):
    """Pydantic: Individual events within a schedule snapshot"""
    url: str
    crawled_at: Optional[datetime] = None  # Crawl timestamp
    events: List[ScheduleEventSchema]

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
