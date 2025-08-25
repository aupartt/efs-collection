import asyncio
import logging

from api_carto_client import Client
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_searchbygrouplocationcode as api_search_location,
)
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.models.sampling_location_result import SamplingLocationResult

from collecte.core.settings import settings
from collecte.schemas.location import LocationSchema
from collecte.services.groups import load_groups
from collecte.services.locations import save_locations
from collecte.services.utils import api_to_pydantic, check_api, with_api_client

logger = logging.getLogger(__name__)


@with_api_client
async def _retrieve_location_sampling(
    client: Client, groupement: SamplingGroupEntity
) -> list[LocationSchema]:
    """Retrieve all locations from API"""
    res: SamplingLocationResult = await api_search_location.asyncio(
        client=client, group_code=groupement.gr_code
    )
    return await api_to_pydantic(res.sampling_location_entities, LocationSchema)


async def _filter_location(
    location: LocationSchema,
) -> list[LocationSchema] | None:
    """Run some check on the location to avoid bad data"""
    if location.post_code and location.post_code[:2] not in ["22", "29", "35", "56", ""]:
        logger.warning(
            f"Bad post_code {location.info()}"
        )
        return None
    if not all(
        [
            settings.MIN_LAT < location.latitude < settings.MAX_LAT,
            settings.MIN_LNG < location.longitude < settings.MAX_LNG,
        ]
    ):
        logger.warning(
            f"Bad LAT / LNG {location.info()}: lat={location.latitude}, lng={location.longitude}"
        )
        return None

    return location


async def update_locations(locations: list[LocationSchema] = None) -> None:
    """Retrieve all locations from API and store them in database"""
    logger.info("Start updating locations...")

    if not locations:
        logger.info("No locations specified, retrieving from API...")
        if not await check_api():
            return
        # Retrieve locations
        groups = await load_groups()
        tasks = [_retrieve_location_sampling(groupement=group) for group in groups]
        _locations = await asyncio.gather(*tasks)
        locations = [location for sublist in _locations for location in sublist]
        logger.info("Locations retrieved.")

    if not locations:
        logger.error("No locations to process.")
        return

    logger.info(f"Checking {len(locations)} locations...")

    tasks = [_filter_location(location) for location in locations]
    results = [item for item in await asyncio.gather(*tasks) if item]

    logger.info(f"Checks complete, processing  {len(results)} locations...")

    # Save locations
    added_locations = await save_locations(results)

    logger.info(f"Processed {len(added_locations)} collections")
