import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.services.groups as group_services
from collecte.models.group import GroupModel
from collecte.schemas.group import GroupSchema


@pytest.fixture
def fake_groups_model():
    return


@pytest.fixture
def fake_groups():
    class main:
        schema = [
            GroupSchema(gr_code="F00004", gr_lib="BREST", gr_desd=None),
            GroupSchema(gr_code="F00005", gr_lib="QUIMPER - MDD", gr_desd=None),
            GroupSchema(gr_code="F00006", gr_lib="RENNES - MDD", gr_desd=None),
        ]

        model = [
            GroupModel(gr_code="F00004", gr_lib="BREST", gr_desd=None),
            GroupModel(gr_code="F00005", gr_lib="QUIMPER - MDD", gr_desd=None),
            GroupModel(gr_code="F00006", gr_lib="RENNES - MDD", gr_desd=None),
        ]

    return main


@pytest.mark.asyncio
async def test_load_groups(mocker, async_cm, fake_groups):
    fake_session = AsyncMock(spec=AsyncSession)
    fake_results = MagicMock()
    fake_results.scalars.return_value.all.return_value = fake_groups.model
    fake_session.execute.return_value = fake_results

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(fake_session))

    result = await group_services.load_groups()

    fake_session.execute.assert_awaited()
    assert result == fake_groups.schema


@pytest.mark.asyncio
async def test_get_group_found(fake_groups):
    fake_session = AsyncMock(spec=AsyncSession)
    fake_results = MagicMock()
    fake_results.scalar_one_or_none.return_value = fake_groups.model[1]
    fake_session.execute.return_value = fake_results

    result = await group_services.get_group(fake_session, "ABC123")

    fake_session.execute.assert_awaited()
    assert result == fake_groups.model[1]


@pytest.mark.asyncio
async def test_add_group_new(mocker, async_cm, fake_groups):
    fake_session = AsyncMock(spec=AsyncSession)
    fake_results = MagicMock()
    fake_results.scalar_one_or_none.return_value = None
    fake_session.execute.return_value = fake_results

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(fake_session))

    group_services.get_db.return_value.__aenter__.return_value = fake_session

    result = await group_services.add_group(fake_groups.schema[0])

    fake_session.add.assert_called()
    fake_session.commit.assert_awaited()
    fake_session.refresh.assert_awaited()
    assert isinstance(result, GroupModel)


@pytest.mark.asyncio
async def test_add_group_existing(mocker, async_cm):
    existing_group = GroupModel(gr_code="F00004", gr_lib="Old", gr_desd="Old")
    fake_session = AsyncMock(spec=AsyncSession)
    fake_results = MagicMock()
    fake_results.scalar_one_or_none.return_value = existing_group
    fake_session.execute.return_value = fake_results

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(fake_session))

    new_group = GroupSchema(gr_code="F00004", gr_lib="New", gr_desd="New")
    result = await group_services.add_group(new_group)

    assert existing_group.gr_lib == "New"
    fake_session.commit.assert_awaited()
    fake_session.refresh.assert_awaited()
    assert result is existing_group


@pytest.mark.asyncio
async def test_add_group_exception(mocker, async_cm):
    fake_session = AsyncMock(spec=AsyncSession)
    fake_session.execute.side_effect = Exception("DB error")
    fake_group = GroupSchema(gr_code="F00004", gr_lib="Old", gr_desd="Old")

    mocker.patch("collecte.services.groups.get_db", return_value=async_cm(fake_session))

    mock_log = mocker.patch.object(group_services.logger, "error")
    result = await group_services.add_group(fake_group)
    assert result is None
    fake_session.rollback.assert_awaited()
    mock_log.assert_called_once()


@pytest.mark.asyncio
async def test_save_groups(mocker, async_cm, fake_groups):
    mocker.patch("collecte.services.groups.add_group", return_value=async_cm("added"))

    await group_services.save_groups(fake_groups.schema)

    assert group_services.add_group.await_count == len(fake_groups.schema)
