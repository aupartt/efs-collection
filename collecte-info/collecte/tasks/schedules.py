import asyncio
import logging

from collecte.schemas import ScheduleSchema, ScheduleGroupSchema, CollectionEventSchema
from collecte.services.schedules import retrieve_events, add_schedule
from collecte.services.collections import get_active_collections
from collecte.tasks.collections import get_esf_id


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


async def _handle_schedule(schedule: ScheduleSchema) -> list[ScheduleSchema]:
    """Retrieve events related to a schedule and match the schedule for each event"""
    try:
        events: list[CollectionEventSchema] = await retrieve_events(schedule)
        schedules = []

        if len(events) == 0:
            raise ValueError("No event found.")

        # Only one event: We can save directly the schedule
        if len(events) == 1:
            schedule.event_id = events[0].id
            schedules.append(schedule)
        else:
            # Multiple events: We have to split the schedule (mostly morning / afternoon)
            tasks = [_match_event(schedule, event) for event in events]
            schedules = await asyncio.gather(*tasks)

        return schedules
    except Exception as e:
        logger.error(f"Error while handling schedule {schedule.info()} : {e}")


async def _handle_schedules_group(
    schedules_group: ScheduleGroupSchema,
) -> list[ScheduleSchema]:
    """Retrieve EFS_ID of the url before handling each schedules"""
    try:
        efs_id = await get_esf_id(schedules_group.url)
        if not efs_id:
            raise ValueError("Could get EFS_ID.")

        schedules_group.efs_id = efs_id
        schedules = schedules_group.build()

        tasks = [_handle_schedule(schedule) for schedule in schedules]
        results = await asyncio.gather(*tasks)

        return [item for items in results for item in items if item]
    except Exception as e:
        logger.error(
            f"Error while handling schedules group {schedules_group.info()} : {e}"
        )


async def save_schedules(
    schedules_groups: list[ScheduleGroupSchema] | None = None,
) -> None:
    """Retrieve, process and save schedules"""
    if not schedules_groups:
        schedules_groups = await _get_schedules_from_crawler()
    if not schedules_groups or len(schedules_groups) == 0:
        logger.error("No schedules to process")
        return

    # Get efs_ids and event id
    tasks = [
        _handle_schedules_group(schedules_group) for schedules_group in schedules_groups
    ]
    results = await asyncio.gather(*tasks)

    # Add scedules
    tasks = [
        add_schedule(schedule)
        for schedules in results
        for schedule in schedules
        if schedule
    ]
    results = await asyncio.gather(*tasks)

    logger.info(f"Added {len(results)} to the database")

    return results
