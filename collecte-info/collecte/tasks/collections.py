import asyncio
import logging
import aiohttp
import requests
import re
from api_carto_client import Client
from api_carto_client.models.sampling_location_collections_entity import (
    SamplingLocationCollectionsEntity,
)
from api_carto_client.models.sampling_collection_entity import SamplingCollectionEntity
from api_carto_client.models.sampling_collection_result import SamplingCollectionResult
from api_carto_client.api.sampling_collection import (
    get_carto_api_v3_samplingcollection_searchbypostcode as api_search_collection,
)

# Schemas
from collecte.schemas.location import LocationSchema
from collecte.schemas.collection import (
    CollectionSchema,
    CollectionGroupSchema,
)

# DB Models
from collecte.models.collection import CollectionGroupModel
from collecte.models.location import LocationModel
from collecte.services.utils import with_api_client, check_api
from collecte.services.locations import get_location, get_postal_codes
from collecte.services.collections import save_collection_group

logger = logging.getLogger(__name__)


@with_api_client
async def retrieve_sampling_collections(
    client: Client, post_code: str
) -> list[SamplingLocationCollectionsEntity]:
    """Retrieve collections from the API"""
    collections = await api_search_collection.asyncio(
        client=client,
        post_code=post_code,
        hide_non_publiable_collects=True,
        limit=100,
        user_latitude=48,
        user_longitude=-2,
    )
    if not collections:
        return []
    return collections.sampling_location_collections


async def get_esf_id(url: str) -> str | None:
    """Retrieve ESF id from url"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(url, allow_redirects=True) as resp:
                reg = r"trouver-une-collecte/([0-9]+)/"
                match = re.search(reg, resp.url.raw_path)
                return match.group(1) if match else None
        except asyncio.TimeoutError:
            logger.error(f"Timeout while retrieving ESF id from {url}")
            return None
        except Exception as e:
            logger.error(f"Error while retrieving ESF id from {url}: {e}")
            return None


async def get_collections_locations() -> list[LocationSchema]:
    """Retrieve all collection locations from the API with post_codes and flatten the list"""
    if not await check_api():
        return []
    postal_codes = await get_postal_codes()
    tasks = [retrieve_sampling_collections(postal_code) for postal_code in postal_codes]
    _locations = await asyncio.gather(*tasks)
    locations = [
        LocationSchema(**collection.to_dict())
        for sublist in _locations
        for collection in sublist
    ]
    return locations


async def _handle_collection(collection: CollectionSchema, location_db: LocationModel):
    """Handle a single collection"""
    url = collection.url
    if not url:
        logger.warning(f"No URL found for collection {collection.model_dump(include={"nature", "url_blood", "url_plasma", "url_platelets"})}")
    efs_id = await get_esf_id(url)
    group_collection: CollectionGroupSchema = collection.as_group(from_db=False)
    group_collection.efs_id = efs_id
    await save_collection_group(group_collection, location_db)


async def _handle_location(location: LocationSchema) -> LocationModel:
    """Handle a single location"""
    location_db = await get_location(location)

    return location_db


async def update_collections():
    """Update all collections for all locations"""
    logger.info("Start updating collections...")

    locations = await get_collections_locations()

    logger.info(f"{len(locations)} locations retrieved from API")

    for location in locations:
        location_db = await _handle_location(location)
        if not location_db:
            continue
        try:
            collections: list[CollectionSchema] = location.collections
            tasks = [
                _handle_collection(collection, location_db)
                for collection in collections
            ]
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(
                f"Error while updating collections for location {location.name}: {e}"
            )
            continue

    logger.info(f"{len(locations)} Collections updated")
