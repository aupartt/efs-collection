import json
from pathlib import Path
import logging
from api_carto_client import Client
from api_carto_client.models.ping import Ping
from api_carto_client.models.sampling_region_entity import SamplingRegionEntity
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.models.sampling_location_entity import SamplingLocationEntity
from api_carto_client.api.ping import get_carto_api_v3_ping as api_ping
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getregions as api_get_regions,
)
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getgroupements as api_get_groupements,
)
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_searchbygrouplocationcode as api_search_location,
)

FICHIER_GROUPEMENTS = Path("data/groupements.jsonl")
FICHIER_LIEUX = Path("data/lieux.jsonl")


def with_api_client(func):
    def wrapper(*args, **kwargs):
        client = Client(base_url="https://oudonner.api.efs.sante.fr/")
        with client as cli:
            return func(cli, *args, **kwargs)

    return wrapper


@with_api_client
def check_api(client: Client):
    ping_resp: Ping = api_ping.sync(client=client)
    if ping_resp.version != "v3":
        raise Exception(
            f"Le serveur exécute l'API en {ping_resp.version}, mais seule la v3 est supportée"
        )


@with_api_client
def get_region(client: Client, nom: str) -> SamplingRegionEntity:
    regions: list[SamplingRegionEntity] = api_get_regions.sync(client=client)
    for region in regions:
        if region.libelle == nom:
            return region
    return None


@with_api_client
def get_groupements(client: Client, region: SamplingRegionEntity):
    groupements: list[SamplingGroupEntity] = api_get_groupements.sync(
        client=client, region_code=region.code
    )
    return groupements


@with_api_client
def get_lieux_prelevement(client: Client, groupement: SamplingGroupEntity):
    res: SamplingLocationEntity = api_search_location.sync(
        client=client, group_code=groupement.gr_code
    )
    return res.sampling_location_entities


def charger_groupements_traites() -> set[SamplingGroupEntity]:
    groupements_traites = set()

    if not FICHIER_LIEUX.is_file():
        return groupements_traites

    with FICHIER_LIEUX.open("r", encoding="utf-8") as fp:
        for line in fp:
            lieu = json.loads(line)
            groupements_traites.add(lieu["groupCode"])

    return groupements_traites


def load_groupements() -> list[SamplingGroupEntity]:
    groupements: list[SamplingGroupEntity] = []

    if FICHIER_GROUPEMENTS.is_file():
        logging.info("Chargement des groupements depuis le fichier")
        with FICHIER_GROUPEMENTS.open("r", encoding="utf-8") as fp:
            for line in fp:
                groupement = SamplingGroupEntity.from_dict(json.loads(line))
                groupements.append(groupement)
    else:
        logging.info("Chargement des groupements depuis l'API")
        region_bretagne: SamplingRegionEntity = get_region(nom="Bretagne")
        if region_bretagne is None:
            logging.error(
                "Impossible de télécharger l'identifiant de la région Bretagne"
            )
            exit(1)
        with FICHIER_GROUPEMENTS.open("w", encoding="utf-8") as fp:
            groupements = get_groupements(region=region_bretagne)
            for groupement in groupements:
                fp.write(json.dumps(groupement.to_dict(), indent=None))
                fp.write("\n")

    return groupements


if __name__ == "__main__":
    groupements = load_groupements()
    groupements_traites = charger_groupements_traites()

    with Path(FICHIER_LIEUX).open("a", encoding="utf-8") as fp_lieux:
        for groupement in groupements:
            if groupement.gr_code in groupements_traites:
                continue
            logging.info(f"Téléchargement des lieux de {groupement.gr_code}")
            lieux = get_lieux_prelevement(groupement=groupement)
            for lieu in lieux:
                if lieu.post_code[0:2] not in {"22", "29", "35", "56"}:
                    logging.warning(
                        f"Code postal inattendu dans le groupement {groupement.gr_lib}: '{lieu.post_code}'"
                    )
                else:
                    fp_lieux.write(json.dumps(lieu.to_dict(), indent=None))
                    fp_lieux.write("\n")

    logging.info(f"Groupements en Bretagne: {len(groupements)}")
