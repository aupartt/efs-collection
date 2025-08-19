from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.services.groups as group_services
from collecte.models.group import GroupModel
from collecte.schemas.group import GroupSchema


@pytest.mark.asyncio
async def test_load_groups(mocker, async_cm, mock_grp):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalars.return_value.all.return_value = mock_grp.models
    mock_session.execute.return_value = mock_results

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(mock_session))
    mocker.patch(
        "collecte.services.locations.sqlalchemy_to_pydantic",
        return_value=mock_grp.schemas,
    )

    result = await group_services.load_groups()

    mock_session.execute.assert_awaited()
    assert result == mock_grp.schemas


@pytest.mark.asyncio
async def test_get_group_found(mock_grp):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = mock_grp.models[1]
    mock_session.execute.return_value = mock_results

    result = await group_services.get_group(mock_session, "ABC123")

    mock_session.execute.assert_awaited()
    assert result == mock_grp.models[1]


@pytest.mark.asyncio
async def test_add_group_new(mocker, async_cm, mock_grp):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_results

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(mock_session))

    group_services.get_db.return_value.__aenter__.return_value = mock_session

    result = await group_services.add_group(mock_grp.schemas[0])

    mock_session.add.assert_called()
    mock_session.commit.assert_awaited()
    mock_session.refresh.assert_awaited()
    assert isinstance(result, GroupModel)


@pytest.mark.asyncio
async def test_add_group_existing(mocker, async_cm):
    existing_group = GroupModel(gr_code="F00004", gr_lib="Old", gr_desd="Old")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_results = MagicMock()
    mock_results.scalar_one_or_none.return_value = existing_group
    mock_session.execute.return_value = mock_results

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(mock_session))

    new_group = GroupSchema(gr_code="F00004", gr_lib="New", gr_desd="New")
    result = await group_services.add_group(new_group)

    assert existing_group.gr_lib == "New"
    mock_session.commit.assert_awaited()
    mock_session.refresh.assert_awaited()
    assert result is existing_group


@pytest.mark.asyncio
async def test_add_group_exception(mocker, async_cm):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.side_effect = Exception("DB error")
    mock_group = GroupSchema(gr_code="F00004", gr_lib="Old", gr_desd="Old")

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(mock_session))

    mock_log = mocker.patch.object(group_services.logger, "error")
    result = await group_services.add_group(mock_group)
    assert result is None
    mock_session.rollback.assert_awaited()
    mock_log.assert_called_once()


@pytest.mark.asyncio
async def test_save_groups(mocker, async_cm, mock_grp):
    mocker.patch("collecte.services.groups.add_group", return_value=async_cm("added"))

    await group_services.save_groups(mock_grp.schemas)

    assert group_services.add_group.await_count == len(mock_grp.schemas)
