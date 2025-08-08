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

from collecte.services.utils import (
    api_to_pydantic,
    with_api_client,
    check_api,
)
from collecte.schemas import GroupSchema
from collecte.services import save_groups, load_groups
from collecte.core.settings import settings


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
async def _retrieve_groups(client: Client, region: SamplingRegionEntity) -> list[GroupSchema]:
    """Retrieve groups for a region from API"""
    groups: list[SamplingGroupEntity] = await api_get_groupements.asyncio(
        client=client, region_code=region.code
    )
    return api_to_pydantic(groups, GroupSchema)


async def update_groups() -> None:
    """Retrieve groups from API and add them to database"""
    if not await check_api():
        return

    region: SamplingRegionEntity = await _retrieve_region(settings.REGION_NAME)
    groups: list[GroupSchema] = await _retrieve_groups(region)

    await save_groups(groups)
