from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SnapshotSchedulesSchema(BaseModel):
    """Pydantic: Snapshot of schedules for a Collection availability at a specific time"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int]
    url: str
    efs_id: Optional[int]  # ID from the url
    crawled_at: datetime  # When this data was collected
    slots: int  # Number of slots available at crawl time
    schedules: dict  # JSON of schedules at crawl time


class SnapshotCollectionSchema(BaseModel):
    """Pydantic: Snapshot of a Collection availability at a specific time"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    snapshot_id: Optional[int]
    id: int  # EFS id
    efs_id: Optional[int]  # ID from the url
    date: datetime  # When the collection is happening
    lp_code: str

    # Date and timing
    morning_start_time: Optional[time]
    morning_end_time: Optional[time]
    afternoon_start_time: Optional[time]
    afternoon_end_time: Optional[time]

    # Capacity info
    taux_remplissage: Optional[float] = Field(alias="tauxRemplissage")
    nb_places_restantes_st: Optional[int] = Field(
        alias="nbPlacesRestantesST", default=None
    )
    nb_places_totales_st: Optional[int] = Field(alias="nbPlacesTotalesST")
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

    schedules: Optional[SnapshotSchedulesSchema] = []
