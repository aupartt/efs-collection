import logging
import requests
import re

from api_carto_client import Client
from api_carto_client.models.sampling_collection_entity import SamplingCollectionEntity
from api_carto_client.models.sampling_collection_result import SamplingCollectionResult
from api_carto_client.api.sampling_collection import (
    get_carto_api_v3_samplingcollection_searchbypostcode as api_search_collection,
)

from collecte.core.database import get_db
from collecte.schemas import (
    CollectionSchema,
    CollectionDBSchema,
    SnapshotCollectionSchema,
)
from collecte.models import CollectionModel, SnapshotCollectionModel
from collecte.services.utils import (
    api_to_pydantic,
    update_all,
    with_api_client,
    check_api,
)
from .locations import get_postal_codes

logger = logging.getLogger(__name__)


@with_api_client
def _retrieve_collections(client: Client, post_code: str) -> list[CollectionSchema]:
    collections: SamplingCollectionResult = api_search_collection.sync(
        client=client,
        post_code=post_code,
        hide_private_collects=True,
        page=1,
        limit=100,
        user_latitude=48.11,
        user_longitude=-1.67,
    )
    return api_to_pydantic(collections.sampling_location_collections, CollectionSchema)


def _get_collection_url(collections: list[CollectionSchema]) -> str:
    """Retrieve url from collections,
    it doesn't matter if the url is for blood, plasma or platelets as the crawler will try to get all informations.
    """
    url = None

    for collection in collections:
        if collection.get("urlBlood"):
            url = collection["urlBlood"]
        elif collection.get("urlPlasma"):
            url = collection["urlPlasma"]
        elif collection.get("urlPlatelets"):
            url = collection["urlPlatelets"]

    if not url:
        raise ValueError("No url found in collections")

    if not re.match(r"https?://", url):
        url = f"https://{url}"

    return url


def _get_esf_id(url: str) -> str:
    res = requests.head(url, allow_redirects=True)
    reg = r"trouver-une-collecte/([0-9]+)/"
    res = re.search(reg, res.url)
    return res.group(1)


async def _get_collections() -> list[CollectionSchema]:
    if not await check_api():
        return []

    postal_codes = await get_postal_codes()
    collections = []
    for postal_code in postal_codes:
        api_collections = await _retrieve_collections(postal_code)
        collections.extend(api_collections)
    return collections


async def update_collections():
    collections = await _get_collections()


    pass
