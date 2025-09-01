import asyncio
import logging
import uuid

from crawlee import Request
from crawler import start_crawler

from collecte.schemas import CollectionEventSchema, ScheduleGroupSchema, ScheduleSchema
from collecte.services.collections import get_active_collections
from collecte.services.schedules import add_schedule, retrieve_events
from collecte.tasks.efs_batch_processor import EFSBatchProcessor

logger = logging.getLogger(__name__)


async def _retrieve_active_collections_url() -> list[str]:
    """Retrieve all active collections from the database 
    then create Request object with their URL
    """
    active_collections = await get_active_collections()
    return [
        Request.from_url(c.url, unique_key=f"{c.url}:{uuid.uuid4()}")
        for c in active_collections
    ]


async def _get_schedules_from_crawler() -> list[ScheduleGroupSchema]:
    """Retrieves active collections URLs,
    then calls the crawler to get corresponding schedules.
    """
    try:
        urls = await _retrieve_active_collections_url()
        if not urls:
            logger.info("No URLs found to crawl.")
            return []

        # crawler_logger = logging.getLogger(f"{__name__}.crawler")
        all_results = []

        logger.info(f"Starting crawler for {len(urls)} URLs.")

        results = await start_crawler(urls)  # crawler_logger=crawler_logger)
        all_results.extend(results)

        logger.info(f"Total schedules scraped: {len(all_results)}")
        return all_results

    except Exception as e:
        logger.error("Failed to retrieve schedules from crawler", exc_info=e)
        return []


async def _match_event(
    schedule: ScheduleSchema, event: CollectionEventSchema
) -> ScheduleSchema | None:
    """Match the schedule with the event and return the schedule with the event id."""
    try:
        is_morning = bool(event.morning_start_time and event.morning_end_time)
        is_afternoon = bool(event.afternoon_start_time and event.afternoon_end_time)
        is_all_day = (is_morning and is_afternoon) or bool(
            event.morning_start_time and event.afternoon_end_time
        )

        if not (is_morning or is_afternoon or is_all_day):
            logger.warning("Event has no time range.", extra=event.info())
            return None

        # Create a new schedule object with the event ID.
        new_schedule = schedule.model_copy(update={"event_id": event.id})

        # If the event is all-day, return the schedule as is.
        if is_all_day:
            return new_schedule

        # Determine the correct time range to filter by.
        min_value = (
            event.morning_start_time if is_morning else event.afternoon_start_time
        )
        max_value = event.morning_end_time if is_morning else event.afternoon_end_time

        # Filter timetables based on the determined time range.
        new_schedule.timetables = {
            k: v for k, v in schedule.timetables.items() if min_value <= k <= max_value
        }

        return new_schedule

    except Exception as e:
        logger.error(
            "Failed to match schedule with event",
            extra={"event_id": event.id, **schedule.info(), "error": str(e)},
            exc_info=e,
        )
        return None


async def _handle_schedule(schedule: ScheduleSchema) -> list[ScheduleSchema]:
    """Retrieve events related to a schedule and match the schedule for each event."""
    try:
        events = await retrieve_events(schedule)
        if not events:
            logger.warning("No event found for schedule.", extra=schedule.info())
            return []

        tasks = [_match_event(schedule, event) for event in events]
        schedules = await asyncio.gather(*tasks)

        return [s for s in schedules if s is not None]

    except Exception as e:
        logger.error(
            "Failed to handle schedule.",
            extra={**schedule.info(), "error": str(e)},
            exc_info=e,
        )
        return []


async def _handle_schedules_group(
    schedules_group: ScheduleGroupSchema, efs_processor: EFSBatchProcessor
) -> list[ScheduleSchema]:
    """Retrieve EFS_ID of the url before handling each schedules."""
    try:
        efs_id = await efs_processor.get_efs_id(schedules_group.url)
        if not efs_id:
            logger.warning("Couldn't get EFS_ID.", extra={"url": schedules_group.url})
            return []

        schedules_group.efs_id = efs_id
        schedules = schedules_group.build()

        if not schedules:
            logger.info(
                "No schedules to process in this group.",
                extra={"url": schedules_group.url},
            )
            return []

        tasks = [_handle_schedule(schedule) for schedule in schedules]
        results = await asyncio.gather(*tasks)

        return [item for items in results for item in items]

    except Exception as e:
        logger.error(
            "Failed to handle ScheduleGroup.",
            extra={**schedules_group.info(), "error": str(e)},
            exc_info=e,
        )
        return []


async def update_schedules(
    schedules_groups: list[dict] | None = None,
) -> None:
    """Retrieve, process, and save schedules."""
    logger.info("Starting schedule update process.")

    if not schedules_groups:
        logger.info("No schedules specified. Retrieving with the crawler.")
        schedules_groups = await _get_schedules_from_crawler()

    if not schedules_groups:
        logger.error("No schedules to process.")
        return

    # Process all schedule groups concurrently.
    schedule_groups = [ScheduleGroupSchema(**sg) for sg in schedules_groups if sg]
    logger.info(f"Processing {len(schedule_groups)} schedule groups.")

    async with EFSBatchProcessor() as efs_processor:
        tasks = [_handle_schedules_group(sg, efs_processor) for sg in schedule_groups]
        processed_schedule_groups = await asyncio.gather(*tasks)

    # Flatten the list of lists of schedules.
    final_schedules = [s for sublist in processed_schedule_groups for s in sublist]

    if not final_schedules:
        logger.info("No schedules to save after processing.")
        return

    logger.info(f"Saving {len(final_schedules)} schedules.")
    save_tasks = [add_schedule(s) for s in final_schedules]
    await asyncio.gather(*save_tasks)

    logger.info(f"Successfully processed {len(final_schedules)} schedules.")
