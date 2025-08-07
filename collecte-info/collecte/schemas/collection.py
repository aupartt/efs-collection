from datetime import datetime, time
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict, Field

from .snapshot import SnapshotCollectionSchema


class CollectionSchema(BaseModel):
    """Pydantic: Informations relative of a collection"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int] = None
    group_code: str = Field(alias="groupCode")
    sampling_location_code: str = Field(alias="samplingLocationCode")

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
    children: Optional[list["CollectionSchema"]] = None


class CollectionDBSchema(BaseModel):
    """Pydantic: Database Collection schema"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int] = None
    efs_id: Optional[int] = None  # ID from the url

    # Date and timing
    date_start: datetime
    date_end: datetime
    morning_end_time_min_max: Optional[time]
    morning_start_time: Optional[time]
    afternoon_end_time_min: Optional[time]
    afternoon_start_time_max: Optional[time]

    # Collection details
    nature: Optional[str] = None
    is_public: bool = Field(alias="isPublic")
    is_publishable: bool = Field(alias="isPublishable")
    propose_planning_rdv: bool = Field(alias="proposePlanningRdv")

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

    snapshots: Optional[list["SnapshotCollectionSchema"]] = []