import pytest
from api_carto_client.models.sampling_region_entity import SamplingRegionEntity

import collecte.tasks.groups as tasks_groups
from collecte.schemas.group import GroupSchema


@pytest.fixture
def mock_regions():
    return [
        SamplingRegionEntity(code="1", libelle="Corse"),
        SamplingRegionEntity(code="2", libelle="Bretagne"),
        SamplingRegionEntity(code="3", libelle="Loire-Atlantique"),
    ]


@pytest.mark.asyncio
async def test_retrieve_region_found(mocker, mock_regions):
    mock_api_get_regions = mocker.patch(
        "collecte.tasks.groups.api_get_regions.asyncio", return_value=mock_regions
    )

    result = await tasks_groups._retrieve_region("Bretagne")

    mock_api_get_regions.assert_awaited()
    assert result == mock_regions[1]


@pytest.mark.asyncio
async def test_retrieve_region_not_found(mocker, mock_regions):
    mock_api_get_regions = mocker.patch(
        "collecte.tasks.groups.api_get_regions.asyncio", return_value=mock_regions
    )

    result = await tasks_groups._retrieve_region("Centre-Val de Loire")

    mock_api_get_regions.assert_awaited()
    assert result is None


@pytest.mark.asyncio
async def test_retrieve_groups(mocker, mock_regions, mock_grp):
    mock_api_get_groupements = mocker.patch(
        "collecte.tasks.groups.api_get_groupements.asyncio",
        return_value=mock_grp.api,
    )
    mock_api_to_pydantic = mocker.patch(
        "collecte.tasks.groups.api_to_pydantic", return_value=mock_grp.schemas
    )

    region = mock_regions[1]
    result = await tasks_groups._retrieve_groups(region)

    mock_api_get_groupements.assert_awaited_with(
        client=mocker.ANY, region_code=region.code
    )
    mock_api_to_pydantic.assert_awaited_with(mock_grp.api, GroupSchema)
    assert result == mock_grp.schemas


@pytest.mark.asyncio
async def test_update_groups_success(mocker, mock_regions, mock_grp):
    mock_region = mock_regions[1]

    mock_check_api = mocker.patch("collecte.tasks.groups.check_api", return_value=True)
    mock_retrieve_region = mocker.patch(
        "collecte.tasks.groups._retrieve_region", return_value=mock_region
    )
    mock_retrieve_groups = mocker.patch(
        "collecte.tasks.groups._retrieve_groups", return_value=mock_grp.schemas
    )
    mock_save_groups = mocker.patch("collecte.tasks.groups.save_groups")
    mock_settings = mocker.patch("collecte.tasks.groups.settings")
    mock_settings.REGION_NAME = mock_region.libelle
    mock_log = mocker.patch.object(tasks_groups.logger, "info")

    await tasks_groups.update_groups()

    mock_check_api.assert_awaited()
    mock_retrieve_region.assert_awaited_with(mock_region.libelle)
    mock_retrieve_groups.assert_awaited_with(mock_region)
    mock_save_groups.assert_awaited_with(mock_grp.schemas)
    assert mock_log.call_count == 3


@pytest.mark.asyncio
async def test_update_groups_api_check_fails(mocker):
    mock_check_api = mocker.patch("collecte.tasks.groups.check_api", return_value=False)
    mock_retrieve_region = mocker.patch("collecte.tasks.groups._retrieve_region")
    mock_retrieve_groups = mocker.patch("collecte.tasks.groups._retrieve_groups")
    mock_save_groups = mocker.patch("collecte.tasks.groups.save_groups")

    await tasks_groups.update_groups()

    mock_check_api.assert_awaited()
    mock_retrieve_region.assert_not_awaited()
    mock_retrieve_groups.assert_not_awaited()
    mock_save_groups.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_groups_empty_groups(mocker, mock_regions):
    mock_region = mock_regions[1]
    empty_groups = []

    mock_check_api = mocker.patch("collecte.tasks.groups.check_api", return_value=True)
    mock_retrieve_region = mocker.patch(
        "collecte.tasks.groups._retrieve_region", return_value=mock_region
    )
    mock_retrieve_groups = mocker.patch(
        "collecte.tasks.groups._retrieve_groups", return_value=empty_groups
    )
    mock_save_groups = mocker.patch("collecte.tasks.groups.save_groups")
    mock_settings = mocker.patch("collecte.tasks.groups.settings")
    mock_settings.REGION_NAME = mock_region.libelle
    mock_log = mocker.patch.object(tasks_groups.logger, "error")

    await tasks_groups.update_groups()

    mock_check_api.assert_awaited()
    mock_log.assert_called_once()
    mock_retrieve_region.assert_awaited_with(mock_region.libelle)
    mock_retrieve_groups.assert_awaited_with(mock_region)
    mock_save_groups.assert_not_called()
