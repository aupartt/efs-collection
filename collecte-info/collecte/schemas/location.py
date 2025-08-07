from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class LocationSchema(BaseModel):
    """Pydantic: Informations relative to a location where events can be scheduled"""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int] = None
    sampling_location_code: str = Field(alias="samplingLocationCode")
    group_code: str = Field(alias="groupCode")
    region_code: str = Field(alias="regionCode")

    # Address info
    name: str
    city: Optional[str]
    post_code: str = Field(alias="postCode")
    full_address: str = Field(alias="fullAddress")
    address1: Optional[str]
    address2: Optional[str]

    # Coordinates
    latitude: float
    longitude: float

    # Services offered
    give_blood: bool = Field(alias="giveBlood")
    give_plasma: bool = Field(alias="givePlasma")
    give_platelet: bool = Field(alias="givePlatelet")

    # URLs
    # url_blood: Optional[str] = Field(alias="urlBlood", default=None)
    # url_plasma: Optional[str] = Field(alias="urlPlasma", default=None)
    # url_platelets: Optional[str] = Field(alias="urlPlatelets", default=None)

    # Additional information
    horaires: Optional[str] = None
    infos: Optional[str] = None
    metro: Optional[str] = None
    bus: Optional[str] = None
    tram: Optional[str] = None
    parking: Optional[str] = None
    debut_infos: Optional[str] = Field(alias="debutInfos", default=None)
    fin_infos: Optional[str] = Field(alias="finInfos", default=None)
    ville: Optional[str] = None
    phone: Optional[str] = None
