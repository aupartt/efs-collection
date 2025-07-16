from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SamplingSquareEntity")


@_attrs_define
class SamplingSquareEntity:
    """Objet de retour de l'autozoom

    Attributes:
        north_east_latitude (Union[Unset, float]): Latitude Nord-Est
        north_east_longitude (Union[Unset, float]): Longitude Nord-Est
        south_west_latitude (Union[Unset, float]): Latitude Sud-Ouest
        south_west_longitude (Union[Unset, float]): Longitude Sud-Ouest
    """

    north_east_latitude: Union[Unset, float] = UNSET
    north_east_longitude: Union[Unset, float] = UNSET
    south_west_latitude: Union[Unset, float] = UNSET
    south_west_longitude: Union[Unset, float] = UNSET

    def to_dict(self) -> dict[str, Any]:
        north_east_latitude = self.north_east_latitude

        north_east_longitude = self.north_east_longitude

        south_west_latitude = self.south_west_latitude

        south_west_longitude = self.south_west_longitude

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if north_east_latitude is not UNSET:
            field_dict["northEastLatitude"] = north_east_latitude
        if north_east_longitude is not UNSET:
            field_dict["northEastLongitude"] = north_east_longitude
        if south_west_latitude is not UNSET:
            field_dict["southWestLatitude"] = south_west_latitude
        if south_west_longitude is not UNSET:
            field_dict["southWestLongitude"] = south_west_longitude

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        north_east_latitude = d.pop("northEastLatitude", UNSET)

        north_east_longitude = d.pop("northEastLongitude", UNSET)

        south_west_latitude = d.pop("southWestLatitude", UNSET)

        south_west_longitude = d.pop("southWestLongitude", UNSET)

        sampling_square_entity = cls(
            north_east_latitude=north_east_latitude,
            north_east_longitude=north_east_longitude,
            south_west_latitude=south_west_latitude,
            south_west_longitude=south_west_longitude,
        )

        return sampling_square_entity
