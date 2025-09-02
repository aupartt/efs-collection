from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sampling_location_entity import SamplingLocationEntity
    from ..models.sampling_location_sf_entity import SamplingLocationSFEntity


T = TypeVar("T", bound="SamplingLocationResult")


@_attrs_define
class SamplingLocationResult:
    """Objet de retour des lieux de prélèvemenet

    Attributes:
        sampling_location_entities_sf (Union[None, Unset, list['SamplingLocationSFEntity']]): Lieux de prélèvement fixes
        sampling_location_entities (Union[None, Unset, list['SamplingLocationEntity']]): Lieux de prélèvement mobiles
    """

    sampling_location_entities_sf: None | Unset | list["SamplingLocationSFEntity"] = UNSET
    sampling_location_entities: None | Unset | list["SamplingLocationEntity"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        sampling_location_entities_sf: None | Unset | list[dict[str, Any]]
        if isinstance(self.sampling_location_entities_sf, Unset):
            sampling_location_entities_sf = UNSET
        elif isinstance(self.sampling_location_entities_sf, list):
            sampling_location_entities_sf = []
            for sampling_location_entities_sf_type_0_item_data in self.sampling_location_entities_sf:
                sampling_location_entities_sf_type_0_item = sampling_location_entities_sf_type_0_item_data.to_dict()
                sampling_location_entities_sf.append(sampling_location_entities_sf_type_0_item)

        else:
            sampling_location_entities_sf = self.sampling_location_entities_sf

        sampling_location_entities: None | Unset | list[dict[str, Any]]
        if isinstance(self.sampling_location_entities, Unset):
            sampling_location_entities = UNSET
        elif isinstance(self.sampling_location_entities, list):
            sampling_location_entities = []
            for sampling_location_entities_type_0_item_data in self.sampling_location_entities:
                sampling_location_entities_type_0_item = sampling_location_entities_type_0_item_data.to_dict()
                sampling_location_entities.append(sampling_location_entities_type_0_item)

        else:
            sampling_location_entities = self.sampling_location_entities

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if sampling_location_entities_sf is not UNSET:
            field_dict["samplingLocationEntities_SF"] = sampling_location_entities_sf
        if sampling_location_entities is not UNSET:
            field_dict["samplingLocationEntities"] = sampling_location_entities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sampling_location_entity import SamplingLocationEntity
        from ..models.sampling_location_sf_entity import SamplingLocationSFEntity

        d = dict(src_dict)

        def _parse_sampling_location_entities_sf(data: object) -> None | Unset | list["SamplingLocationSFEntity"]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sampling_location_entities_sf_type_0 = []
                _sampling_location_entities_sf_type_0 = data
                for sampling_location_entities_sf_type_0_item_data in _sampling_location_entities_sf_type_0:
                    sampling_location_entities_sf_type_0_item = SamplingLocationSFEntity.from_dict(
                        sampling_location_entities_sf_type_0_item_data
                    )

                    sampling_location_entities_sf_type_0.append(sampling_location_entities_sf_type_0_item)

                return sampling_location_entities_sf_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | list["SamplingLocationSFEntity"], data)

        sampling_location_entities_sf = _parse_sampling_location_entities_sf(
            d.pop("samplingLocationEntities_SF", UNSET)
        )

        def _parse_sampling_location_entities(data: object) -> None | Unset | list["SamplingLocationEntity"]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sampling_location_entities_type_0 = []
                _sampling_location_entities_type_0 = data
                for sampling_location_entities_type_0_item_data in _sampling_location_entities_type_0:
                    sampling_location_entities_type_0_item = SamplingLocationEntity.from_dict(
                        sampling_location_entities_type_0_item_data
                    )

                    sampling_location_entities_type_0.append(sampling_location_entities_type_0_item)

                return sampling_location_entities_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | list["SamplingLocationEntity"], data)

        sampling_location_entities = _parse_sampling_location_entities(d.pop("samplingLocationEntities", UNSET))

        sampling_location_result = cls(
            sampling_location_entities_sf=sampling_location_entities_sf,
            sampling_location_entities=sampling_location_entities,
        )

        return sampling_location_result
