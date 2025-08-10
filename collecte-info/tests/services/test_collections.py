import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.services.collections as collection_services
from collecte.schemas.collection import (
    CollectionGroupSchema,
)


@pytest.mark.asyncio
async def test_load_collection_groups(mocker, async_cm, mock_grp_col):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalars.return_value.all.return_value = mock_grp_col.models
    mock_session.execute.return_value = mock_results

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch(
        "collecte.services.collections.sqlalchemy_to_pydantic",
        return_value=mock_grp_col.schemas,
    )

    result = await collection_services.load_collection_groups()

    mock_session.execute.assert_awaited()
    collection_services.sqlalchemy_to_pydantic.assert_called_once_with(
        mock_grp_col.models, CollectionGroupSchema
    )
    assert result == mock_grp_col.schemas


@pytest.mark.asyncio
async def test_get_collection_found(mock_grp_col):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = mock_grp_col.models[0]
    mock_session.execute.return_value = mock_results

    result = await collection_services.get_collection(
        mock_session, mock_grp_col.schemas[0]
    )

    mock_session.execute.assert_awaited()
    assert result == mock_grp_col.models[0]


@pytest.mark.asyncio
async def test_get_collection_not_found(mock_grp_col):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_results

    result = await collection_services.get_collection(
        mock_session, mock_grp_col.schemas[0]
    )

    mock_session.execute.assert_awaited()
    assert result is None


@pytest.mark.asyncio
async def test_get_event_found(mock_evt_col):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = mock_evt_col.models[0]
    mock_session.execute.return_value = mock_results

    result = await collection_services.get_event(mock_session, 101)

    mock_session.execute.assert_awaited()
    assert result == mock_evt_col.models[0]


@pytest.mark.asyncio
async def test_get_event_not_found():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_results

    result = await collection_services.get_event(mock_session, 404)

    mock_session.execute.assert_awaited()
    assert result is None


@pytest.mark.asyncio
async def test_handle_location_found(mocker, async_cm, mock_loc, mock_grp_col):
    mock_session = AsyncMock(spec=AsyncSession)
    location = mock_loc.schemas[0]
    location.collections = mock_grp_col.schemas

    location_db = mock_loc.models[0]
    location_db.id = 101

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch("collecte.services.collections.get_location", return_value=location_db)

    result = await collection_services._handle_location(location)

    assert len(result) == 1
    assert result[0].location_id == location_db.id


@pytest.mark.asyncio
async def test_handle_location_not_found(mocker, async_cm, mock_loc_col):
    mock_session = AsyncMock(spec=AsyncSession)

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch("collecte.services.collections.get_location", return_value=None)
    mock_log = mocker.patch.object(collection_services.logger, "warning")

    result = await collection_services._handle_location(mock_loc_col.schemas[0])

    mock_log.assert_called_once()
    assert result is None


@pytest.mark.asyncio
async def test_handle_collection_new(mocker, async_cm, mock_grp_col):
    mock_session = AsyncMock(spec=AsyncSession)

    collection = mock_grp_col.schemas[0]
    collection.efs_id = "foo"

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch("collecte.services.collections.get_collection", return_value=None)

    result = await collection_services._handle_collection(collection)

    mock_session.add.assert_called()
    mock_session.commit.assert_awaited()
    assert result is None


@pytest.mark.asyncio
async def test_handle_collection_existing(mocker, async_cm, mock_grp_col):
    mock_session = AsyncMock(spec=AsyncSession)

    collection_input = mock_grp_col.schemas[0]
    collection_input.efs_id = "foo"
    collection_check = collection_input.copy()
    collection_check.update_ids("1337")

    collection_db = mock_grp_col.models[0]
    collection_db.id = "1337"

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch(
        "collecte.services.collections.get_collection", return_value=collection_db
    )

    result = await collection_services._handle_collection(collection_input)

    mock_session.commit.assert_awaited()
    assert result == (collection_check.events, collection_check.snapshots)


@pytest.mark.asyncio
async def test_handle_collection_no_efs_id(mocker, async_cm, mock_grp_col):
    mocker.patch("collecte.services.collections.get_db", return_value=async_cm(None))
    mock_log = mocker.patch.object(collection_services.logger, "warning")

    result = await collection_services._handle_collection(mock_grp_col.schemas[0])

    mock_log.assert_called_once()
    assert result is None


@pytest.mark.asyncio
async def test_handle_event_new(mocker, async_cm, mock_evt_col):
    mock_session = AsyncMock(spec=AsyncSession)

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch("collecte.services.collections.get_event", return_value=None)

    result = await collection_services._handle_event(mock_evt_col.schemas[0])

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited()
    assert result


@pytest.mark.asyncio
async def test_handle_event_existing(mocker, async_cm, mock_evt_col):
    mock_session = AsyncMock(spec=AsyncSession)

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )
    mocker.patch(
        "collecte.services.collections.get_event", return_value=mock_evt_col.models[0]
    )

    result = await collection_services._handle_event(mock_evt_col.schemas[0])

    mock_session.add.assert_not_called()
    mock_session.commit.assert_awaited()
    assert result == mock_evt_col.models[0]


@pytest.mark.asyncio
async def test_handle_snapshot(mocker, async_cm, mock_snap_col):
    mock_session = AsyncMock(spec=AsyncSession)

    mocker.patch(
        "collecte.services.collections.get_db", return_value=async_cm(mock_session)
    )

    result = await collection_services._handle_snapshot(mock_snap_col.schemas[0])

    mock_session.add.assert_called()
    mock_session.commit.assert_awaited()
    assert result


@pytest.mark.asyncio
async def test_save_location_collections_success(
    mocker, mock_loc_col, mock_grp_col, mock_evt_col, mock_snap_col
):
    async def mock_handle_location(location):
        return [mock_grp_col.schemas[0]]

    async def mock_handle_collection(collection):
        return (
            [mock_evt_col.schemas[0], mock_evt_col.schemas[0]],
            [mock_snap_col.schemas[0]],
        )

    async def mock_handle_event(event):
        return event

    async def mock_handle_snapshot(snapshot):
        return snapshot

    mocker.patch(
        "collecte.services.collections._handle_location",
        side_effect=mock_handle_location,
    )
    mocker.patch(
        "collecte.services.collections._handle_collection",
        side_effect=mock_handle_collection,
    )
    mocker.patch(
        "collecte.services.collections._handle_event", side_effect=mock_handle_event
    )
    mocker.patch(
        "collecte.services.collections._handle_snapshot",
        side_effect=mock_handle_snapshot,
    )

    result = await collection_services.save_location_collections(
        [mock_loc_col.schemas[0]]
    )

    assert result == (1, 2, 1)


@pytest.mark.asyncio
async def test_save_location_collections_with_none_results(
    mocker,
    mock_loc_col,
):
    mocker.patch("collecte.services.collections._handle_location", return_value=None)

    result = await collection_services.save_location_collections(
        [mock_loc_col.schemas[0]]
    )

    assert result == (0, 0, 0)
