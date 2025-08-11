import pytest
from datetime import time
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.tasks.schedules as schedule_tasks
from collecte.models import ScheduleModel
from collecte.schemas import ScheduleSchema, CollectionEventSchema


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


class TestGetSchedulesFromCrawler:
    # Need to addapt the crawler first
    pass


class TestMatchEvent:
    timetables_count_morning = 4
    timetables_count_afternoon = 5
    timetables_count_total = timetables_count_morning + timetables_count_afternoon

    @pytest.fixture
    def _mock_schedule(self, mock_sch):
        mock_schedule = mock_sch.schemas[0]
        morning = {
            time(9): 1,
            time(10): 2,
            time(11): 1,
            time(13): 0,
        }
        afternoon = {
            time(14): 1,
            time(15): 2,
            time(16): 1,
            time(17): 0,
            time(18): 1,
        }
        mock_schedule.timetables = morning | afternoon
        return mock_schedule

    @pytest.fixture
    def _mock_event(self, mock_evt_col):
        def _make(
            start_morning: bool,
            end_morning: bool,
            start_afternoon: bool,
            end_afternoon: bool,
        ) -> CollectionEventSchema:
            mock_event = mock_evt_col.schemas[0]
            mock_event.morning_start_time = None
            mock_event.morning_end_time = None
            mock_event.afternoon_start_time = None
            mock_event.afternoon_end_time = None

            if start_morning:
                mock_event.morning_start_time = time(8)
            if end_morning:
                mock_event.morning_end_time = time(13)
            if start_afternoon:
                mock_event.afternoon_start_time = time(14)
            if end_afternoon:
                mock_event.afternoon_end_time = time(19)

            return mock_event

        return _make

    @pytest.mark.asyncio
    async def test_match_all(self, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(True, True, True, True)

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        assert isinstance(result, ScheduleSchema)
        assert result.total_slots == self.timetables_count_total

    @pytest.mark.asyncio
    async def test_match_morning(self, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(True, True, False, False)

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        assert isinstance(result, ScheduleSchema)
        assert result.total_slots == self.timetables_count_morning

    @pytest.mark.asyncio
    async def test_match_afternoon(self, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(False, False, True, True)

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        assert isinstance(result, ScheduleSchema)
        assert result.total_slots == self.timetables_count_afternoon

    @pytest.mark.asyncio
    async def test_match_start_end(self, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(True, False, False, True)

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        assert isinstance(result, ScheduleSchema)
        assert result.total_slots == self.timetables_count_total


    @pytest.mark.asyncio
    async def test_no_match(self, mocker, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(False, False, False, False)

        mock_log = mocker.patch.object(schedule_tasks.logger, "error")

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        mock_log.assert_called_once()
        assert result is None
