import logging
import re

from crawlee.crawlers import BeautifulSoupCrawlingContext

from crawler.models import Event, Locator, Result, Schedules

logger = logging.getLogger(__name__)


async def _parse_event_date(event_locator: Locator) -> str:
    date = event_locator.attrs.get("data-date")
    if not date:
        raise ValueError("EVENT_DATE_NOT_FOUND")
    return date


async def _parse_event_slots(event_locator: Locator) -> int:
    """Extract the total number of slots available from the collect event."""
    slots_element = event_locator.select_one(".timeslot-item__header > .place")
    total_slots_match = re.search(r"\d+", slots_element.text)
    if not total_slots_match:
        raise ValueError("EVENT_SLOT_NOT_FOUND")
    return int(total_slots_match.group())


async def _parse_event_schedules(event_locator: Locator) -> Schedules:
    """Extract schedules of the event."""
    time_block_items = event_locator.select(".time-block__item")
    schedules: Schedules = {}

    for time_block_item in time_block_items:
        parts = re.search(r"(\d{2}h\d{2})(\d+)", time_block_item.text)
        if not parts:
            continue

        schedule, slots = parts.groups()
        slots_match = re.search(r"\d+", slots)
        if slots_match:
            schedules[schedule] = int(slots_match.group())

    return schedules


async def _parse_event(url: str, event_id: int, event_locator: Locator) -> Result[Event]:
    """Parse the date, available slots and detailed schedules from an event."""
    try:
        date = await _parse_event_date(event_locator)
        slots = await _parse_event_slots(event_locator)
        schedules = Schedules()
        if slots > 0:
            schedules = await _parse_event_schedules(event_locator)

        event = Event(date=date, slots=slots, schedules=schedules)
        return Result(success=True, value=event)
    except ValueError as e:
        # The event might be private or online but not ready
        logger.warning(
            f"Failed to parse the event information for iteration {event_id}",
            extra={"url": url, "error": str(e)},
        )
        return Result(success=False, error=str(e))
    except Exception as e:
        logger.error(
            f"Something went wrong while parsing event iteration {event_id}",
            extra={"url": url},
            exc_info=e,
        )
        return Result(success=False, error=str(e))


async def parse_events(context: BeautifulSoupCrawlingContext) -> Result[list[Event]]:
    """Retrieve all the events selector, then parse them to get all the details."""
    events_element = context.soup.select(".timeslot-item")
    if not events_element:
        logger.warning("No events found.", extra={"url": context.request.url})
        return Result(success=False, error="NO_EVENT_FOUND")
    logger.info(f"Found {len(events_element)} events.", extra={"url": context.request.url})

    events = []
    for event_id, event_locator in enumerate(events_element):
        event_result = await _parse_event(context.request.url, event_id, event_locator)
        if not event_result.success:
            continue
        events.append(event_result.value)

    logger.info(
        f"Successfully parsed {len(events)} events.",
        extra={"url": context.request.url},
    )
    return Result(success=True, value=events)
