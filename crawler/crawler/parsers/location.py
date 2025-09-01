import logging

from crawlee.crawlers import BeautifulSoupCrawlingContext

from crawler.models import CollectType, Result

logger = logging.getLogger(__name__)


async def parse_location(context: BeautifulSoupCrawlingContext) -> Result[str]:
    """Retrieve the events location"""
    location_element = context.soup.select_one(".card-rdv .top")
    if not location_element:
        logger.error("Location not found.", extra={"url": context.request.url})
        return Result(success=False, error="NO_LOCATION_FOUND")
    location = location_element.text.strip()
    logger.info(f"Location found: {location}", extra={"url": context.request.url})
    return Result(success=True, value=location)


async def _translate_collect_type(collect_type: str) -> Result[CollectType]:
    """Translate the type of donation from french to english."""
    type_map = {"plasma": "plasma", "sang": "blood", "plaquettes": "platelets"}

    if collect_type not in type_map:
        logger.error(f"{collect_type} is not a valid collect type.")
        return Result(success=False, error="UNKNOWN_COLLECT_TYPE")

    collect_type = type_map.get(collect_type)
    return Result(success=True, value=collect_type)


async def parse_collect_type(
    context: BeautifulSoupCrawlingContext,
) -> Result[CollectType]:
    """Retrieve the type of the collect from the HTML page"""
    try:
        select = context.soup.select_one("#map-timeslot__don-type select")
        option = select.select_one("option", selected=True)
        value = option.get("value")
        result = await _translate_collect_type(value.lower())

        if not result.success:
            return Result(success=False, error=result.error)

        logger.info(
            f"Collect type found: {result.value}.", extra={"url": context.request.url}
        )
        return Result(success=True, value=result.value)
    except Exception as e:
        logger.error(
            "Error while parsing the collect type.",
            extra={"url": context.request.url},
            exc_info=e,
        )
        return Result(success=False, error="COLLECT_TYPE_NOT_FOUND")
