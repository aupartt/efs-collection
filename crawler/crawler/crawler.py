import asyncio
import aio_pika
from datetime import timedelta
import json

from crawlee import Request
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

from crawler.settings import settings
from crawler.models import LocationEvents
from crawler.locators import process_by_type


async def request_handler(context: PlaywrightCrawlingContext, keep_alive: bool, channel: aio_pika.Channel = None):
    context.log.info(f"Processing {context.request.url} ...")

    await context.page.wait_for_load_state("networkidle")

    data = await process_by_type(context)

    if keep_alive:
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(data.model_dump()).encode()),
            routing_key=settings.rabbitmq_processed_data_queue,
        )
    else:
        await context.push_data(data.model_dump())


async def consume_urls(queue: aio_pika.Queue, crawler: PlaywrightCrawler, channel: aio_pika.Channel):
    async for message in queue:
        async with message.process():
            url = message.body.decode()
            context = PlaywrightCrawlingContext(request=Request(url=url), crawler=crawler)
            await request_handler(context, crawler.keep_alive, channel)


async def get_location_events(
    urls: list[str],
    max_requests_per_crawl: int = 10,
    headless: bool = True,
    browser_type: str = "firefox",
    keep_alive: bool = False,
    connection: aio_pika.Connection = None,
    channel: aio_pika.Channel = None
) -> list[LocationEvents]:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=max_requests_per_crawl,
        headless=headless,
        browser_type=browser_type,
        keep_alive=keep_alive,
        request_handler_timeout=timedelta(seconds=120),
    )

    if keep_alive:
        urls_queue = await channel.get_queue(settings.rabbitmq_urls_queue)
        # Start consuming URLs from the queue
        asyncio.create_task(consume_urls(urls_queue, crawler, channel))

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext):
        await request_handler(context, keep_alive, channel)
    await crawler.run(urls)

    # await crawler.export_data("results.json")
    if not keep_alive:
        data = await crawler.get_data()
        crawler.log.info(f"Extracted data: {data.items}")
        return data
