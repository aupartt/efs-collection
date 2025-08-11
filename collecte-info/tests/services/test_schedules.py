import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.services.schedules as schedule_services
from collecte.models import ScheduleModel
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
    async def test_found(self, mocker, mock_grp_col, mock_sch):
        mock_schedule = mock_sch.schemas[0]
        mock_schedule.efs_id = "1337"

        mocker.patch("collecte.services.schedules.get_db")
        mock_get_collection = mocker.patch(
            "collecte.services.schedules.get_collection",
            return_value=mock_grp_col.models[0],
        )

        result = await schedule_services._retrieve_events(mock_schedule)

        mock_get_collection.assert_awaited_once_with(mocker.ANY, "1337")
        assert result == mock_grp_col.models[0].events

    @pytest.mark.asyncio
    async def test_not_found(self, mocker, mock_sch):
        mock_schedule = MagicMock(sepc=ScheduleSchema)
        mock_schedule.efs_id = "1337"

        mocker.patch("collecte.services.schedules.get_db")
        mock_get_collection = mocker.patch(
            "collecte.services.schedules.get_collection", return_value=None
        )
        mock_log = mocker.patch.object(schedule_services.logger, "warning")

        result = await schedule_services._retrieve_events(mock_schedule)

        mock_get_collection.assert_awaited_once_with(mocker.ANY, "1337")
        mock_log.assert_called_once()
        mock_schedule.info.assert_called_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_exception(self, mocker, mock_sch):
        mock_schedule = mock_sch.schemas[0]
        mock_schedule.efs_id = "1337"

        mocker.patch("collecte.services.schedules.get_db")
        mock_get_collection = mocker.patch(
            "collecte.services.schedules.get_collection", side_effect=Exception("error")
        )
        mock_log = mocker.patch.object(schedule_services.logger, "error")

        result = await schedule_services._retrieve_events(mock_schedule)

        mock_get_collection.assert_awaited_once_with(mocker.ANY, mock_schedule.efs_id)
        mock_log.assert_called_once()
        assert result is None
