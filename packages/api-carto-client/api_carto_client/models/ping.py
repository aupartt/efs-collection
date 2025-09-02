from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Ping")


@_attrs_define
class Ping:
    """Objet retourné lors d'un ping sur l'API.

    Attributes:
        version (Union[None, Unset, str]): La version de l'API.
        environment (Union[None, Unset, str]): Le nom de l'environnement.
    """

    version: None | Unset | str = UNSET
    environment: None | Unset | str = UNSET

    def to_dict(self) -> dict[str, Any]:
        version: None | Unset | str
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        environment: None | Unset | str
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_version(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        version = _parse_version(d.pop("version", UNSET))

        def _parse_environment(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        environment = _parse_environment(d.pop("environment", UNSET))

        ping = cls(
            version=version,
            environment=environment,
        )

        return ping
