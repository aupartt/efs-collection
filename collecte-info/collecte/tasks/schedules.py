import asyncio
import logging
import math
import uuid

from crawlee import Request
from crawler.crawler import start_crawler

from collecte.core.settings import settings
from collecte.schemas import CollectionEventSchema, ScheduleGroupSchema, ScheduleSchema
from collecte.services.collections import get_active_collections
from collecte.services.schedules import add_schedule, retrieve_events
from collecte.tasks.efs_batch_processor import EFSBatchProcessor

logger = logging.getLogger(__name__)


async def _retrieve_active_collections_url() -> list[str]:
    """Retrieve all active collections from the database and return their URL"""
    active_collections = await get_active_collections()
    return list({collection.url for collection in active_collections if collection})


async def _get_schedules_from_crawler() -> list[ScheduleGroupSchema] | None:
    """Retrieves active collections urls
    then call the crawler to get corresponding schedules
    """

    async def buil_request(url):
        _id = f"{url}:{uuid.uuid4()}"
        return Request.from_url(url, unique_key=_id)

    try:
        urls = await _retrieve_active_collections_url()

        results = []
        b = settings.CRAWLER_BATCH
        crawler_logger = logging.getLogger(__name__ + ".crawler")

        logger.info(f"Start crawler with batch {b} for {len(urls)} urls")

        for i in range(math.ceil(len(urls) / b)):
            _urls = [await buil_request(url) for url in urls[b * i : b * i + b]]
            batch_results = await start_crawler(_urls, crawler_logger=crawler_logger)
            results.extend(batch_results.items)

        filtered_results = [result for result in results if result]
        logger.info(f"Total schedules scraped : {len(filtered_results)}")
        return filtered_results
    except Exception as e:
        logger.error("Failed to retrieve schedules from crawler", extra={"error": e})


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
            "Failed to match schedule with event",
            extra={"event_id": event.id, **schedule.info(), "error": str(e)},
        )


async def _handle_schedule(schedule: ScheduleSchema) -> list[ScheduleSchema]:
    """Retrieve events related to a schedule and match the schedule for each event"""
    try:
        events: list[CollectionEventSchema] = await retrieve_events(schedule)
        schedules = []

        if len(events) == 0:
            logger.warning("No event found", extra={**schedule.info()})
            return schedules

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
        logger.error(
            "Failed to handle Schedule",
            extra={**schedule.info(), "error": str(e)},
        )
        return []


async def _handle_schedules_group(
    schedules_group: ScheduleGroupSchema,
    efs_processor: EFSBatchProcessor
) -> list[ScheduleSchema]:
    """Retrieve EFS_ID of the url before handling each schedules"""
    try:
        efs_id = await efs_processor.get_efs_id(schedules_group.url)
        if not efs_id:
            raise ValueError("Couldn't get EFS_ID.")

        schedules_group.efs_id = efs_id
        schedules = schedules_group.build()

        tasks = [_handle_schedule(schedule) for schedule in schedules]
        results = await asyncio.gather(*tasks)

        return [item for items in results for item in items if item]
    except Exception as e:
        logger.error(
            "Failed to handle ScheduleGroup",
            extra={**schedules_group.info(), "error": str(e)},
        )


async def update_schedules(
    schedules_groups: list[dict] | None = None,
) -> None:
    """Retrieve, process and save schedules"""
    logger.info("Start updating schedules...")

    if not schedules_groups:
        logger.info("No schedules specified, retrieving with the crawler")
        schedules_groups = await _get_schedules_from_crawler()
        logger.info("Schedules retrieved.")

    if not schedules_groups or len(schedules_groups) == 0:
        logger.error("No schedules to process")
        return

    schedules_groups = [
        ScheduleGroupSchema(**schedule) for schedule in schedules_groups if schedule
    ]

    logger.info(f"Processing {len(schedules_groups)} schedules...")

    # Get efs_ids and event id
    async with EFSBatchProcessor() as efs_processor:
        tasks = [
            _handle_schedules_group(schedules_group, efs_processor)
            for schedules_group in schedules_groups
            if schedules_group
        ]
        results = await asyncio.gather(*tasks)

    # Add scedules
    tasks = [
        add_schedule(schedule)
        for schedules in results
        if schedules
        for schedule in schedules
        if schedule and bool(schedule.timetables)
    ]
    results = await asyncio.gather(*tasks)

    logger.info("Successfully processed schedules", extra={"n_schedules": len(results)})
