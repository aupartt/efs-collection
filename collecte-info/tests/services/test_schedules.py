import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs

import collecte.services.schedules as schedule_services
from collecte.models import ScheduleModel, CollectionEventModel, CollectionGroupModel
from collecte.schemas import ScheduleSchema


class TestLoadSchedules:
    @pytest.mark.asyncio
    async def test_success(self, mocker, async_cm, mock_sch):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_results = MagicMock()
        mock_results.scalars.return_value.all.return_value = mock_sch.models
        mock_session.execute.return_value = mock_results

        mocker.patch(
            "collecte.services.schedules.get_db", return_value=async_cm(mock_session)
        )

        result = await schedule_services.load_schedules()

        mock_session.execute.assert_awaited()
        assert result == mock_sch.schemas

    @pytest.mark.asyncio
    async def test_empty(self, mocker, async_cm):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_results = MagicMock()
        mock_results.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_results

        mocker.patch(
            "collecte.services.schedules.get_db", return_value=async_cm(mock_session)
        )

        result = await schedule_services.load_schedules()

        assert result == []

    @pytest.mark.asyncio
    async def test_excption(self, mocker, async_cm):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("error")

        mocker.patch(
            "collecte.services.schedules.get_db", return_value=async_cm(mock_session)
        )
        mock_log = mocker.patch.object(schedule_services.logger, "error")

        result = await schedule_services.load_schedules()

        mock_log.assert_called_once()
        assert result is None


class TestRetrieveEvents:
    @pytest.mark.asyncio
    async def test_found(self, mocker):
        mock_evt_col_1 = MagicMock(spec=CollectionEventModel, date="date_A")
        mock_evt_col_2 = MagicMock(spec=CollectionEventModel, date="date_A")
        mock_evt_col_3 = MagicMock(spec=CollectionEventModel, date="date_B")

        # Créez le mock de la collection principale
        mock_grp_col = MagicMock(
            spec=CollectionGroupModel,
            events=[mock_evt_col_1, mock_evt_col_2, mock_evt_col_3],
        )

        # Méthode 1: Utiliser une coroutine directe (simple)
        async def mock_events_property():
            return None

        awaitable_attrs_mock = MagicMock()
        awaitable_attrs_mock.events = mock_events_property()
        mock_grp_col.awaitable_attrs = awaitable_attrs_mock

        mock_schedule = MagicMock(spec=ScheduleSchema, date="date_A", efs_id="1337")

        mocker.patch("collecte.services.schedules.CollectionEventSchema")
        mocker.patch("collecte.services.schedules.get_db")
        mock_get_collection = mocker.patch(
            "collecte.services.schedules.get_collection",
            return_value=mock_grp_col,
        )

        result = await schedule_services.retrieve_events(mock_schedule)

        mock_get_collection.assert_awaited_once_with(mocker.ANY, "1337")
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_not_found(self, mocker, mock_sch):
        mock_schedule = MagicMock(sepc=ScheduleSchema)
        mock_schedule.efs_id = "1337"

        mocker.patch("collecte.services.schedules.get_db")
        mock_get_collection = mocker.patch(
            "collecte.services.schedules.get_collection", return_value=None
        )
        mock_log = mocker.patch.object(schedule_services.logger, "warning")

        result = await schedule_services.retrieve_events(mock_schedule)

        mock_get_collection.assert_awaited_once_with(mocker.ANY, "1337")
        mock_log.assert_called_once()
        mock_schedule.info.assert_called_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_exception(self, mocker):
        mock_schedule = MagicMock(spec=ScheduleSchema, efs_id="1337")

        mocker.patch("collecte.services.schedules.get_db")
        mock_get_collection = mocker.patch(
            "collecte.services.schedules.get_collection", side_effect=Exception("error")
        )
        mock_log = mocker.patch.object(schedule_services.logger, "error")

        result = await schedule_services.retrieve_events(mock_schedule)

        mock_get_collection.assert_awaited_once_with(mocker.ANY, mock_schedule.efs_id)
        mock_log.assert_called_once()
        assert result is None


class TestAddSchedule:
    @pytest.mark.asyncio
    async def test_success(self, mocker, async_cm, mock_sch):
        mock_session = AsyncMock(spec=AsyncSession)

        mocker.patch(
            "collecte.services.schedules.get_db", return_value=async_cm(mock_session)
        )

        result = await schedule_services.add_schedule(mock_sch.schemas[0])

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert isinstance(result, ScheduleModel)

    @pytest.mark.asyncio
    async def test_exception(self, mocker, async_cm, mock_sch):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit.side_effect = Exception("error")

        mocker.patch(
            "collecte.services.schedules.get_db", return_value=async_cm(mock_session)
        )
        mock_log = mocker.patch.object(schedule_services.logger, "error")

        result = await schedule_services.add_schedule(mock_sch.schemas[0])

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_not_called()
        mock_log.assert_called_once()
        assert result is None
