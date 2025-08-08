import logging
import asyncio

from api_carto_client import Client
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.models.sampling_location_entity import SamplingLocationEntity
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_searchbygrouplocationcode as api_search_location,
)

from collecte.schemas.location import LocationSchema
from collecte.services.utils import api_to_pydantic, with_api_client, check_api
from collecte.services import load_groups, save_locations

logger = logging.getLogger(__name__)


@with_api_client
async def _retrieve_location_sampling(
    client: Client, groupement: SamplingGroupEntity
) -> list[LocationSchema]:
    """Retrieve all locations from API"""
    res: SamplingLocationEntity = await api_search_location.asyncio(
        client=client, group_code=groupement.gr_code
    )
    return await api_to_pydantic(res.sampling_location_entities, LocationSchema)


async def update_locations():
    """Retrieve all locations from API and store them in database"""
    if not await check_api():
        return

    groups = await load_groups()
    tasks = [_retrieve_location_sampling(groupement=group) for group in groups]
    _locations = await asyncio.gather(*tasks)
    locations = [location for sublist in _locations for location in sublist]

    await save_locations(locations)
