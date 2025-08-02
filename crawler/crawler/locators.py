import asyncio
from datetime import datetime, timezone

from crawlee.crawlers import PlaywrightCrawlingContext
from crawler.models import LocationEvents, Event, EventType
from crawler.parsers import parse_event, parse_event_type


async def locate_events(
    context: PlaywrightCrawlingContext, _type: EventType
) -> list[Event]:
    """Extract all collect events."""
    events_element = context.page.locator(".timeslot-item")
    count = await events_element.count()

    context.log.info(f"Found {count} events.")
    tasks = [parse_event(events_element.nth(i), _type) for i in range(count)]
    events: list[Event] = await asyncio.gather(*tasks)

    return events


async def wait_for_loader(context: PlaywrightCrawlingContext):
    """Wait for the loader to disappear."""
    for _ in range(10):
        await context.page.wait_for_timeout(1000)
        loader = context.page.locator("#efs-js-loader")
        count = await loader.count()
        if count == 0:
            continue
        classes = await loader.get_attribute("class")
        if "hidden" in classes:
            break


async def process_by_type(context: PlaywrightCrawlingContext) -> LocationEvents:
    """Extract all collect events by type."""
    event_types = context.page.locator(
        ".map-timeslot__don-type__filters button:not(.disabled)"
    )
    count = await event_types.count()
    context.log.info(f"Found {count} event types.")
    events: list[Event] = []

    for i in range(count):
        event_type = event_types.nth(i)
        type_name = parse_event_type(await event_type.text_content())
        context.log.info(f"Processing {type_name} events...")
        btn_classes = await event_type.get_attribute("class")

        if "active" not in btn_classes:
            await event_type.click()
            await wait_for_loader(context)

        _events = await locate_events(context, type_name)
        context.log.info(f"Processed {len(_events)} {type_name} events.")
        events.extend(_events)

    now = datetime.now(timezone.utc)
    return LocationEvents(url=context.request.url, time=now, events=events)
