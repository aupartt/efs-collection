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
    args.file = None
    args.format = None
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


@pytest.mark.asyncio
async def test_cli_file(mocker: MockerFixture, _mock_args):
    _mock_args.schedules = True
    _mock_args.file = "/path/to/data.json"
    mock_file_content = [{"foo": 1, "bar": 2}]

    mock_update_groups = mocker.patch("cli.update_groups")
    mock_update_locations = mocker.patch("cli.update_locations")
    mock_update_collections = mocker.patch("cli.update_collections")
    mock_update_schedules = mocker.patch("cli.update_schedules")
    mock_load_data = mocker.patch("cli.load_data", return_value=mock_file_content)

    await cli(_mock_args)

    mock_update_groups.assert_not_awaited()
    mock_update_locations.assert_not_awaited()
    mock_update_collections.assert_not_awaited()
    mock_update_schedules.assert_awaited_once_with(mock_file_content)
    mock_load_data.assert_called_once_with(_mock_args.file, None)


@pytest.mark.asyncio
async def test_cli_load_data_json(mocker: MockerFixture, _mock_args):
    _mock_args.schedules = True
    _mock_args.file = "/path/to/data.json"
    _mock_args.format = "JSON"
    mock_file_content = [{"foo": 1, "bar": 2}, {"foo": 1, "bar": 2}]
    mock_file_read = '[{"foo": 1, "bar": 2},\n{"foo": 1, "bar": 2}]'

    mock_update_groups = mocker.patch("cli.update_groups")
    mock_update_locations = mocker.patch("cli.update_locations")
    mock_update_collections = mocker.patch("cli.update_collections")
    mock_update_schedules = mocker.patch("cli.update_schedules")
    mock_open = mocker.mock_open(read_data=mock_file_read)
    mocker.patch("cli.open", mock_open)

    await cli(_mock_args)

    mock_update_groups.assert_not_awaited()
    mock_update_locations.assert_not_awaited()
    mock_update_collections.assert_not_awaited()
    mock_update_schedules.assert_awaited_once_with(mock_file_content)
    mock_open.assert_called_once_with(_mock_args.file)


@pytest.mark.asyncio
async def test_cli_load_data_jsonl(mocker: MockerFixture, _mock_args):
    _mock_args.schedules = True
    _mock_args.file = "/path/to/data.json"
    _mock_args.format = "JSONL"
    mock_file_content = [{"foo": 1, "bar": 2}, {"foo": 1, "bar": 2}]
    mock_file_read = '{"foo": 1, "bar": 2}\n{"foo": 1, "bar": 2}'

    mock_update_groups = mocker.patch("cli.update_groups")
    mock_update_locations = mocker.patch("cli.update_locations")
    mock_update_collections = mocker.patch("cli.update_collections")
    mock_update_schedules = mocker.patch("cli.update_schedules")
    mock_open = mocker.mock_open(read_data=mock_file_read)
    mocker.patch("cli.open", mock_open)

    await cli(_mock_args)

    mock_update_groups.assert_not_awaited()
    mock_update_locations.assert_not_awaited()
    mock_update_collections.assert_not_awaited()
    mock_update_schedules.assert_awaited_once_with(mock_file_content)
    mock_open.assert_called_once_with(_mock_args.file)
