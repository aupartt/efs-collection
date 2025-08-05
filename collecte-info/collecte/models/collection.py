from datetime import datetime, time
from typing import Optional, List
from pydantic import BaseModel, Field


class CollectionModel(BaseModel):
    date: datetime
    group_code: str = Field(alias="groupCode")
    id: int
    is_public: bool = Field(alias="isPublic")
    is_publishable: bool = Field(alias="isPublishable")
    lp_code: str = Field(alias="lpCode")

    morning_end_time: Optional[time] = Field(alias="morningEndTime")
    morning_start_time: Optional[time] = Field(alias="morningStartTime")
    afternoon_end_time: Optional[time] = Field(alias="afternoonEndTime")
    afternoon_start_time: Optional[time] = Field(alias="afternoonStartTime")

    nature: Optional[str] = None
    url_blood: Optional[str] = Field(alias="urlBlood", default=None)
    url_plasma: Optional[str] = Field(alias="urlPlasma", default=None)
    url_platelet: Optional[str] = Field(alias="urlPlatelet", default=None)

    convocation_label_long: Optional[str] = Field(
        alias="convocationLabelLong", default=None
    )
    convocation_label_sms: Optional[str] = Field(
        alias="convocationLabelSMS", default=None
    )

    taux_remplissage: Optional[float] = Field(alias="tauxRemplissage", default=None)

    # Slot information
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

    propose_planning_rdv: bool = Field(alias="proposePlanningRdv")

    # Handle children collections
    children: Optional[List["CollectionModel"]] = None

    class Config:
        allow_population_by_field_name = True
