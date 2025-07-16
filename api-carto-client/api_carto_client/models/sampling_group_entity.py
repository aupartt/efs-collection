import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SamplingGroupEntity")


@_attrs_define
class SamplingGroupEntity:
    """Objet représentant un groupement

    Attributes:
        gr_code (Union[None, Unset, str]): Code
        gr_lib (Union[None, Unset, str]): Libellé
        gr_desd (Union[None, Unset, datetime.datetime]):
    """

    gr_code: Union[None, Unset, str] = UNSET
    gr_lib: Union[None, Unset, str] = UNSET
    gr_desd: Union[None, Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        gr_code: Union[None, Unset, str]
        if isinstance(self.gr_code, Unset):
            gr_code = UNSET
        else:
            gr_code = self.gr_code

        gr_lib: Union[None, Unset, str]
        if isinstance(self.gr_lib, Unset):
            gr_lib = UNSET
        else:
            gr_lib = self.gr_lib

        gr_desd: Union[None, Unset, str]
        if isinstance(self.gr_desd, Unset):
            gr_desd = UNSET
        elif isinstance(self.gr_desd, datetime.datetime):
            gr_desd = self.gr_desd.isoformat()
        else:
            gr_desd = self.gr_desd

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if gr_code is not UNSET:
            field_dict["grCode"] = gr_code
        if gr_lib is not UNSET:
            field_dict["grLib"] = gr_lib
        if gr_desd is not UNSET:
            field_dict["grDesd"] = gr_desd

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_gr_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gr_code = _parse_gr_code(d.pop("grCode", UNSET))

        def _parse_gr_lib(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gr_lib = _parse_gr_lib(d.pop("grLib", UNSET))

        def _parse_gr_desd(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                gr_desd_type_0 = isoparse(data)

                return gr_desd_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        gr_desd = _parse_gr_desd(d.pop("grDesd", UNSET))

        sampling_group_entity = cls(
            gr_code=gr_code,
            gr_lib=gr_lib,
            gr_desd=gr_desd,
        )

        return sampling_group_entity
