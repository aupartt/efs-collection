from typing import TYPE_CHECKING, Optional, Union
from pydantic import BaseModel, ConfigDict, Field

from collecte.schemas.collection import CollectionSchema, CollectionGroupSchema


class LocationSchema(BaseModel):
    """Pydantic: Informations relative to a location where events can be scheduled"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: Optional[int] = None
    sampling_location_code: str = Field(alias="samplingLocationCode")
    region_code: Optional[str] = Field(alias="regionCode")

    # Address info
    name: Optional[str] = ""
    city: Optional[str] = ""
    post_code: str = Field(alias="postCode")
    full_address: str = Field(alias="fullAddress")
    address1: Optional[str] = ""
    address2: Optional[str] = ""

    # Coordinates
    latitude: float
    longitude: float

    # Services offered
    give_blood: bool = Field(alias="giveBlood")
    give_plasma: bool = Field(alias="givePlasma")
    give_platelet: bool = Field(alias="givePlatelet")

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

    # Relations
    group_code: str = Field(alias="groupCode")
    collections: Optional[list[Union["CollectionSchema", "CollectionGroupSchema"]]] = []

    def info(self) -> str:
        return f"{str(self.group_code):>6} - {str(self.post_code):>5} - {str(self.city):>20} - {self.name}"
