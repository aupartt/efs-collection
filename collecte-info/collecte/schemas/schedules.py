from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ScheduleSchema(BaseModel):
    """Pydantic: Informations relative to a schedule event"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    event_id: int
    efs_id: Optional[str] = None

    # Details
    date: datetime
    url: str
    time: str

    # Data
    total_slots: int
    type: str
    schedules: dict[str, int]


class ScheduleEventSchema(BaseModel):
    """Pydantic: Informations relative to a schedule event"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    date: datetime
    total_slots: int = Field(..., alias="slots")
    type: str = Field(..., alias="type")
    schedules: dict[str, time]


class ScheduleGroupSchema(BaseModel):
    """Pydantic: Informations relative to a group of locations"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    event_id: int
    efs_id: Optional[str] = None

    url: str
    time: str
    events: list[ScheduleEventSchema]

    def to_list(self) -> list[ScheduleSchema]:
        schedules = []
        for event in self.events:
            schedules.append(
                ScheduleSchema(
                    **event.model_dump(),
                    **self.model_dump(exclude={"events"}),
                )
            )
        return schedules
