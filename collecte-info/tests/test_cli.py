from argparse import Namespace
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from cli import main as cli


@pytest.fixture
def _mock_args():
    args = MagicMock(spec=Namespace)
    args.groups = False
    args.locations = False
    args.collections = False
    args.schedules = False
    return args


@pytest.mark.asyncio
async def test_cli_groups(mocker: MockerFixture, _mock_args):
    _mock_args.groups = True

    mock_update_groups = mocker.patch("cli.update_groups")
    mock_update_locations = mocker.patch("cli.update_locations")
    mock_update_collections = mocker.patch("cli.update_collections")
    mock_update_schedules = mocker.patch("cli.update_schedules")

    await cli(_mock_args)

    mock_update_groups.assert_awaited_once()
    mock_update_locations.assert_not_awaited()
    mock_update_collections.assert_not_awaited()
    mock_update_schedules.assert_not_awaited()


@pytest.mark.asyncio
async def test_cli_locations(mocker: MockerFixture, _mock_args):
    _mock_args.locations = True

    mock_update_groups = mocker.patch("cli.update_groups")
    mock_update_locations = mocker.patch("cli.update_locations")
    mock_update_collections = mocker.patch("cli.update_collections")
    mock_update_schedules = mocker.patch("cli.update_schedules")

    await cli(_mock_args)

    mock_update_groups.assert_not_awaited()
    mock_update_locations.assert_awaited_once()
    mock_update_collections.assert_not_awaited()
    mock_update_schedules.assert_not_awaited()


@pytest.mark.asyncio
async def test_cli_collections(mocker: MockerFixture, _mock_args):
    _mock_args.collections = True

    mock_update_groups = mocker.patch("cli.update_groups")
    mock_update_locations = mocker.patch("cli.update_locations")
    mock_update_collections = mocker.patch("cli.update_collections")
    mock_update_schedules = mocker.patch("cli.update_schedules")

    await cli(_mock_args)

    mock_update_groups.assert_not_awaited()
    mock_update_locations.assert_not_awaited()
    mock_update_collections.assert_awaited_once()
    mock_update_schedules.assert_not_awaited()


@pytest.mark.asyncio
async def test_cli_schedules(mocker: MockerFixture, _mock_args):
    _mock_args.schedules = True

    mock_update_groups = mocker.patch("cli.update_groups")
    mock_update_locations = mocker.patch("cli.update_locations")
    mock_update_collections = mocker.patch("cli.update_collections")
    mock_update_schedules = mocker.patch("cli.update_schedules")

    await cli(_mock_args)

    mock_update_groups.assert_not_awaited()
    mock_update_locations.assert_not_awaited()
    mock_update_collections.assert_not_awaited()
    mock_update_schedules.assert_awaited_once()
