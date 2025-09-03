import re
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict


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

    def info(self) -> dict:
        return {
            **self.model_dump(include=["id", "lp_code"]),
            "date": self.date.isoformat(),
        }


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

    def info(self) -> dict:
        return {
            **self.model_dump(
                include=[
                    "id",
                    "efs_id",
                    "location_id",
                    "is_public",
                    "is_publishable",
                    "url",
                    "nature",
                ]
            ),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }
