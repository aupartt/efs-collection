from pydantic import BaseModel
from typing import Dict

Schedules = Dict[str, int]


class Event(BaseModel):
    date: str
    slots: int
    schedules: Schedules


class EventCollection(BaseModel):
    url: str
    events: list[Event]
