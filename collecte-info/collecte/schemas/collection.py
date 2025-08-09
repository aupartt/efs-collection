from datetime import datetime, time
import re
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field


class CollectionGroupSnapshotSchema(BaseModel):
    """Pydantic: Snapshot of stats for an collection group"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int]

    taux_remplissage: Optional[float] = None

    # Blood slots
    nb_places_restantes_st: Optional[int] = None
    nb_places_totales_st: Optional[int] = None
    nb_places_reservees_st: Optional[int] = None

    # Plasma slots
    nb_places_restantes_pla: Optional[int] = None
    nb_places_totales_pla: Optional[int] = None
    nb_places_reservees_pla: Optional[int] = None

    # Platelet slots
    nb_places_restantes_cpa: Optional[int] = None
    nb_places_totales_cpa: Optional[int] = None
    nb_places_reservees_cpa: Optional[int] = None

    # Relations
    collection_group_id: Optional[int] = None


class CollectionEventSchema(BaseModel):
    """Pydantic: Single event information"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    lp_code: str

    date: datetime

    morning_start_time: Optional[time] = None
    morning_end_time: Optional[time] = None
    afternoon_start_time: Optional[time] = None
    afternoon_end_time: Optional[time] = None

    # Relations
    collection_group_id: Optional[int] = None


class CollectionGroupSchema(BaseModel):
    """Pydantic: Global data for a group of events"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int] = None
    efs_id: Optional[str] = None

    # Date
    start_date: datetime = None
    end_date: datetime = None

    # Details
    nature: Optional[str]
    is_public: bool
    is_publishable: bool
    propose_planning_rdv: bool

    # URLs
    url_blood: Optional[str] = None
    url_plasma: Optional[str] = None
    url_platelet: Optional[str] = None

    # Text descriptions
    convocation_label_long: Optional[str] = None
    convocation_label_sms: Optional[str] = None

    # Relations
    group_code: Optional[str] = None
    location_id: Optional[int] = None
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

    def info(self) -> str:
        return f"{str(self.efs_id):>6} - {str(self.url):22} - {self.nature}"

    


class CollectionSchema(BaseModel):
    """Pydantic: Main collection information"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int] = None
    efs_id: Optional[str] = None
    group_code: Optional[str] = Field(alias="groupCode")

    # Date and timing
    date: datetime
    morning_end_time: Optional[time] = Field(alias="morningEndTime")
    morning_start_time: Optional[time] = Field(alias="morningStartTime")
    afternoon_end_time: Optional[time] = Field(alias="afternoonEndTime")
    afternoon_start_time: Optional[time] = Field(alias="afternoonStartTime")

    # Collection details
    nature: Optional[str] = None
    lp_code: str = Field(alias="lpCode")
    is_public: bool = Field(alias="isPublic")
    is_publishable: bool = Field(alias="isPublishable")
    propose_planning_rdv: bool = Field(alias="proposePlanningRdv")

    # Capacity info
    taux_remplissage: Optional[float] = Field(alias="tauxRemplissage", default=None)
    nb_places_restantes_st: Optional[int] = Field(
        alias="nbPlacesRestantesST", default=None
    )
    nb_places_totales_st: Optional[int] = Field(alias="nbPlacesTotalesST", default=None)
    nb_places_reservees_st: Optional[int] = Field(
        alias="nbPlacesReserveesST", default=None
    )
    nb_places_restantes_pla: Optional[int] = Field(
        alias="nbPlacesRestantesPLA", default=None
    )
    nb_places_totales_pla: Optional[int] = Field(
        alias="nbPlacesTotalesPLA", default=None
    )
    nb_places_reservees_pla: Optional[int] = Field(
        alias="nbPlacesReserveesPLA", default=None
    )
    nb_places_restantes_cpa: Optional[int] = Field(
        alias="nbPlacesRestantesCPA", default=None
    )
    nb_places_totales_cpa: Optional[int] = Field(
        alias="nbPlacesTotalesCPA", default=None
    )
    nb_places_reservees_cpa: Optional[int] = Field(
        alias="nbPlacesReserveesCPA", default=None
    )

    # URLs for booking
    url_blood: Optional[str] = Field(alias="urlBlood", default=None)
    url_plasma: Optional[str] = Field(alias="urlPlasma", default=None)
    url_platelet: Optional[str] = Field(alias="urlPlatelet", default=None)

    # Text descriptions
    convocation_label_long: Optional[str] = Field(
        alias="convocationLabelLong", default=None
    )
    convocation_label_sms: Optional[str] = Field(
        alias="convocationLabelSMS", default=None
    )

    # Handle children collections
    children: Optional[list["CollectionSchema"]] = []

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
