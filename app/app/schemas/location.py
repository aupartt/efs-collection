from typing import Union

from pydantic import BaseModel, ConfigDict, Field

from collector.schemas.collection import CollectionGroupSchema, CollectionSchema


class LocationSchema(BaseModel):
    """Pydantic: Informations relative to a location where events can be scheduled"""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int | None = None
    sampling_location_code: str = Field(alias="samplingLocationCode")
    region_code: str | None = Field(alias="regionCode")

    # Address info
    name: str | None = ""
    city: str | None = ""
    post_code: str = Field(alias="postCode")
    full_address: str = Field(alias="fullAddress")
    address1: str | None = ""
    address2: str | None = ""

    # Coordinates
    latitude: float
    longitude: float

    # Services offered
    give_blood: bool = Field(alias="giveBlood")
    give_plasma: bool = Field(alias="givePlasma")
    give_platelet: bool = Field(alias="givePlatelet")

    # Additional information
    horaires: str | None = None
    infos: str | None = None
    metro: str | None = None
    bus: str | None = None
    tram: str | None = None
    parking: str | None = None
    debut_infos: str | None = Field(alias="debutInfos", default=None)
    fin_infos: str | None = Field(alias="finInfos", default=None)
    ville: str | None = None
    phone: str | None = None

    # Relations
    group_code: str = Field(alias="groupCode")
    collections: list[Union["CollectionSchema", "CollectionGroupSchema"]] | None = []

    def info(self) -> dict:
        return {
            **self.model_dump(
                include=[
                    "id",
                    "city",
                    "post_code",
                    "full_address",
                    "group_code",
                    "latitude",
                    "longitude",
                ]
            ),
            # Avoid KeyError: "Attempt to overwrite 'name' in LogRecord"
            "location_name": self.name,
        }
