from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, Field


class ScheduleEventModel(BaseModel):
    date: str  # Format: "09/09/2025"
    slots: int
    event_type: str = Field(alias="type")
    schedules: Dict[str, int]  # {"09h00": 1, "09h15": 2, ...}

    model_config = ConfigDict(populate_by_name=True)


class ScheduleSnapshotModel(BaseModel):
    url: str
    time: Optional[datetime] = None  # Crawl timestamp
    events: List[ScheduleEventModel]

    model_config = ConfigDict(populate_by_name=True)
