from unittest.mock import MagicMock

import pytest
from api_carto_client.models.sampling_location_result import SamplingLocationResult
from pytest_mock import MockerFixture

import collecte.tasks.locations as tasks_locations
from collecte.schemas.location import LocationSchema


@pytest.mark.asyncio
async def test_retrieve_location_sampling(mocker, mock_grp, mock_loc):
    mock_grp_api = mock_grp.api[0]
    mock_sampling_loc_res = SamplingLocationResult(
        sampling_location_entities=mock_loc.api
    )

    mock_api_search_location = mocker.patch(
        "collecte.tasks.locations.api_search_location.asyncio",
        return_value=mock_sampling_loc_res,
    )
    mock_api_to_pydantic = mocker.patch(
        "collecte.tasks.locations.api_to_pydantic", return_value=mock_loc.schemas
    )

    result = await tasks_locations._retrieve_location_sampling(mock_grp_api)

    mock_api_search_location.assert_awaited_with(
        client=mocker.ANY, group_code=mock_grp_api.gr_code
    )
    mock_api_to_pydantic.assert_awaited_with(mock_loc.api, LocationSchema)
    assert result == mock_loc.schemas


@pytest.mark.asyncio
async def test_filter_location_success(mocker: MockerFixture):
    mock_input = MagicMock(spec=LocationSchema, post_code="22", latitude=48, longitude=-2)

    mock_log = mocker.patch.object(tasks_locations.logger, "error")

    result = await tasks_locations._filter_location(mock_input)

    mock_log.assert_not_called()
    assert result == mock_input


@pytest.mark.parametrize("post_code, lat, lng", [["53", 48, -2], ["35", 0, 0], ["35", 48, 0], ["35", 0, -2]])
@pytest.mark.asyncio
async def test_filter_location_error(mocker: MockerFixture, post_code, lat, lng):
    mock_input = MagicMock(spec=LocationSchema, post_code=post_code, latitude=lat, longitude=lng)

    mock_log = mocker.patch.object(tasks_locations.logger, "warning")

    result = await tasks_locations._filter_location(mock_input)

    mock_log.assert_called_once()
    assert result is None


@pytest.mark.asyncio
async def test_update_locations_success(mocker, mock_grp, mock_loc):
    mock_check_api = mocker.patch(
        "collecte.tasks.locations.check_api", return_value=True
    )

    mock_groups = mock_grp.api[:2]
    mock__locations = [mock_loc.schemas[:2], mock_loc.schemas[2:]]
    mock_locations = mock_loc.schemas

    # Retrieve locations
    mock_load_groups = mocker.patch(
        "collecte.tasks.locations.load_groups", return_value=mock_groups
    )
    mocker.patch(
        "collecte.tasks.locations._retrieve_location_sampling",
        side_effect=mock__locations,
    )

    # Save locations
    mock_save_locations = mocker.patch(
        "collecte.tasks.locations.save_locations", return_value=mock_locations
    )

    await tasks_locations.update_locations()

    mock_check_api.assert_awaited()
    mock_load_groups.assert_awaited()
    mock_save_locations.assert_awaited_with(mock_locations)


@pytest.mark.asyncio
async def test_update_locations_api_check_fails(mocker):
    mock_check_api = mocker.patch(
        "collecte.tasks.locations.check_api", return_value=False
    )
    mock_load_groups = mocker.patch("collecte.tasks.locations.load_groups")
    mock_save_locations = mocker.patch("collecte.tasks.locations.save_locations")

    await tasks_locations.update_locations()

    mock_check_api.assert_awaited()
    mock_load_groups.assert_not_awaited()
    mock_save_locations.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_locations_empty_groups(mocker):
    mock_check_api = mocker.patch(
        "collecte.tasks.locations.check_api", return_value=True
    )

    mock_groups = []
    mock__locations = []

    mock_load_groups = mocker.patch(
        "collecte.tasks.locations.load_groups", return_value=mock_groups
    )
    mock_save_locations = mocker.patch(
        "collecte.tasks.locations.save_locations", return_value=mock__locations
    )
    mock_log = mocker.patch.object(tasks_locations.logger, "error")

    await tasks_locations.update_locations()

    mock_log.assert_called_once()
    mock_check_api.assert_awaited()
    mock_load_groups.assert_awaited()
    mock_save_locations.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_locations_no_locations_found(mocker, mock_grp):
    mock_check_api = mocker.patch(
        "collecte.tasks.locations.check_api", return_value=True
    )

    mock_groups = mock_grp.api
    mock__locations = []
    mock_locations = []

    mock_load_groups = mocker.patch(
        "collecte.tasks.locations.load_groups", return_value=mock_groups
    )
    mocker.patch(
        "collecte.tasks.locations._retrieve_location_sampling",
        return_value=mock__locations,
    )
    mock_save_locations = mocker.patch(
        "collecte.tasks.locations.save_locations", return_value=mock_locations
    )
    mock_log = mocker.patch.object(tasks_locations.logger, "error")

    await tasks_locations.update_locations()

    mock_log.assert_called_once()
    mock_check_api.assert_awaited()
    mock_load_groups.assert_awaited()
    mock_save_locations.assert_not_awaited()
