import asyncio
import re
from datetime import datetime
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

from crawler.models import EventCollection, Event, Schedules


async def extract_date(date_collecte) -> str:
    """Extract and parse the date of the collect event."""
    date_element = date_collecte.locator(".timeslot-item__header > .date")
    count = await date_element.count()

    if count == 0:
        return "N/A"

    # Real date exemple : "mar. 30/09" -> "Day. DD/MM"
    date_content = await date_element.text_content()
    parts = re.search(r"(\d{2})/(\d{2})", date_content)
    if not parts:
        return "N/A"
    day, month = map(int, parts.groups())

    current_date = datetime.today()
    year = current_date.year
    date = datetime(year, month, day)

    if date < current_date:
        date = datetime(year + 1, month, day)

    return date.strftime("%Y-%m-%d")


async def extract_slots(date_collecte) -> int:
    """Extract the total number of slots available from the collect event."""
    slots_element = date_collecte.locator(".timeslot-item__header > .place")
    _slots = (
        await slots_element.text_content() if await slots_element.count() > 0 else "0"
    )
    total_slots_match = re.search(r"\d+", _slots)
    return int(total_slots_match.group()) if total_slots_match else 0


async def extract_schedules(date_collecte) -> Schedules:
    """Extract schedules from the collect event."""
    time_block_items = date_collecte.locator(".time-block__item")
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


async def process_date_collecte(date_collecte) -> Event:
    date = await extract_date(date_collecte)
    slots = await extract_slots(date_collecte)
    schedules = await extract_schedules(date_collecte)

    return Event(date=date, slots=slots, schedules=schedules)


async def request_handler(context: PlaywrightCrawlingContext) -> EventCollection:
    context.log.info(f"Processing {context.request.url} ...")

    await context.page.wait_for_load_state("networkidle")

    date_collectes = context.page.locator(".timeslot-item")
    count = await date_collectes.count()
    events = []

    for i in range(count):
        date_collecte = date_collectes.nth(i)
        event = await process_date_collecte(date_collecte)
        events.append(event)

    data = EventCollection(url=context.request.url, events=events)
    await context.push_data(data.__dict__)
    return data


async def get_event_data(
    urls: list[str],
    max_requests_per_crawl: int = 10,
    headless: bool = True,
    browser_type: str = "firefox",
    keep_alive: bool = False,
) -> list[EventCollection]:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=max_requests_per_crawl,
        headless=headless,
        browser_type=browser_type,
        keep_alive=keep_alive,
    )

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext):
        await request_handler(context)

    await crawler.run(urls)

    # await crawler.export_data("results.json")
    data = await crawler.get_data()
    crawler.log.info(f"Extracted data: {data.items}")
    return data


if __name__ == "__main__":
    asyncio.run(
        get_event_data(
            [
                "https://efs.link/FNh76",
                "https://efs.link/RE2rS",
            ]
        )
    )
