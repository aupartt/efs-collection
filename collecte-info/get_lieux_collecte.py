import json
from pathlib import Path
import logging
from tqdm import tqdm
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


logger = logging.getLogger(__name__)

GROUPS_FILE = Path("data/groups.jsonl")
LOCATIONS_FILE = Path("data/locations.jsonl")
REGION_NAME = "Bretagne"


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
def get_region(client: Client, name: str) -> SamplingRegionEntity:
    regions: list[SamplingRegionEntity] = api_get_regions.sync(client=client)
    for region in regions:
        if region.libelle == name:
            return region
    return None


@with_api_client
def get_groups(client: Client, region: SamplingRegionEntity):
    groups: list[SamplingGroupEntity] = api_get_groupements.sync(
        client=client, region_code=region.code
    )
    return groups


@with_api_client
def get_location_sampling(client: Client, groupement: SamplingGroupEntity):
    res: SamplingLocationEntity = api_search_location.sync(
        client=client, group_code=groupement.gr_code
    )
    return res.sampling_location_entities


def load_processed_groups() -> set[SamplingGroupEntity]:
    processed_groups = set()

    if not LOCATIONS_FILE.is_file():
        return processed_groups

    with LOCATIONS_FILE.open("r", encoding="utf-8") as fp:
        for line in fp:
            lieu = json.loads(line)
            processed_groups.add(lieu["groupCode"])

    logger.info(f"Groupements déjà traités chargés: {len(processed_groups)}")
    return processed_groups


def load_groups() -> list[SamplingGroupEntity]:
    groups: list[SamplingGroupEntity] = []

    if GROUPS_FILE.is_file():
        logger.info("Chargement des groupements depuis le fichier")
        with GROUPS_FILE.open("r", encoding="utf-8") as fp:
            for line in fp:
                group = SamplingGroupEntity.from_dict(json.loads(line))
                groups.append(group)
    else:
        logger.info("Chargement des groupements depuis l'API")
        region: SamplingRegionEntity = get_region(name=REGION_NAME)

        if region is None:
            logger.error(
                "Impossible de télécharger l'identifiant de la région Bretagne"
            )
            exit(1)

        with GROUPS_FILE.open("w", encoding="utf-8") as file:
            groups = get_groups(region=region)
            for group in groups:
                file.write(json.dumps(group.to_dict(), indent=None))
                file.write("\n")

    return groups


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    groups = load_groups()
    processed_groups = load_processed_groups()

    with Path(LOCATIONS_FILE).open("a", encoding="utf-8") as file:
        logger.info("Téléchargement des lieux de collecte:")
        for group in tqdm(groups):
            if group.gr_code in processed_groups:
                continue
            locations = get_location_sampling(groupement=group)
            for location in locations:
                if location.post_code[0:2] not in {"22", "29", "35", "56"}:
                    # logger.warning(
                    #     f"Code postal inattendu dans le groupement {group.gr_lib}: '{location.post_code}'"
                    # )
                    continue
                else:
                    file.write(json.dumps(location.to_dict(), indent=None))
                    file.write("\n")

    logger.info(f"Groupements en Bretagne: {len(groups)}")
