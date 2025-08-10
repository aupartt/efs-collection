import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.services.schedules as schedule_services
from collecte.models.group import GroupModel
from collecte.schemas.group import GroupSchema


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

