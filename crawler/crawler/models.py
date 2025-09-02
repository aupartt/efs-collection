from datetime import datetime
from typing import Literal

from bs4 import NavigableString, PageElement, Tag
from pydantic import BaseModel

Schedules = dict[str, int]
Locator = PageElement | Tag | NavigableString

CollectType = Literal["plasma", "blood", "platelets"]


class Event(BaseModel):
    date: str
    slots: int
    schedules: Schedules


class LocationEvents(BaseModel):
    url: str
    location: str
    collect_type: CollectType
    time: datetime
    events: list[Event]


class Result[T](BaseModel):
    success: bool
    value: T | None = None
    error: str | None = None
