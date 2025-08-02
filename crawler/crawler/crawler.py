import asyncio
import aio_pika
from datetime import timedelta
import json
import logging

from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.storages import RequestQueue

from crawler.settings import settings
from crawler.models import LocationEvents
from crawler.locators import process_by_type

logger = logging.getLogger(__name__)


async def request_handler(
    context: PlaywrightCrawlingContext, channel: aio_pika.Channel = None
):
    try:
        context.log.info(f"Processing {context.request.url} ...")
        await context.page.wait_for_load_state("networkidle")
        data = await process_by_type(context)

        if channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=data.model_dump_json().encode()),
                routing_key=settings.RABBITMQ_DATA_QUEUE,
            )
        else:
            await context.push_data(data.model_dump_json())

    except Exception as e:
        context.log.error(f"Error in request handler: {e}")


async def start_crawler(
    urls: list[str],
    headless: bool = True,
    browser_type: str = "firefox",
    keep_alive: bool = False,
    channel: aio_pika.Channel | None = None,
    request_queue: RequestQueue | None = None,
) -> LocationEvents | None:
    crawler = PlaywrightCrawler(
        headless=headless,
        browser_type=browser_type,
        keep_alive=keep_alive,
        request_handler_timeout=timedelta(seconds=120),
        request_manager=request_queue,
    )

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext):
        await request_handler(context, channel)

    try:
        await crawler.run(urls)
    except Exception as e:
        logger.error(f"Error during crawling: {e}")

    if not keep_alive:
        data = await crawler.get_data()
        crawler.log.info(f"Extracted data: {data.items}")
        return data


if __name__ == "__main__":
    asyncio.run(
        start_crawler(
            urls=["https://dondesang.efs.sante.fr/trouver-une-collecte/138202/sang"],
            keep_alive=False,
        )
    )
