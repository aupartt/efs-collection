import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SamplingCollectionEntity")


@_attrs_define
class SamplingCollectionEntity:
    """Objet de retour de collecte

    Attributes:
        date (Union[None, Unset, datetime.datetime]): Date de la collecte.
        group_code (Union[None, Unset, str]): Code de groupement du lieu de prélévement (SITEFX ou code de mobilité).
        id (Union[Unset, float]): Identifiant de la collecte (avec le code région).
        is_public (Union[None, Unset, bool]): Indique si la collecte est publique, privée ou inconnue.
        is_publishable (Union[None, Unset, bool]): Indique si la collecte est publiable, non publiable ou inconnue.
        lp_code (Union[None, Unset, str]): Code du lieu de prélèvement.
        morning_end_time (Union[None, Unset, str]): Heure de fin du matin de la collecte.
        morning_start_time (Union[None, Unset, str]): Heure de début du matin de la collecte.
        afternoon_end_time (Union[None, Unset, str]): Heure de fin de l'après-midi de la collecte.
        afternoon_start_time (Union[None, Unset, str]): Heure de début de l'après-midi de la collecte.
        nature (Union[None, Unset, str]): Le caractère de la collecte (commune, professionnel, enseignement, armée...).
        url_blood (Union[None, Unset, str]): Lien don de sans
        url_plasma (Union[None, Unset, str]): Lien don de plasma
        url_platelet (Union[None, Unset, str]): Lien don de plaquettes
        convocation_label_long (Union[None, Unset, str]): Libellé de convocation
        convocation_label_sms (Union[None, Unset, str]): Libellé de convocation court (SMS)
        taux_remplissage (Union[None, Unset, float]): Taux de remplissage de la collecte
        children (Union[None, Unset, list['SamplingCollectionEntity']]): Collectes filles
        nb_places_restantes_st (Union[None, Unset, int]): Places restantes Sang Total
        nb_places_totales_st (Union[None, Unset, int]): Places Totale Sang Total
        nb_places_reservees_st (Union[None, Unset, int]): Places réservées Sang Total
        nb_places_restantes_pla (Union[None, Unset, int]): Places restantes Plasma
        nb_places_totales_pla (Union[None, Unset, int]): Places totales Plasma
        nb_places_reservees_pla (Union[None, Unset, int]): Places részervées Plasma
        nb_places_restantes_cpa (Union[None, Unset, int]): Places restantes Plaquettes
        nb_places_totales_cpa (Union[None, Unset, int]): Places totales Plaquettes
        nb_places_reservees_cpa (Union[None, Unset, int]): Places réservées Plaquettes
        propose_planning_rdv (Union[None, Unset, bool]): La collecte propose un planning
    """

    date: None | Unset | datetime.datetime = UNSET
    group_code: None | Unset | str = UNSET
    id: Unset | float = UNSET
    is_public: None | Unset | bool = UNSET
    is_publishable: None | Unset | bool = UNSET
    lp_code: None | Unset | str = UNSET
    morning_end_time: None | Unset | str = UNSET
    morning_start_time: None | Unset | str = UNSET
    afternoon_end_time: None | Unset | str = UNSET
    afternoon_start_time: None | Unset | str = UNSET
    nature: None | Unset | str = UNSET
    url_blood: None | Unset | str = UNSET
    url_plasma: None | Unset | str = UNSET
    url_platelet: None | Unset | str = UNSET
    convocation_label_long: None | Unset | str = UNSET
    convocation_label_sms: None | Unset | str = UNSET
    taux_remplissage: None | Unset | float = UNSET
    children: None | Unset | list["SamplingCollectionEntity"] = UNSET
    nb_places_restantes_st: None | Unset | int = UNSET
    nb_places_totales_st: None | Unset | int = UNSET
    nb_places_reservees_st: None | Unset | int = UNSET
    nb_places_restantes_pla: None | Unset | int = UNSET
    nb_places_totales_pla: None | Unset | int = UNSET
    nb_places_reservees_pla: None | Unset | int = UNSET
    nb_places_restantes_cpa: None | Unset | int = UNSET
    nb_places_totales_cpa: None | Unset | int = UNSET
    nb_places_reservees_cpa: None | Unset | int = UNSET
    propose_planning_rdv: None | Unset | bool = UNSET

    def to_dict(self) -> dict[str, Any]:
        date: None | Unset | str
        if isinstance(self.date, Unset):
            date = UNSET
        elif isinstance(self.date, datetime.datetime):
            date = self.date.isoformat()
        else:
            date = self.date

        group_code: None | Unset | str
        if isinstance(self.group_code, Unset):
            group_code = UNSET
        else:
            group_code = self.group_code

        id = self.id

        is_public: None | Unset | bool
        if isinstance(self.is_public, Unset):
            is_public = UNSET
        else:
            is_public = self.is_public

        is_publishable: None | Unset | bool
        if isinstance(self.is_publishable, Unset):
            is_publishable = UNSET
        else:
            is_publishable = self.is_publishable

        lp_code: None | Unset | str
        if isinstance(self.lp_code, Unset):
            lp_code = UNSET
        else:
            lp_code = self.lp_code

        morning_end_time: None | Unset | str
        if isinstance(self.morning_end_time, Unset):
            morning_end_time = UNSET
        else:
            morning_end_time = self.morning_end_time

        morning_start_time: None | Unset | str
        if isinstance(self.morning_start_time, Unset):
            morning_start_time = UNSET
        else:
            morning_start_time = self.morning_start_time

        afternoon_end_time: None | Unset | str
        if isinstance(self.afternoon_end_time, Unset):
            afternoon_end_time = UNSET
        else:
            afternoon_end_time = self.afternoon_end_time

        afternoon_start_time: None | Unset | str
        if isinstance(self.afternoon_start_time, Unset):
            afternoon_start_time = UNSET
        else:
            afternoon_start_time = self.afternoon_start_time

        nature: None | Unset | str
        if isinstance(self.nature, Unset):
            nature = UNSET
        else:
            nature = self.nature

        url_blood: None | Unset | str
        if isinstance(self.url_blood, Unset):
            url_blood = UNSET
        else:
            url_blood = self.url_blood

        url_plasma: None | Unset | str
        if isinstance(self.url_plasma, Unset):
            url_plasma = UNSET
        else:
            url_plasma = self.url_plasma

        url_platelet: None | Unset | str
        if isinstance(self.url_platelet, Unset):
            url_platelet = UNSET
        else:
            url_platelet = self.url_platelet

        convocation_label_long: None | Unset | str
        if isinstance(self.convocation_label_long, Unset):
            convocation_label_long = UNSET
        else:
            convocation_label_long = self.convocation_label_long

        convocation_label_sms: None | Unset | str
        if isinstance(self.convocation_label_sms, Unset):
            convocation_label_sms = UNSET
        else:
            convocation_label_sms = self.convocation_label_sms

        taux_remplissage: None | Unset | float
        if isinstance(self.taux_remplissage, Unset):
            taux_remplissage = UNSET
        else:
            taux_remplissage = self.taux_remplissage

        children: None | Unset | list[dict[str, Any]]
        if isinstance(self.children, Unset):
            children = UNSET
        elif isinstance(self.children, list):
            children = []
            for children_type_0_item_data in self.children:
                children_type_0_item = children_type_0_item_data.to_dict()
                children.append(children_type_0_item)

        else:
            children = self.children

        nb_places_restantes_st: None | Unset | int
        if isinstance(self.nb_places_restantes_st, Unset):
            nb_places_restantes_st = UNSET
        else:
            nb_places_restantes_st = self.nb_places_restantes_st

        nb_places_totales_st: None | Unset | int
        if isinstance(self.nb_places_totales_st, Unset):
            nb_places_totales_st = UNSET
        else:
            nb_places_totales_st = self.nb_places_totales_st

        nb_places_reservees_st: None | Unset | int
        if isinstance(self.nb_places_reservees_st, Unset):
            nb_places_reservees_st = UNSET
        else:
            nb_places_reservees_st = self.nb_places_reservees_st

        nb_places_restantes_pla: None | Unset | int
        if isinstance(self.nb_places_restantes_pla, Unset):
            nb_places_restantes_pla = UNSET
        else:
            nb_places_restantes_pla = self.nb_places_restantes_pla

        nb_places_totales_pla: None | Unset | int
        if isinstance(self.nb_places_totales_pla, Unset):
            nb_places_totales_pla = UNSET
        else:
            nb_places_totales_pla = self.nb_places_totales_pla

        nb_places_reservees_pla: None | Unset | int
        if isinstance(self.nb_places_reservees_pla, Unset):
            nb_places_reservees_pla = UNSET
        else:
            nb_places_reservees_pla = self.nb_places_reservees_pla

        nb_places_restantes_cpa: None | Unset | int
        if isinstance(self.nb_places_restantes_cpa, Unset):
            nb_places_restantes_cpa = UNSET
        else:
            nb_places_restantes_cpa = self.nb_places_restantes_cpa

        nb_places_totales_cpa: None | Unset | int
        if isinstance(self.nb_places_totales_cpa, Unset):
            nb_places_totales_cpa = UNSET
        else:
            nb_places_totales_cpa = self.nb_places_totales_cpa

        nb_places_reservees_cpa: None | Unset | int
        if isinstance(self.nb_places_reservees_cpa, Unset):
            nb_places_reservees_cpa = UNSET
        else:
            nb_places_reservees_cpa = self.nb_places_reservees_cpa

        propose_planning_rdv: None | Unset | bool
        if isinstance(self.propose_planning_rdv, Unset):
            propose_planning_rdv = UNSET
        else:
            propose_planning_rdv = self.propose_planning_rdv

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if group_code is not UNSET:
            field_dict["groupCode"] = group_code
        if id is not UNSET:
            field_dict["id"] = id
        if is_public is not UNSET:
            field_dict["isPublic"] = is_public
        if is_publishable is not UNSET:
            field_dict["isPublishable"] = is_publishable
        if lp_code is not UNSET:
            field_dict["lpCode"] = lp_code
        if morning_end_time is not UNSET:
            field_dict["morningEndTime"] = morning_end_time
        if morning_start_time is not UNSET:
            field_dict["morningStartTime"] = morning_start_time
        if afternoon_end_time is not UNSET:
            field_dict["afternoonEndTime"] = afternoon_end_time
        if afternoon_start_time is not UNSET:
            field_dict["afternoonStartTime"] = afternoon_start_time
        if nature is not UNSET:
            field_dict["nature"] = nature
        if url_blood is not UNSET:
            field_dict["urlBlood"] = url_blood
        if url_plasma is not UNSET:
            field_dict["urlPlasma"] = url_plasma
        if url_platelet is not UNSET:
            field_dict["urlPlatelet"] = url_platelet
        if convocation_label_long is not UNSET:
            field_dict["convocationLabelLong"] = convocation_label_long
        if convocation_label_sms is not UNSET:
            field_dict["convocationLabelSMS"] = convocation_label_sms
        if taux_remplissage is not UNSET:
            field_dict["tauxRemplissage"] = taux_remplissage
        if children is not UNSET:
            field_dict["children"] = children
        if nb_places_restantes_st is not UNSET:
            field_dict["nbPlacesRestantesST"] = nb_places_restantes_st
        if nb_places_totales_st is not UNSET:
            field_dict["nbPlacesTotalesST"] = nb_places_totales_st
        if nb_places_reservees_st is not UNSET:
            field_dict["nbPlacesReserveesST"] = nb_places_reservees_st
        if nb_places_restantes_pla is not UNSET:
            field_dict["nbPlacesRestantesPLA"] = nb_places_restantes_pla
        if nb_places_totales_pla is not UNSET:
            field_dict["nbPlacesTotalesPLA"] = nb_places_totales_pla
        if nb_places_reservees_pla is not UNSET:
            field_dict["nbPlacesReserveesPLA"] = nb_places_reservees_pla
        if nb_places_restantes_cpa is not UNSET:
            field_dict["nbPlacesRestantesCPA"] = nb_places_restantes_cpa
        if nb_places_totales_cpa is not UNSET:
            field_dict["nbPlacesTotalesCPA"] = nb_places_totales_cpa
        if nb_places_reservees_cpa is not UNSET:
            field_dict["nbPlacesReserveesCPA"] = nb_places_reservees_cpa
        if propose_planning_rdv is not UNSET:
            field_dict["proposePlanningRdv"] = propose_planning_rdv

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_date(data: object) -> None | Unset | datetime.datetime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_type_0 = isoparse(data)

                return date_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.datetime, data)

        date = _parse_date(d.pop("date", UNSET))

        def _parse_group_code(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        group_code = _parse_group_code(d.pop("groupCode", UNSET))

        id = d.pop("id", UNSET)

        def _parse_is_public(data: object) -> None | Unset | bool:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | bool, data)

        is_public = _parse_is_public(d.pop("isPublic", UNSET))

        def _parse_is_publishable(data: object) -> None | Unset | bool:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | bool, data)

        is_publishable = _parse_is_publishable(d.pop("isPublishable", UNSET))

        def _parse_lp_code(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        lp_code = _parse_lp_code(d.pop("lpCode", UNSET))

        def _parse_morning_end_time(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        morning_end_time = _parse_morning_end_time(d.pop("morningEndTime", UNSET))

        def _parse_morning_start_time(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        morning_start_time = _parse_morning_start_time(d.pop("morningStartTime", UNSET))

        def _parse_afternoon_end_time(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        afternoon_end_time = _parse_afternoon_end_time(d.pop("afternoonEndTime", UNSET))

        def _parse_afternoon_start_time(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        afternoon_start_time = _parse_afternoon_start_time(d.pop("afternoonStartTime", UNSET))

        def _parse_nature(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        nature = _parse_nature(d.pop("nature", UNSET))

        def _parse_url_blood(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        url_blood = _parse_url_blood(d.pop("urlBlood", UNSET))

        def _parse_url_plasma(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        url_plasma = _parse_url_plasma(d.pop("urlPlasma", UNSET))

        def _parse_url_platelet(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        url_platelet = _parse_url_platelet(d.pop("urlPlatelet", UNSET))

        def _parse_convocation_label_long(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        convocation_label_long = _parse_convocation_label_long(d.pop("convocationLabelLong", UNSET))

        def _parse_convocation_label_sms(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        convocation_label_sms = _parse_convocation_label_sms(d.pop("convocationLabelSMS", UNSET))

        def _parse_taux_remplissage(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        taux_remplissage = _parse_taux_remplissage(d.pop("tauxRemplissage", UNSET))

        def _parse_children(data: object) -> None | Unset | list["SamplingCollectionEntity"]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                children_type_0 = []
                _children_type_0 = data
                for children_type_0_item_data in _children_type_0:
                    children_type_0_item = SamplingCollectionEntity.from_dict(children_type_0_item_data)

                    children_type_0.append(children_type_0_item)

                return children_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | list["SamplingCollectionEntity"], data)

        children = _parse_children(d.pop("children", UNSET))

        def _parse_nb_places_restantes_st(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_restantes_st = _parse_nb_places_restantes_st(d.pop("nbPlacesRestantesST", UNSET))

        def _parse_nb_places_totales_st(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_totales_st = _parse_nb_places_totales_st(d.pop("nbPlacesTotalesST", UNSET))

        def _parse_nb_places_reservees_st(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_reservees_st = _parse_nb_places_reservees_st(d.pop("nbPlacesReserveesST", UNSET))

        def _parse_nb_places_restantes_pla(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_restantes_pla = _parse_nb_places_restantes_pla(d.pop("nbPlacesRestantesPLA", UNSET))

        def _parse_nb_places_totales_pla(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_totales_pla = _parse_nb_places_totales_pla(d.pop("nbPlacesTotalesPLA", UNSET))

        def _parse_nb_places_reservees_pla(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_reservees_pla = _parse_nb_places_reservees_pla(d.pop("nbPlacesReserveesPLA", UNSET))

        def _parse_nb_places_restantes_cpa(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_restantes_cpa = _parse_nb_places_restantes_cpa(d.pop("nbPlacesRestantesCPA", UNSET))

        def _parse_nb_places_totales_cpa(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_totales_cpa = _parse_nb_places_totales_cpa(d.pop("nbPlacesTotalesCPA", UNSET))

        def _parse_nb_places_reservees_cpa(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        nb_places_reservees_cpa = _parse_nb_places_reservees_cpa(d.pop("nbPlacesReserveesCPA", UNSET))

        def _parse_propose_planning_rdv(data: object) -> None | Unset | bool:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | bool, data)

        propose_planning_rdv = _parse_propose_planning_rdv(d.pop("proposePlanningRdv", UNSET))

        sampling_collection_entity = cls(
            date=date,
            group_code=group_code,
            id=id,
            is_public=is_public,
            is_publishable=is_publishable,
            lp_code=lp_code,
            morning_end_time=morning_end_time,
            morning_start_time=morning_start_time,
            afternoon_end_time=afternoon_end_time,
            afternoon_start_time=afternoon_start_time,
            nature=nature,
            url_blood=url_blood,
            url_plasma=url_plasma,
            url_platelet=url_platelet,
            convocation_label_long=convocation_label_long,
            convocation_label_sms=convocation_label_sms,
            taux_remplissage=taux_remplissage,
            children=children,
            nb_places_restantes_st=nb_places_restantes_st,
            nb_places_totales_st=nb_places_totales_st,
            nb_places_reservees_st=nb_places_reservees_st,
            nb_places_restantes_pla=nb_places_restantes_pla,
            nb_places_totales_pla=nb_places_totales_pla,
            nb_places_reservees_pla=nb_places_reservees_pla,
            nb_places_restantes_cpa=nb_places_restantes_cpa,
            nb_places_totales_cpa=nb_places_totales_cpa,
            nb_places_reservees_cpa=nb_places_reservees_cpa,
            propose_planning_rdv=propose_planning_rdv,
        )

        return sampling_collection_entity
