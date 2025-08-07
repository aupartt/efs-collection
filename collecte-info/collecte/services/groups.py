import logging

from api_carto_client import Client
from api_carto_client.models.sampling_region_entity import SamplingRegionEntity
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getregions as api_get_regions,
)
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getgroupements as api_get_groupements,
)
from sqlalchemy import select

from collecte.services.utils import api_to_pydantic, update_all, with_api_client, check_api
from collecte.core.database import get_db
from collecte.models import GroupModel
from collecte.schemas import GroupSchema


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGION_NAME = "Bretagne"


@with_api_client
def _retrieve_region(client: Client, name: str) -> SamplingRegionEntity:
    """Retrieve region from API"""
    regions: list[SamplingRegionEntity] = api_get_regions.sync(client=client)
    for region in regions:
        if region.libelle == name:
            return region
    return None


@with_api_client
def _retrieve_groups(client: Client, region: SamplingRegionEntity) -> list[GroupSchema]:
    """Retrieve groups for a region from API"""
    groups: list[SamplingGroupEntity] = api_get_groupements.sync(
        client=client, region_code=region.code
    )
    return api_to_pydantic(groups, GroupSchema)


async def get_groups() -> list[GroupSchema]:
    """Return all groups from database"""
    async with get_db() as session:
        results = await session.execute(select(GroupModel))
        groups = results.scalars().all()

        return [GroupSchema.model_validate(group) for group in groups] if groups else []


async def set_groups() -> None:
    """Retrieve groups from API and add them to database"""
    if not check_api():
        return

    region: SamplingRegionEntity = _retrieve_region(REGION_NAME)
    groups: list[GroupSchema] = _retrieve_groups(region)

    await update_all(groups, GroupModel)
