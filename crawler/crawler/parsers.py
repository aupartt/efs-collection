import re

from crawler.models import Event, EventType, Schedules


def parse_event_type(event_title) -> EventType:
    """Extract the type of the collect event."""
    type_map = {"plasma": "plasma", "sang": "blood", "plaquettes": "platelets"}
    _type = event_title.split(" ")[-1]
    return type_map.get(_type, _type)


async def parse_event_slots(event_locator) -> int:
    """Extract the total number of slots available from the collect event."""
    slots_element = event_locator.locator(".timeslot-item__header > .place")
    _slots = (
        await slots_element.text_content() if await slots_element.count() > 0 else "0"
    )
    total_slots_match = re.search(r"\d+", _slots)
    return int(total_slots_match.group()) if total_slots_match else 0


async def parse_event_schedules(event_locator) -> Schedules:
    """Extract schedules from the collect event."""
    time_block_items = event_locator.locator(".time-block__item")
    count = await time_block_items.count()
    schedules = {}

    for i in range(count):
        time_block_item = time_block_items.nth(i)
        item_content = await time_block_item.text_content()
        parts = re.search(r"(\d{2}h\d{2})(\d+)", item_content)
        if parts:
            schedule, slots = parts.groups()
            slots_match = re.search(r"\d+", slots)
            if slots_match:
                schedules[schedule] = int(slots_match.group())

    return schedules


async def parse_event(event_locator, _type: EventType) -> Event:
    date = await event_locator.get_attribute("data-date")
    slots = await parse_event_slots(event_locator)
    schedules = await parse_event_schedules(event_locator)

    return Event(date=date, type=_type, slots=slots, schedules=schedules)
