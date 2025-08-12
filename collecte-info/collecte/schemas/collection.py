import re
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field


class CollectionGroupSnapshotSchema(BaseModel):
    """Pydantic: Snapshot of stats for an collection group"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int | None

    taux_remplissage: float | None = None

    # Blood slots
    nb_places_restantes_st: int | None = None
    nb_places_totales_st: int | None = None
    nb_places_reservees_st: int | None = None

    # Plasma slots
    nb_places_restantes_pla: int | None = None
    nb_places_totales_pla: int | None = None
    nb_places_reservees_pla: int | None = None

    # Platelet slots
    nb_places_restantes_cpa: int | None = None
    nb_places_totales_cpa: int | None = None
    nb_places_reservees_cpa: int | None = None

    # Relations
    collection_group_id: int | None = None


class CollectionEventSchema(BaseModel):
    """Pydantic: Single event information"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    lp_code: str

    date: datetime

    morning_start_time: time | None = None
    morning_end_time: time | None = None
    afternoon_start_time: time | None = None
    afternoon_end_time: time | None = None

    # Relations
    collection_group_id: int | None = None


class CollectionGroupSchema(BaseModel):
    """Pydantic: Global data for a group of events"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int | None = None
    efs_id: str | None = None

    # Date
    start_date: datetime = None
    end_date: datetime = None

    # Details
    nature: str | None
    is_public: bool
    is_publishable: bool
    propose_planning_rdv: bool

    # URLs
    url_blood: str | None = None
    url_plasma: str | None = None
    url_platelet: str | None = None

    # Text descriptions
    convocation_label_long: str | None = None
    convocation_label_sms: str | None = None

    # Relations
    group_code: str | None = None
    location_id: int | None = None
    events: list[CollectionEventSchema] = []
    snapshots: list[CollectionGroupSnapshotSchema] = []

    @property
    def url(self) -> str:
        """Return the first available url for booking"""
        url = None

        if self.url_blood:
            url = self.url_blood
        elif self.url_plasma:
            url = self.url_plasma
        elif self.url_platelet:
            url = self.url_platelet

        if url and not re.match(r"https?://", url):
            url = f"https://{url}"

        return url

    def update_ids(self, _id: int):
        for snapshot in self.snapshots:
            snapshot.collection_group_id = _id

        for event in self.events:
            event.collection_group_id = _id

    def info(self) -> str:
        return f"{str(self.efs_id):>6} - {str(self.url):22} - {self.nature}"


class CollectionSchema(BaseModel):
    """Pydantic: Main collection information"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int | None = None
    efs_id: str | None = None
    group_code: str | None = Field(alias="groupCode")

    # Date and timing
    date: datetime
    morning_end_time: time | None = Field(alias="morningEndTime")
    morning_start_time: time | None = Field(alias="morningStartTime")
    afternoon_end_time: time | None = Field(alias="afternoonEndTime")
    afternoon_start_time: time | None = Field(alias="afternoonStartTime")

    # Collection details
    nature: str | None = None
    lp_code: str = Field(alias="lpCode")
    is_public: bool = Field(alias="isPublic")
    is_publishable: bool = Field(alias="isPublishable")
    propose_planning_rdv: bool = Field(alias="proposePlanningRdv")

    # Capacity info
    taux_remplissage: float | None = Field(alias="tauxRemplissage", default=None)
    nb_places_restantes_st: int | None = Field(
        alias="nbPlacesRestantesST", default=None
    )
    nb_places_totales_st: int | None = Field(alias="nbPlacesTotalesST", default=None)
    nb_places_reservees_st: int | None = Field(
        alias="nbPlacesReserveesST", default=None
    )
    nb_places_restantes_pla: int | None = Field(
        alias="nbPlacesRestantesPLA", default=None
    )
    nb_places_totales_pla: int | None = Field(alias="nbPlacesTotalesPLA", default=None)
    nb_places_reservees_pla: int | None = Field(
        alias="nbPlacesReserveesPLA", default=None
    )
    nb_places_restantes_cpa: int | None = Field(
        alias="nbPlacesRestantesCPA", default=None
    )
    nb_places_totales_cpa: int | None = Field(alias="nbPlacesTotalesCPA", default=None)
    nb_places_reservees_cpa: int | None = Field(
        alias="nbPlacesReserveesCPA", default=None
    )

    # URLs for booking
    url_blood: str | None = Field(alias="urlBlood", default=None)
    url_plasma: str | None = Field(alias="urlPlasma", default=None)
    url_platelet: str | None = Field(alias="urlPlatelet", default=None)

    # Text descriptions
    convocation_label_long: str | None = Field(
        alias="convocationLabelLong", default=None
    )
    convocation_label_sms: str | None = Field(alias="convocationLabelSMS", default=None)

    # Handle children collections
    children: list["CollectionSchema"] | None = []

    @property
    def url(self) -> str:
        """Return the first available url for booking"""
        url = None

        if self.url_blood:
            url = self.url_blood
        elif self.url_plasma:
            url = self.url_plasma
        elif self.url_platelet:
            url = self.url_platelet

        if url and not re.match(r"https?://", url):
            url = f"https://{url}"

        return url

    def get_dates(self) -> str:
        """Return the last available date for booking"""
        dates = []
        if self.date:
            dates.append(self.date)
        if self.children:
            child_dates = [child.date for child in self.children if child.date]
            dates.extend(child_dates)
        return dates

    def snapshot(self, from_db=False) -> CollectionGroupSnapshotSchema:
        """Generate a snapshot for the collection"""
        snapshot = CollectionGroupSnapshotSchema.model_validate(self)
        if not from_db:
            # Make sure to not take an event ID as PK
            snapshot.id = None
        return snapshot

    def event(self, data) -> CollectionEventSchema:
        """Generate an event from the given data"""
        event = CollectionEventSchema.model_validate(data)
        return event

    def events(self, from_db=False) -> list[CollectionEventSchema]:
        """Generate all events from a collection"""
        events = []
        main_event = self.event(self)
        events.append(main_event)

        if self.children:
            child_events = [self.event(child) for child in self.children]
            events.extend(child_events)

        return events

    def as_group(self, from_db=False) -> CollectionGroupSchema:
        """Return the collection as a group"""
        dates = self.get_dates()
        snapshot = self.snapshot(from_db)
        events = self.events(from_db)
        group = CollectionGroupSchema(
            **self.model_dump(),
            snapshots=[snapshot],
            events=events,
            start_date=min(dates),
            end_date=max(dates),
        )
        if not from_db:
            # Make sure to not take an event ID as PK
            group.id = None
        return group
