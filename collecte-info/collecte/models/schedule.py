from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class ScheduleEventModel(BaseModel):
    date: str  # Format: "09/09/2025"
    slots: int
    event_type: str = Field(alias="type")
    schedules: Dict[str, int]  # {"09h00": 1, "09h15": 2, ...}

    class Config:
        allow_population_by_field_name = True


class ScheduleSnapshotModel(BaseModel):
    url: str
    time: Optional[datetime] = None  # Crawl timestamp
    events: List[ScheduleEventModel]

    class Config:
        allow_population_by_field_name = True
