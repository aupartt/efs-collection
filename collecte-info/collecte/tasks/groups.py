from api_carto_client import Client
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getgroupements as api_get_groupements,
)
from api_carto_client.api.sampling_location import (
    get_carto_api_v3_samplinglocation_getregions as api_get_regions,
)
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.models.sampling_region_entity import SamplingRegionEntity

from collecte.core.logging import logger
from collecte.core.settings import settings
from collecte.schemas import GroupSchema
from collecte.services.groups import save_groups
from collecte.services.utils import (
    api_to_pydantic,
    check_api,
    with_api_client,
)


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
    if not groups:
        if not await check_api():
            return
        region: SamplingRegionEntity = await _retrieve_region(settings.REGION_NAME)
        groups: list[GroupSchema] = await _retrieve_groups(region)
        logger.info(
            f"{len(groups)} Groups retrieved from API for region {region.libelle}"
        )

    if not groups:
        logger.error("No groups to process.")
        return

    logger.info(f"Start processing {len(groups)} groups.")

    await save_groups(groups)

    logger.info("Groups updated !")
