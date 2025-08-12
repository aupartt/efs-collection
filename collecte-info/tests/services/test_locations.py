from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.services.locations as location_services
from collecte.models.location import LocationModel
from collecte.schemas.location import LocationSchema


@pytest.mark.asyncio
async def test_load_locations(mocker, async_cm, mock_loc):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalars.return_value.all.return_value = mock_loc.models
    mock_session.execute.return_value = mock_results

    mocker.patch(
        "collecte.services.locations.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch(
        "collecte.services.locations.sqlalchemy_to_pydantic",
        return_value=mock_loc.schemas,
    )

    result = await location_services.load_locations()

    mock_session.execute.assert_awaited()
    location_services.sqlalchemy_to_pydantic.assert_awaited_once_with(
        mock_loc.models, LocationSchema
    )
    assert result == mock_loc.schemas


@pytest.mark.asyncio
async def test_get_postal_codes(mocker, async_cm):
    expected_postal_codes = ["29200", "29000", "35000"]
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalars.return_value.all.return_value = expected_postal_codes
    mock_session.execute.return_value = mock_results

    mocker.patch(
        "collecte.services.locations.get_db", return_value=async_cm(mock_session)
    )

    result = await location_services.get_postal_codes()

    mock_session.execute.assert_awaited()
    assert result == expected_postal_codes


@pytest.mark.asyncio
async def test_get_location_found(mock_loc):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = mock_loc.models[0]
    mock_session.execute.return_value = mock_results

    result = await location_services.get_location(mock_session, mock_loc.schemas[0])

    mock_session.execute.assert_awaited_once()
    assert result == mock_loc.models[0]


@pytest.mark.asyncio
async def test_get_location_not_found(mock_loc):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_results

    result = await location_services.get_location(mock_session, mock_loc.schemas[0])

    mock_session.execute.assert_awaited()
    assert result is None


@pytest.mark.asyncio
async def test_add_location_new(mocker, async_cm, mock_loc):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = None  # Location doesn't exist
    mock_session.execute.return_value = mock_results

    # Mock group exists
    mock_group = MagicMock()
    mocker.patch("collecte.services.locations.get_group", return_value=mock_group)
    mocker.patch(
        "collecte.services.locations.get_db", return_value=async_cm(mock_session)
    )

    result = await location_services.add_location(mock_loc.schemas[0])

    mock_session.add.assert_called()
    mock_session.commit.assert_awaited()
    mock_session.refresh.assert_awaited()
    assert isinstance(result, LocationModel)


@pytest.mark.asyncio
async def test_add_location_existing(mocker, async_cm, mock_loc):
    existing_location = mock_loc.models[0]
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = existing_location
    mock_session.execute.return_value = mock_results

    mocker.patch(
        "collecte.services.locations.get_db", return_value=async_cm(mock_session)
    )

    result = await location_services.add_location(mock_loc.schemas[0])

    mock_session.add.assert_not_called()
    mock_session.commit.assert_awaited()
    assert result is existing_location


@pytest.mark.asyncio
async def test_add_location_group_not_exists(mocker, async_cm, mock_loc):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = None  # Location doesn't exist
    mock_session.execute.return_value = mock_results

    # Mock group doesn't exist
    mocker.patch("collecte.services.locations.get_group", return_value=None)
    mocker.patch(
        "collecte.services.locations.get_db", return_value=async_cm(mock_session)
    )
    mock_log = mocker.patch.object(location_services.logger, "warning")

    result = await location_services.add_location(mock_loc.schemas[0])

    mock_log.assert_called_once()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_awaited()
    assert result is None


@pytest.mark.asyncio
async def test_add_location_exception(mocker, async_cm, mock_loc):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.side_effect = Exception("DB error")

    mocker.patch(
        "collecte.services.locations.get_db", return_value=async_cm(mock_session)
    )
    mock_log = mocker.patch.object(location_services.logger, "error")

    result = await location_services.add_location(mock_loc.schemas[0])

    assert result is None
    mock_session.rollback.assert_awaited()
    mock_log.assert_called_once()


@pytest.mark.asyncio
async def test_save_locations(mocker, mock_loc):
    mock_results = mock_loc.models

    async def mock_add_location(location):
        index = mock_loc.schemas.index(location)
        return mock_results[index]

    mocker.patch(
        "collecte.services.locations.add_location", side_effect=mock_add_location
    )

    result = await location_services.save_locations(mock_loc.schemas)

    assert result == mock_results


@pytest.mark.asyncio
async def test_save_locations_with_failures(mocker, mock_loc):
    # Mock some successful and some failed additions
    mock_results = [mock_loc.models[0], None, mock_loc.models[2]]

    async def mock_add_location(location):
        index = mock_loc.schemas.index(location)
        return mock_results[index]

    mocker.patch(
        "collecte.services.locations.add_location", side_effect=mock_add_location
    )

    result = await location_services.save_locations(mock_loc.schemas)

    assert result == mock_results
    assert result[1] is None  # Second location failed
