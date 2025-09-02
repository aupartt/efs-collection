from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sampling_location_collections_entity import SamplingLocationCollectionsEntity
    from ..models.sampling_location_sf_entity import SamplingLocationSFEntity


T = TypeVar("T", bound="SamplingCollectionResult")


@_attrs_define
class SamplingCollectionResult:
    """Objet de résultat de recherche de collectes

    Attributes:
        sampling_location_entities_sf (Union[None, Unset, list['SamplingLocationSFEntity']]): Lieux de collectes fixes
        sampling_location_collections (Union[None, Unset, list['SamplingLocationCollectionsEntity']]): Lieux et
            collectes mobiles
    """

    sampling_location_entities_sf: Union[None, Unset, list["SamplingLocationSFEntity"]] = UNSET
    sampling_location_collections: Union[None, Unset, list["SamplingLocationCollectionsEntity"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        sampling_location_entities_sf: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.sampling_location_entities_sf, Unset):
            sampling_location_entities_sf = UNSET
        elif isinstance(self.sampling_location_entities_sf, list):
            sampling_location_entities_sf = []
            for sampling_location_entities_sf_type_0_item_data in self.sampling_location_entities_sf:
                sampling_location_entities_sf_type_0_item = sampling_location_entities_sf_type_0_item_data.to_dict()
                sampling_location_entities_sf.append(sampling_location_entities_sf_type_0_item)

        else:
            sampling_location_entities_sf = self.sampling_location_entities_sf

        sampling_location_collections: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.sampling_location_collections, Unset):
            sampling_location_collections = UNSET
        elif isinstance(self.sampling_location_collections, list):
            sampling_location_collections = []
            for sampling_location_collections_type_0_item_data in self.sampling_location_collections:
                sampling_location_collections_type_0_item = sampling_location_collections_type_0_item_data.to_dict()
                sampling_location_collections.append(sampling_location_collections_type_0_item)

        else:
            sampling_location_collections = self.sampling_location_collections

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if sampling_location_entities_sf is not UNSET:
            field_dict["samplingLocationEntities_SF"] = sampling_location_entities_sf
        if sampling_location_collections is not UNSET:
            field_dict["samplingLocationCollections"] = sampling_location_collections

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sampling_location_collections_entity import SamplingLocationCollectionsEntity
        from ..models.sampling_location_sf_entity import SamplingLocationSFEntity

        d = dict(src_dict)

        def _parse_sampling_location_entities_sf(data: object) -> Union[None, Unset, list["SamplingLocationSFEntity"]]:
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
            return cast(Union[None, Unset, list["SamplingLocationSFEntity"]], data)

        sampling_location_entities_sf = _parse_sampling_location_entities_sf(
            d.pop("samplingLocationEntities_SF", UNSET)
        )

        def _parse_sampling_location_collections(
            data: object,
        ) -> Union[None, Unset, list["SamplingLocationCollectionsEntity"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sampling_location_collections_type_0 = []
                _sampling_location_collections_type_0 = data
                for sampling_location_collections_type_0_item_data in _sampling_location_collections_type_0:
                    sampling_location_collections_type_0_item = SamplingLocationCollectionsEntity.from_dict(
                        sampling_location_collections_type_0_item_data
                    )

                    sampling_location_collections_type_0.append(sampling_location_collections_type_0_item)

                return sampling_location_collections_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["SamplingLocationCollectionsEntity"]], data)

        sampling_location_collections = _parse_sampling_location_collections(
            d.pop("samplingLocationCollections", UNSET)
        )

        sampling_collection_result = cls(
            sampling_location_entities_sf=sampling_location_entities_sf,
            sampling_location_collections=sampling_location_collections,
        )

        return sampling_collection_result
