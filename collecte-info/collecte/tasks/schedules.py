import logging

from collecte.schemas import ScheduleSchema, ScheduleGroupSchema, CollectionEventSchema
from collecte.services.schedules import retrieve_events, add_schedule
from collecte.services.collections import get_active_collections


logger = logging.getLogger(__name__)


async def _retrieve_active_collections_url() -> list[str]:
    """Retrieve all active collections from the database and return their URL"""
    active_collections = await get_active_collections()
    return [collection.url for collection in active_collections if collection]


async def _get_schedules_from_crawler() -> list[ScheduleGroupSchema]:
    """Retrieves active collections urls
    then call the crawler to get corresponding schedules
    """
    urls = await _retrieve_active_collections_url()
    pass


async def _match_event(
    schedule: ScheduleSchema, event: CollectionEventSchema
) -> ScheduleSchema | None:
    """Match the schedule with the event and return the schedule with the event id.
    - It may have multiple events for the same day but with different timetables.
    """
    try:
        # Get basic informations
        is_morning = all([event.morning_start_time, event.morning_end_time])
        is_afternoon = all([event.afternoon_start_time, event.afternoon_end_time])
        is_all_day = all([event.morning_start_time, event.afternoon_end_time]) or all(
            [is_morning, is_afternoon]
        )
        if not any([is_morning, is_afternoon, is_all_day]):
            raise ValueError("The event have no timerange")

        # No error, we can assign ID
        schedule.event_id = event.id

        # Check if this event is for the whole day
        if is_all_day:
            return schedule

        # Set MinMax values for event
        if is_morning:
            min_value = event.morning_start_time
            max_value = event.morning_end_time
        else:
            min_value = event.afternoon_start_time
            max_value = event.afternoon_end_time

        new_schedule = schedule.model_copy()
        new_schedule.timetables = {
            k: v
            for k, v in schedule.timetables.items()
            if k >= min_value and k <= max_value
        }

        return new_schedule

    except Exception as e:
        logger.error(
            f"Error while matching schedule {schedule.info()} with event {event.id} : {e}"
        )
