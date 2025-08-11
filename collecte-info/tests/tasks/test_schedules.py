import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.tasks.schedules as schedule_tasks
from collecte.models import ScheduleModel
from collecte.schemas import ScheduleSchema


class TestRetrieveActiveCollectionsUrl:
    @pytest.mark.asyncio
    async def test_found(self, mocker, mock_grp_col):
        mock_get_active_collections = mocker.patch(
            "collecte.tasks.schedules.get_active_collections",
            return_value=mock_grp_col.schemas,
        )

        result = await schedule_tasks._retrieve_active_collections_url()

        mock_get_active_collections.assert_called_once()
        assert result == [schema.url for schema in mock_grp_col.schemas]

    @pytest.mark.asyncio
    async def test_not_found(self, mocker, mock_grp_col):
        mock_get_active_collections = mocker.patch(
            "collecte.tasks.schedules.get_active_collections", return_value=[]
        )

        result = await schedule_tasks._retrieve_active_collections_url()

        mock_get_active_collections.assert_called_once()
        assert result == []
