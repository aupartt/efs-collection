import logging

from api_carto_client import Client
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getgroupements as api_get_groupements,
)
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getregions as api_get_regions,
)
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.models.sampling_region_entity import SamplingRegionEntity

from collecte.core.settings import settings
from collecte.schemas import GroupSchema
from collecte.services.groups import save_groups
from collecte.services.utils import (
    api_to_pydantic,
    check_api,
    with_api_client,
)

logger = logging.getLogger(__name__)


@with_api_client
async def _retrieve_region(client: Client, name: str) -> SamplingRegionEntity:
    """Retrieve region from API"""
    regions: list[SamplingRegionEntity] = await api_get_regions.asyncio(client=client)
    for region in regions:
        if region.libelle == name:
            return region
    return None


@with_api_client
async def _retrieve_groups(
    client: Client, region: SamplingRegionEntity
) -> list[GroupSchema]:
    """Retrieve groups for a region from API"""
    groups: list[SamplingGroupEntity] = await api_get_groupements.asyncio(
        client=client, region_code=region.code
    )
    return await api_to_pydantic(groups, GroupSchema)


async def update_groups(groups: list[GroupSchema] = None) -> None:
    """Retrieve groups from API and add them to database"""
    logger.info("Start updating groups...")

    if not groups:
        logger.info("No groups specified, retrieving from API...")
        if not await check_api():
            return
        region: SamplingRegionEntity = await _retrieve_region(settings.REGION_NAME)
        groups: list[GroupSchema] = await _retrieve_groups(region)
        logger.info("Groups retrieved.")

    if not groups:
        logger.error("No groups to process")
        return

    logger.info(f"Processing {len(groups)} groups...")

    groups_processed = await save_groups(groups)

    logger.info(f"Processed {len(groups_processed)} groups")
