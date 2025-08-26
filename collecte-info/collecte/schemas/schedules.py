from datetime import date, datetime, time

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
)


class ScheduleSchema(BaseModel):
    """Pydantic: Informations relative to a schedule event"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    event_id: int | None = None
    efs_id: str = None

    # Details
    date: date
    url: str
    created_at: datetime

    # Data
    collecte_type: str
    timetables: dict[time, int]

    @computed_field
    @property
    def total_slots(self) -> int:
        return sum([value for value in self.timetables.values()])

    @computed_field
    @property
    def timetable_min(self) -> time:
        keys = self.timetables.keys()
        if len(keys) > 0:
            return min(keys)

    @computed_field
    @property
    def timetable_max(self) -> time:
        keys = self.timetables.keys()
        if len(keys) > 0:
            return max(keys)

    def info(self) -> dict:
        return {
            **self.model_dump(
                include=["event_id", "efs_id", "url", "collecte_type"]
            ),
            "date": self.date.isoformat()
        }

    @field_validator("date", mode="before")
    def convert_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y").date()
        return value

    @field_validator("timetables", mode="before")
    def convert_timetables_keys(cls, value):
        if not isinstance(value, dict):
            return {}
        new_timetables = {}
        for k, v in value.items():
            if isinstance(k, str):
                new_timetables[datetime.strptime(k, "%Hh%M").time()] = v
            else:
                new_timetables[k] = v
        return new_timetables

    @field_serializer("timetables")
    def serialize_timetables_keys(self, timetables: dict[time, int]):
        if not isinstance(timetables, dict):
            return {}
        new_timetables = {}
        for k, v in timetables.items():
            if isinstance(k, str):
                new_timetables[k] = v
            else:
                new_timetables[k.isoformat()] = v
        return new_timetables


class ScheduleEventSchema(BaseModel):
    """Pydantic: Informations relative to a schedule event"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    date: str
    # total_slots: int = Field(..., alias="slots") Changed into @computed_field of ScheduleSchema
    collecte_type: str = Field(..., alias="type")
    timetables: dict[str, int] = Field(default_factory=dict, alias="schedules")


class ScheduleGroupSchema(BaseModel):
    """Pydantic: Informations relative to a group of locations"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    efs_id: str | None = None

    url: str
    created_at: datetime = Field(..., alias="time")
    events: list[ScheduleEventSchema]

    def info(self) -> dict:
        return self.model_dump(include=["efs_id", "url"])

    def build(self) -> list[ScheduleSchema]:
        schedules = []
        for event in self.events:
            schedules.append(
                ScheduleSchema(
                    **event.model_dump() | self.model_dump(exclude={"events"}),
                )
            )
        return schedules
