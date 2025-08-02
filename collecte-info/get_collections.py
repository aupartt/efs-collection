import json
from pathlib import Path
import logging
from tqdm import tqdm
import time

from api_carto_client import Client
from api_carto_client.models.ping import Ping
from api_carto_client.models.sampling_collection_entity import SamplingCollectionEntity
from api_carto_client.models.sampling_collection_result import SamplingCollectionResult
from api_carto_client.models.sampling_location_entity import SamplingLocationEntity
from api_carto_client.api.ping import get_carto_api_v3_ping as api_ping
from api_carto_client.api.sampling_collection import (
    get_carto_api_v3_samplingcollection_searchbypostcode as api_search_collection,
)


logger = logging.getLogger(__name__)


LOCATIONS_FILE = Path("data/locations.jsonl")
COLLECTIONS_FILE = Path("data/collections.jsonl")


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
def get_collections(client: Client, post_code: str) -> list[SamplingCollectionEntity]:
    collections: SamplingCollectionResult = api_search_collection.sync(
        client=client,
        post_code=post_code,
        hide_private_collects=True,
        page=1,
        limit=100,
        user_latitude=48.11,
        user_longitude=-1.67,
    )
    return collections.sampling_location_collections


def load_postal_codes() -> set[str]:
    if not LOCATIONS_FILE.is_file():
        logger.error(f"Le fichier {LOCATIONS_FILE} n'existe pas")
        time.sleep(5)
        return set()
    with LOCATIONS_FILE.open("r", encoding="utf-8") as file:
        return {
            SamplingLocationEntity.from_dict(json.loads(line)).post_code
            for line in file
        }


if __name__ == "__main__":
    post_codes = load_postal_codes()

    print(f"Chargement des collectes pour {len(post_codes)} codes postaux:")

    with COLLECTIONS_FILE.open("w", encoding="utf-8") as file:
        for postal_code in tqdm(post_codes):
            collections = get_collections(postal_code)
            for collection in collections:
                file.write(json.dumps(collection.to_dict(), indent=None))
                file.write("\n")
