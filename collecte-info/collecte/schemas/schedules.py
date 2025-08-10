from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ScheduleSchema(BaseModel):
    """Pydantic: Informations relative to a schedule event"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    event_id: int | None = None
    efs_id: str | None = None

    # Details
    date: datetime
    url: str
    created_at: datetime

    # Data
    total_slots: int
    collecte_type: str
    schedules: dict[time, int]
    
    @property
    def schedule_min(self):
        return min(self.schedules.keys())
    
    @property
    def schedule_max(self):
        return max(self.schedules.keys())

    def info(self):
        return f"{self.efs_id:>6} - {datetime.strftime('%d/%m/%Y')}"

    @field_validator('date', mode='before')
    def convert_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y").date()
        return value

    @field_validator('schedules', mode='before')
    def convert_schedules_keys(cls, value):
        if not isinstance(value, dict):
            return {}
        new_schedules = {}
        for k, v in value.items():
            if isinstance(k, str):
                new_schedules[datetime.strptime(k, "%Hh%M").time()] = v
            else:
                new_schedules[k] = v
        return new_schedules


class ScheduleEventSchema(BaseModel):
    """Pydantic: Informations relative to a schedule event"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    date: str
    total_slots: int = Field(..., alias="slots")
    collecte_type: str = Field(..., alias="type")
    schedules: dict[str, int]


class ScheduleGroupSchema(BaseModel):
    """Pydantic: Informations relative to a group of locations"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    efs_id: str | None = None

    url: str
    created_at: datetime = Field(..., alias="time")
    events: list[ScheduleEventSchema]

    def build(self) -> list[ScheduleSchema]:
        schedules = []
        for event in self.events:
            schedules.append(
                ScheduleSchema(
                    **event.model_dump() | self.model_dump(exclude={"events"}),
                )
            )
        return schedules
