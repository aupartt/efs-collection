import asyncio
import logging
import re
from datetime import datetime

import aiohttp
from api_carto_client import Client
from api_carto_client.api.sampling_collection import (
    get_carto_api_v3_samplingcollection_searchbypostcode as api_search_collection,
)
from api_carto_client.models.sampling_collection_result import SamplingCollectionResult
from api_carto_client.models.sampling_location_collections_entity import (
    SamplingLocationCollectionsEntity,
)
from dateutil.relativedelta import relativedelta

from collecte.schemas import (
    CollectionGroupSchema,
    CollectionSchema,
    LocationSchema,
)
from collecte.services.collections import save_location_collections
from collecte.services.locations import get_postal_codes
from collecte.services.utils import check_api, with_api_client

logger = logging.getLogger(__name__)
api_semaphore = asyncio.Semaphore(10)


@with_api_client
async def _retrieve_sampling_collections(
    client: Client, post_code: str
) -> list[SamplingLocationCollectionsEntity]:
    """Retrieve collections from the API"""
    collections: SamplingCollectionResult = await api_search_collection.asyncio(
        client=client,
        post_code=post_code,
        # hide_private_collects=True,
        # hide_non_publiable_collects=True,
        limit=100,
        user_latitude=48,
        user_longitude=-2,
        max_date=datetime.now() + relativedelta(months=+6),
    )
    if not collections:
        return []
    return collections.sampling_location_collections


async def get_esf_id(url: str) -> str | None:
    """Retrieve EFS id from url"""
    if not url:
        return

    async with api_semaphore:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.head(url, allow_redirects=True) as resp:
                    reg = r"trouver-une-collecte/([0-9]+)/"
                    match = re.search(reg, resp.url.raw_path)
                    return match.group(1) if match else None
            except Exception as e:
                logger.error(
                    "Failed to retrieve EFS_ID", extra={"url": url, "error": str(e)}
                )


async def _get_collections_locations() -> list[dict]:
    """Retrieve all collection locations from the API with post_codes and flatten the list"""
    if not await check_api():
        return []

    postal_codes = await get_postal_codes()
    tasks = [
        _retrieve_sampling_collections(postal_code) for postal_code in postal_codes
    ]
    _locations = await asyncio.gather(*tasks)

    locations = [
        collection.to_dict() for sublist in _locations for collection in sublist
    ]

    return locations


async def _handle_location(location: LocationSchema) -> None:
    """Handle a single location and filter collections without urls"""

    async def _add_efs_id(collection: CollectionSchema) -> CollectionSchema | None:
        """Add efs_id to a collection"""
        efs_id = await get_esf_id(collection.url)
        if not efs_id:
            return None
        collection.efs_id = efs_id
        return collection

    tasks = [
        _add_efs_id(collection) for collection in location.collections if collection.url
    ]
    location.collections = await asyncio.gather(*tasks)


async def _transform_location_collections(location: LocationSchema) -> None:
    """Transform collections to group collections"""

    async def _collection_to_group(collection: CollectionSchema) -> None:
        group_collection: CollectionGroupSchema = collection.as_group(from_db=False)
        return group_collection

    tasks = [
        _collection_to_group(collection)
        for collection in location.collections
        if collection
    ]
    location.collections = await asyncio.gather(*tasks)


async def update_collections(locations: list[dict] = None) -> None:
    """Update all collections for all locations"""
    logger.info("Start updating collections...")

    if not locations:
        logger.info("No collections specified, retrieving from API")
        # Get all locations with active collections
        locations = await _get_collections_locations()
        logger.info("Collections retrieved")

    if not locations:
        logger.error("No collections to process")
        return

    locations = [LocationSchema(**location) for location in locations if location]

    logger.info(f"Processing {len(locations)} collections...")

    # Set efs_id for all collections within a location
    tasks = [_handle_location(location) for location in locations]
    await asyncio.gather(*tasks)

    # Transform collections to group collections
    tasks = [
        _transform_location_collections(location) for location in locations if location
    ]
    await asyncio.gather(*tasks)

    # Save all collections to database
    collections, events, snapshots = await save_location_collections(locations)

    logger.info(
        "Successfully processed collections",
        extra={
            "n_collections": collections,
            "n_events": events,
            "n_snapshots": snapshots,
        },
    )
