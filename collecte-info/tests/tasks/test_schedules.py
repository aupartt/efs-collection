import pytest
from datetime import time
from unittest.mock import AsyncMock, MagicMock
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

import collecte.tasks.schedules as schedule_tasks
from collecte.models import ScheduleModel
from collecte.schemas import ScheduleSchema, CollectionEventSchema


class TestRetrieveActiveCollectionsUrl:
    @pytest.mark.asyncio
    async def test_found(self, mocker: MockerFixture, mock_grp_col):
        mock_get_active_collections = mocker.patch(
            "collecte.tasks.schedules.get_active_collections",
            return_value=mock_grp_col.schemas,
        )

        result = await schedule_tasks._retrieve_active_collections_url()

        mock_get_active_collections.assert_called_once()
        assert result == [schema.url for schema in mock_grp_col.schemas]

    @pytest.mark.asyncio
    async def test_not_found(self, mocker: MockerFixture, mock_grp_col):
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
    event_id = 42
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
            mock_event.id = self.event_id
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
        assert result.event_id == self.event_id

    @pytest.mark.asyncio
    async def test_match_morning(self, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(True, True, False, False)

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        assert isinstance(result, ScheduleSchema)
        assert result.total_slots == self.timetables_count_morning
        assert result.event_id == self.event_id

    @pytest.mark.asyncio
    async def test_match_afternoon(self, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(False, False, True, True)

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        assert isinstance(result, ScheduleSchema)
        assert result.total_slots == self.timetables_count_afternoon
        assert result.event_id == self.event_id

    @pytest.mark.asyncio
    async def test_match_start_end(self, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(True, False, False, True)

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        assert isinstance(result, ScheduleSchema)
        assert result.total_slots == self.timetables_count_total
        assert result.event_id == self.event_id

    @pytest.mark.asyncio
    async def test_no_match(self, mocker: MockerFixture, _mock_schedule, _mock_event):
        mock_schedule = _mock_schedule
        mock_event = _mock_event(False, False, False, False)

        mock_log = mocker.patch.object(schedule_tasks.logger, "error")

        result = await schedule_tasks._match_event(
            schedule=mock_schedule, event=mock_event
        )

        mock_log.assert_called_once()
        assert result is None


class TestHandleSchedule:
    @pytest.mark.asyncio
    async def test_found_one(self, mocker: MockerFixture, mock_sch, mock_evt_col):
        mock_events = [mock_evt_col.schemas[0]]
        mock_events[0].id = 42

        mock_retrieve_events = mocker.patch(
            "collecte.tasks.schedules.retrieve_events", return_value=mock_events
        )
        mock_match_event = mocker.patch("collecte.tasks.schedules._match_event")

        results = await schedule_tasks._handle_schedule(mock_sch.schemas[0])

        mock_retrieve_events.assert_called_once()
        mock_match_event.assert_not_called()
        assert len(results) == 1
        assert isinstance(results[0], ScheduleSchema)
        assert results[0].event_id == mock_events[0].id

    @pytest.mark.asyncio
    async def test_found_many(self, mocker: MockerFixture, mock_sch, mock_evt_col):
        mock_events = mock_evt_col.schemas[:2]
        mock_results = [
            mock_sch.schemas[:2],
            mock_sch.schemas[2:],
        ]

        mock_retrieve_events = mocker.patch(
            "collecte.tasks.schedules.retrieve_events", return_value=mock_events
        )
        mock_match_event = mocker.patch(
            "collecte.tasks.schedules._match_event", side_effect=mock_results
        )

        results = await schedule_tasks._handle_schedule(mock_sch.schemas[0])

        mock_retrieve_events.assert_awaited_once()
        mock_match_event.call_count == 2
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_not_found(self, mocker: MockerFixture, mock_sch, mock_evt_col):
        mock_events = []
        mock_results = [
            mock_sch.schemas[:2],
            mock_sch.schemas[2:],
        ]

        mock_retrieve_events = mocker.patch(
            "collecte.tasks.schedules.retrieve_events", return_value=mock_events
        )
        mock_match_event = mocker.patch(
            "collecte.tasks.schedules._match_event", side_effect=mock_results
        )
        mock_log = mocker.patch.object(schedule_tasks.logger, "error")

        results = await schedule_tasks._handle_schedule(mock_sch.schemas[0])

        mock_retrieve_events.assert_awaited_once()
        mock_log.assert_called_once()
        mock_match_event.assert_not_called()
        assert results is None


class TestHandleSchedulesGroup:
    @pytest.mark.asyncio
    async def test_no_efs_id(self, mocker: MockerFixture, mock_grp_sch):
        mock_get_esf_id = mocker.patch(
            "collecte.tasks.schedules.get_esf_id", return_value=None
        )
        mock_log = mocker.patch.object(schedule_tasks.logger, "error")

        results = await schedule_tasks._handle_schedules_group(mock_grp_sch.schemas[0])

        mock_get_esf_id.assert_awaited_once()
        mock_log.assert_called_once()
        assert results is None

    @pytest.mark.asyncio
    async def test_success(self, mocker: MockerFixture, mock_grp_sch):
        mock_schedules_group = mock_grp_sch.schemas[0]

        mock_get_esf_id = mocker.patch(
            "collecte.tasks.schedules.get_esf_id", return_value="foo"
        )
        mock_handle_schedule = mocker.patch(
            "collecte.tasks.schedules._handle_schedule",
            side_effect=[[1, 2], [3], [4, 5, 6]],
        )

        results = await schedule_tasks._handle_schedules_group(mock_schedules_group)

        mock_get_esf_id.assert_awaited_once()
        mock_handle_schedule.call_count == 2
        assert len(results) == 6


class TestSaveSchedule:
    @pytest.mark.asyncio
    async def test_no_schedules_groups(self, mocker: MockerFixture, mock_grp_sch):
        mock_get_schedules_from_crawler = mocker.patch(
            "collecte.tasks.schedules._get_schedules_from_crawler", return_value=None
        )
        mock_log = mocker.patch.object(schedule_tasks.logger, "error")

        results = await schedule_tasks.save_schedules()

        mock_get_schedules_from_crawler.assert_awaited_once()
        mock_log.assert_called_once()
        assert results is None

    @pytest.mark.asyncio
    async def test_success_crawler(self, mocker: MockerFixture, mock_grp_sch):
        mock_get_schedules_from_crawler = mocker.patch(
            "collecte.tasks.schedules._get_schedules_from_crawler",
            return_value=mock_grp_sch.schemas,
        )  # return len 3
        mock_handle_schedules_group = mocker.patch(
            "collecte.tasks.schedules._handle_schedules_group",
            side_effect=[
                [1],
                [2, None, 3, 4],
                [],
            ],
        )
        mock_add_schedule = mocker.patch(
            "collecte.tasks.schedules.add_schedule",
            return_value=True,
        )

        results = await schedule_tasks.save_schedules()

        mock_get_schedules_from_crawler.assert_awaited_once()
        mock_handle_schedules_group.call_count == 3
        mock_add_schedule.call_count == 4
        assert len(results) == 4

    @pytest.mark.asyncio
    async def test_success_param(self, mocker: MockerFixture, mock_grp_sch):
        mock_get_schedules_from_crawler = mocker.patch(
            "collecte.tasks.schedules._get_schedules_from_crawler"
        )
        mock_handle_schedules_group = mocker.patch(
            "collecte.tasks.schedules._handle_schedules_group",
            side_effect=[
                [1],
                [2, None, 3, 4],
                [],
            ],
        )
        mock_add_schedule = mocker.patch(
            "collecte.tasks.schedules.add_schedule",
            return_value=True,
        )

        results = await schedule_tasks.save_schedules(mock_grp_sch.schemas)

        mock_get_schedules_from_crawler.assert_not_called()
        mock_handle_schedules_group.call_count == 3
        mock_add_schedule.call_count == 4
        assert len(results) == 4
