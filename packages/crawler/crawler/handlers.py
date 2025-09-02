import logging
from datetime import UTC, datetime

from crawlee.crawlers import (
    BeautifulSoupCrawlingContext,
)

from crawler.models import LocationEvents
from crawler.parsers import parse_collect_type, parse_events, parse_location

logger = logging.getLogger(__name__)


async def collect_handler(context: BeautifulSoupCrawlingContext) -> LocationEvents:
    """Crawler handler. Retrieve all informations for the EFS collects."""
    try:
        url = context.request.url
        data = {"url": context.request.url}

        logger.info("Start processing page.", extra={"url": url})

        # Parse location
        location = await parse_location(context)
        if not location.success:
            return
        data["location"] = location.value

        # Parse events type
        collect_type_result = await parse_collect_type(context)
        if not collect_type_result.success:
            return
        data["collect_type"] = collect_type_result.value

        # Parse all events
        events_result = await parse_events(context)
        if not events_result.success:
            return
        data["events"] = events_result.value

        location_events = LocationEvents(**data, time=datetime.now(UTC))
        await context.push_data(location_events.model_dump_json())
    except Exception as e:
        context.log.error(f"Error in request handler: {e}")
