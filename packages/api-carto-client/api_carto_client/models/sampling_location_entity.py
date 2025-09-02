import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SamplingLocationEntity")


@_attrs_define
class SamplingLocationEntity:
    """Entité de base pour les lieux de prélèvements mobiles.

    Attributes:
        address1 (Union[None, Unset, str]): Ligne d'adresse n°1.
        address2 (Union[None, Unset, str]): Ligne d'adresse n°2.
        city (Union[None, Unset, str]): Ville du lieu de prélévement.
        convocation_label (Union[None, Unset, str]): Le libellé de convocation.
        distance (Union[Unset, float]): Distance depuis le point de recherche ou le centre de la zone de recherche.
        full_address (Union[None, Unset, str]): Adresse complète.
        give_blood (Union[Unset, int]): Si Vrai, il est possible de donner son sang dans ce lieu.
        give_plasma (Union[Unset, int]): Si Vrai, il est possible de donner son plasma dans ce lieu.
        give_platelet (Union[Unset, int]): Si Vrai, il est possible de donner ses plaquettes dans ce lieu.
        region_code (Union[None, Unset, str]): Code région
            Nécessaire pour la recherche des collectes via l'API MonRDV
        group_code (Union[None, Unset, str]): Code de groupement du lieu de prélévement (SITEFX ou code de mobilité).
        latitude (Union[Unset, float]): Latitude.
        longitude (Union[Unset, float]): Longitude.
        name (Union[None, Unset, str]): Libellé du lieu de prélévement.
        post_code (Union[None, Unset, str]): Code postal du lieu de prélévement.
        sampling_location_code (Union[None, Unset, str]): Code du lieu de prélèvement.
        horaires (Union[None, Unset, str]): Information d'horaires
        infos (Union[None, Unset, str]): Informations sur le lieu
        metro (Union[None, Unset, str]): Informations metro
        bus (Union[None, Unset, str]): Informations bus
        tram (Union[None, Unset, str]): Informations tram
        parking (Union[None, Unset, str]): Informations parking
        debut_infos (Union[None, Unset, datetime.datetime]):
        fin_infos (Union[None, Unset, datetime.datetime]):
        ville (Union[None, Unset, str]): Ville
        id (Union[None, Unset, int]): Identifiant du lieu de prélévement.
        phone (Union[None, Unset, str]): Numéro de téléphone du lieu de prélévement.
        url_blood (Union[None, Unset, str]): Url de prise de RDV pour le sang
        url_plasma (Union[None, Unset, str]): Url de prise de RDV pour le plasma
        url_platelets (Union[None, Unset, str]): Url de prise de RDV pour les plaquettes
    """

    address1: Union[None, Unset, str] = UNSET
    address2: Union[None, Unset, str] = UNSET
    city: Union[None, Unset, str] = UNSET
    convocation_label: Union[None, Unset, str] = UNSET
    distance: Union[Unset, float] = UNSET
    full_address: Union[None, Unset, str] = UNSET
    give_blood: Union[Unset, int] = UNSET
    give_plasma: Union[Unset, int] = UNSET
    give_platelet: Union[Unset, int] = UNSET
    region_code: Union[None, Unset, str] = UNSET
    group_code: Union[None, Unset, str] = UNSET
    latitude: Union[Unset, float] = UNSET
    longitude: Union[Unset, float] = UNSET
    name: Union[None, Unset, str] = UNSET
    post_code: Union[None, Unset, str] = UNSET
    sampling_location_code: Union[None, Unset, str] = UNSET
    horaires: Union[None, Unset, str] = UNSET
    infos: Union[None, Unset, str] = UNSET
    metro: Union[None, Unset, str] = UNSET
    bus: Union[None, Unset, str] = UNSET
    tram: Union[None, Unset, str] = UNSET
    parking: Union[None, Unset, str] = UNSET
    debut_infos: Union[None, Unset, datetime.datetime] = UNSET
    fin_infos: Union[None, Unset, datetime.datetime] = UNSET
    ville: Union[None, Unset, str] = UNSET
    id: Union[None, Unset, int] = UNSET
    phone: Union[None, Unset, str] = UNSET
    url_blood: Union[None, Unset, str] = UNSET
    url_plasma: Union[None, Unset, str] = UNSET
    url_platelets: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        address1: Union[None, Unset, str]
        if isinstance(self.address1, Unset):
            address1 = UNSET
        else:
            address1 = self.address1

        address2: Union[None, Unset, str]
        if isinstance(self.address2, Unset):
            address2 = UNSET
        else:
            address2 = self.address2

        city: Union[None, Unset, str]
        if isinstance(self.city, Unset):
            city = UNSET
        else:
            city = self.city

        convocation_label: Union[None, Unset, str]
        if isinstance(self.convocation_label, Unset):
            convocation_label = UNSET
        else:
            convocation_label = self.convocation_label

        distance = self.distance

        full_address: Union[None, Unset, str]
        if isinstance(self.full_address, Unset):
            full_address = UNSET
        else:
            full_address = self.full_address

        give_blood = self.give_blood

        give_plasma = self.give_plasma

        give_platelet = self.give_platelet

        region_code: Union[None, Unset, str]
        if isinstance(self.region_code, Unset):
            region_code = UNSET
        else:
            region_code = self.region_code

        group_code: Union[None, Unset, str]
        if isinstance(self.group_code, Unset):
            group_code = UNSET
        else:
            group_code = self.group_code

        latitude = self.latitude

        longitude = self.longitude

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        post_code: Union[None, Unset, str]
        if isinstance(self.post_code, Unset):
            post_code = UNSET
        else:
            post_code = self.post_code

        sampling_location_code: Union[None, Unset, str]
        if isinstance(self.sampling_location_code, Unset):
            sampling_location_code = UNSET
        else:
            sampling_location_code = self.sampling_location_code

        horaires: Union[None, Unset, str]
        if isinstance(self.horaires, Unset):
            horaires = UNSET
        else:
            horaires = self.horaires

        infos: Union[None, Unset, str]
        if isinstance(self.infos, Unset):
            infos = UNSET
        else:
            infos = self.infos

        metro: Union[None, Unset, str]
        if isinstance(self.metro, Unset):
            metro = UNSET
        else:
            metro = self.metro

        bus: Union[None, Unset, str]
        if isinstance(self.bus, Unset):
            bus = UNSET
        else:
            bus = self.bus

        tram: Union[None, Unset, str]
        if isinstance(self.tram, Unset):
            tram = UNSET
        else:
            tram = self.tram

        parking: Union[None, Unset, str]
        if isinstance(self.parking, Unset):
            parking = UNSET
        else:
            parking = self.parking

        debut_infos: Union[None, Unset, str]
        if isinstance(self.debut_infos, Unset):
            debut_infos = UNSET
        elif isinstance(self.debut_infos, datetime.datetime):
            debut_infos = self.debut_infos.isoformat()
        else:
            debut_infos = self.debut_infos

        fin_infos: Union[None, Unset, str]
        if isinstance(self.fin_infos, Unset):
            fin_infos = UNSET
        elif isinstance(self.fin_infos, datetime.datetime):
            fin_infos = self.fin_infos.isoformat()
        else:
            fin_infos = self.fin_infos

        ville: Union[None, Unset, str]
        if isinstance(self.ville, Unset):
            ville = UNSET
        else:
            ville = self.ville

        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        phone: Union[None, Unset, str]
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        url_blood: Union[None, Unset, str]
        if isinstance(self.url_blood, Unset):
            url_blood = UNSET
        else:
            url_blood = self.url_blood

        url_plasma: Union[None, Unset, str]
        if isinstance(self.url_plasma, Unset):
            url_plasma = UNSET
        else:
            url_plasma = self.url_plasma

        url_platelets: Union[None, Unset, str]
        if isinstance(self.url_platelets, Unset):
            url_platelets = UNSET
        else:
            url_platelets = self.url_platelets

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if address1 is not UNSET:
            field_dict["address1"] = address1
        if address2 is not UNSET:
            field_dict["address2"] = address2
        if city is not UNSET:
            field_dict["city"] = city
        if convocation_label is not UNSET:
            field_dict["convocationLabel"] = convocation_label
        if distance is not UNSET:
            field_dict["distance"] = distance
        if full_address is not UNSET:
            field_dict["fullAddress"] = full_address
        if give_blood is not UNSET:
            field_dict["giveBlood"] = give_blood
        if give_plasma is not UNSET:
            field_dict["givePlasma"] = give_plasma
        if give_platelet is not UNSET:
            field_dict["givePlatelet"] = give_platelet
        if region_code is not UNSET:
            field_dict["regionCode"] = region_code
        if group_code is not UNSET:
            field_dict["groupCode"] = group_code
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if name is not UNSET:
            field_dict["name"] = name
        if post_code is not UNSET:
            field_dict["postCode"] = post_code
        if sampling_location_code is not UNSET:
            field_dict["samplingLocationCode"] = sampling_location_code
        if horaires is not UNSET:
            field_dict["horaires"] = horaires
        if infos is not UNSET:
            field_dict["infos"] = infos
        if metro is not UNSET:
            field_dict["metro"] = metro
        if bus is not UNSET:
            field_dict["bus"] = bus
        if tram is not UNSET:
            field_dict["tram"] = tram
        if parking is not UNSET:
            field_dict["parking"] = parking
        if debut_infos is not UNSET:
            field_dict["debutInfos"] = debut_infos
        if fin_infos is not UNSET:
            field_dict["finInfos"] = fin_infos
        if ville is not UNSET:
            field_dict["ville"] = ville
        if id is not UNSET:
            field_dict["id"] = id
        if phone is not UNSET:
            field_dict["phone"] = phone
        if url_blood is not UNSET:
            field_dict["urlBlood"] = url_blood
        if url_plasma is not UNSET:
            field_dict["urlPlasma"] = url_plasma
        if url_platelets is not UNSET:
            field_dict["urlPlatelets"] = url_platelets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_address1(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        address1 = _parse_address1(d.pop("address1", UNSET))

        def _parse_address2(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        address2 = _parse_address2(d.pop("address2", UNSET))

        def _parse_city(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        city = _parse_city(d.pop("city", UNSET))

        def _parse_convocation_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        convocation_label = _parse_convocation_label(d.pop("convocationLabel", UNSET))

        distance = d.pop("distance", UNSET)

        def _parse_full_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        full_address = _parse_full_address(d.pop("fullAddress", UNSET))

        give_blood = d.pop("giveBlood", UNSET)

        give_plasma = d.pop("givePlasma", UNSET)

        give_platelet = d.pop("givePlatelet", UNSET)

        def _parse_region_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        region_code = _parse_region_code(d.pop("regionCode", UNSET))

        def _parse_group_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_code = _parse_group_code(d.pop("groupCode", UNSET))

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_post_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        post_code = _parse_post_code(d.pop("postCode", UNSET))

        def _parse_sampling_location_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sampling_location_code = _parse_sampling_location_code(d.pop("samplingLocationCode", UNSET))

        def _parse_horaires(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        horaires = _parse_horaires(d.pop("horaires", UNSET))

        def _parse_infos(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        infos = _parse_infos(d.pop("infos", UNSET))

        def _parse_metro(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metro = _parse_metro(d.pop("metro", UNSET))

        def _parse_bus(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bus = _parse_bus(d.pop("bus", UNSET))

        def _parse_tram(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tram = _parse_tram(d.pop("tram", UNSET))

        def _parse_parking(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parking = _parse_parking(d.pop("parking", UNSET))

        def _parse_debut_infos(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                debut_infos_type_0 = isoparse(data)

                return debut_infos_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        debut_infos = _parse_debut_infos(d.pop("debutInfos", UNSET))

        def _parse_fin_infos(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                fin_infos_type_0 = isoparse(data)

                return fin_infos_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        fin_infos = _parse_fin_infos(d.pop("finInfos", UNSET))

        def _parse_ville(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ville = _parse_ville(d.pop("ville", UNSET))

        def _parse_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_phone(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        phone = _parse_phone(d.pop("phone", UNSET))

        def _parse_url_blood(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url_blood = _parse_url_blood(d.pop("urlBlood", UNSET))

        def _parse_url_plasma(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url_plasma = _parse_url_plasma(d.pop("urlPlasma", UNSET))

        def _parse_url_platelets(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url_platelets = _parse_url_platelets(d.pop("urlPlatelets", UNSET))

        sampling_location_entity = cls(
            address1=address1,
            address2=address2,
            city=city,
            convocation_label=convocation_label,
            distance=distance,
            full_address=full_address,
            give_blood=give_blood,
            give_plasma=give_plasma,
            give_platelet=give_platelet,
            region_code=region_code,
            group_code=group_code,
            latitude=latitude,
            longitude=longitude,
            name=name,
            post_code=post_code,
            sampling_location_code=sampling_location_code,
            horaires=horaires,
            infos=infos,
            metro=metro,
            bus=bus,
            tram=tram,
            parking=parking,
            debut_infos=debut_infos,
            fin_infos=fin_infos,
            ville=ville,
            id=id,
            phone=phone,
            url_blood=url_blood,
            url_plasma=url_plasma,
            url_platelets=url_platelets,
        )

        return sampling_location_entity
