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


class GroupScheduleSchema(BaseModel):
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


{
    "url": "https://efs.link/Vcib7",
    "time": "2025-08-10T09:00:39.337881Z",
    "events": [
        {
            "date": "01/10/2025",
            "slots": 76,
            "type": "blood",
            "schedules": {
                "12h00": 1,
                "12h05": 2,
                "12h10": 2,
                "12h15": 0,
                "12h20": 2,
                "12h25": 2,
                "12h30": 1,
                "15h20": 1,
                "15h25": 2,
                "15h30": 1,
                "15h35": 1,
                "15h40": 2,
                "15h45": 1,
                "15h50": 1,
                "15h55": 2,
                "16h00": 0,
            },
        }
    ],
}
