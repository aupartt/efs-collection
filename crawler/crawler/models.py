import datetime
from pydantic import BaseModel
from typing import Dict, Literal

Schedules = Dict[str, int]

EventType = Literal["plasma", "blood", "platelets"]


class Event(BaseModel):
    date: str
    slots: int
    type: EventType
    schedules: Schedules


class LocationEvents(BaseModel):
    url: str
    time: datetime
    events: list[Event]
