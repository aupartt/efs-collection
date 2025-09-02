from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SamplingRegionEntity")


@_attrs_define
class SamplingRegionEntity:
    """Objet de région

    Attributes:
        libelle (Union[None, Unset, str]): Libellé
        acronyme (Union[None, Unset, str]): Acronyme
        monogramme (Union[None, Unset, str]): Monogramme
        code (Union[None, Unset, str]): Code de la région
    """

    libelle: None | Unset | str = UNSET
    acronyme: None | Unset | str = UNSET
    monogramme: None | Unset | str = UNSET
    code: None | Unset | str = UNSET

    def to_dict(self) -> dict[str, Any]:
        libelle: None | Unset | str
        if isinstance(self.libelle, Unset):
            libelle = UNSET
        else:
            libelle = self.libelle

        acronyme: None | Unset | str
        if isinstance(self.acronyme, Unset):
            acronyme = UNSET
        else:
            acronyme = self.acronyme

        monogramme: None | Unset | str
        if isinstance(self.monogramme, Unset):
            monogramme = UNSET
        else:
            monogramme = self.monogramme

        code: None | Unset | str
        if isinstance(self.code, Unset):
            code = UNSET
        else:
            code = self.code

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if libelle is not UNSET:
            field_dict["libelle"] = libelle
        if acronyme is not UNSET:
            field_dict["acronyme"] = acronyme
        if monogramme is not UNSET:
            field_dict["monogramme"] = monogramme
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_libelle(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        libelle = _parse_libelle(d.pop("libelle", UNSET))

        def _parse_acronyme(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        acronyme = _parse_acronyme(d.pop("acronyme", UNSET))

        def _parse_monogramme(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        monogramme = _parse_monogramme(d.pop("monogramme", UNSET))

        def _parse_code(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        code = _parse_code(d.pop("code", UNSET))

        sampling_region_entity = cls(
            libelle=libelle,
            acronyme=acronyme,
            monogramme=monogramme,
            code=code,
        )

        return sampling_region_entity
