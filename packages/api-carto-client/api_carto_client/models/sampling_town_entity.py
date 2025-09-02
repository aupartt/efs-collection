from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SamplingTownEntity")


@_attrs_define
class SamplingTownEntity:
    """Objet de commune

    Attributes:
        nom (Union[None, Unset, str]): Nom de la commune
        code_postal (Union[None, Unset, str]): Code postal
        lat (Union[Unset, float]): Latitude
        lon (Union[Unset, float]): Longitude
    """

    nom: None | Unset | str = UNSET
    code_postal: None | Unset | str = UNSET
    lat: Unset | float = UNSET
    lon: Unset | float = UNSET

    def to_dict(self) -> dict[str, Any]:
        nom: None | Unset | str
        if isinstance(self.nom, Unset):
            nom = UNSET
        else:
            nom = self.nom

        code_postal: None | Unset | str
        if isinstance(self.code_postal, Unset):
            code_postal = UNSET
        else:
            code_postal = self.code_postal

        lat = self.lat

        lon = self.lon

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if nom is not UNSET:
            field_dict["nom"] = nom
        if code_postal is not UNSET:
            field_dict["codePostal"] = code_postal
        if lat is not UNSET:
            field_dict["lat"] = lat
        if lon is not UNSET:
            field_dict["lon"] = lon

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_nom(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        nom = _parse_nom(d.pop("nom", UNSET))

        def _parse_code_postal(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        code_postal = _parse_code_postal(d.pop("codePostal", UNSET))

        lat = d.pop("lat", UNSET)

        lon = d.pop("lon", UNSET)

        sampling_town_entity = cls(
            nom=nom,
            code_postal=code_postal,
            lat=lat,
            lon=lon,
        )

        return sampling_town_entity
