import logging
from sqlalchemy import select

from api_carto_client import Client
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.models.sampling_location_entity import SamplingLocationEntity
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_searchbygrouplocationcode as api_search_location,
)

from collecte.core.database import get_db
from collecte.models import LocationModel
from collecte.schemas import LocationSchema
from .utils import api_to_pydantic, sqlalchemy_to_pydantic, update_all, with_api_client, check_api
from .groups import get_groups

logger = logging.getLogger(__name__)


@with_api_client
def _retrieve_location_sampling(client: Client, groupement: SamplingGroupEntity):
    """Retrieve all locations from API"""
    res: SamplingLocationEntity = api_search_location.sync(
        client=client, group_code=groupement.gr_code
    )
    return api_to_pydantic(res.sampling_location_entities, LocationSchema)


async def get_locations() -> list[LocationSchema]:
    """Return all location from database"""
    async with get_db() as session:
        results = await session.execute(select(LocationModel))
        locations = results.scalars().all()
        return sqlalchemy_to_pydantic(locations, LocationSchema)


async def set_locations():
    """Retrieve all locations from API and store them in database"""
    logging.basicConfig(level=logging.INFO)

    if not check_api():
        return

    groups = await get_groups()
    locations = []
    for group in groups:
        _locations = _retrieve_location_sampling(groupement=group)
        locations.extend(_locations)

    await update_all(locations, LocationModel)
