import asyncio
import aio_pika
from datetime import timedelta
import json
import logging
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawler.settings import settings
from crawler.models import LocationEvents
from crawler.locators import process_by_type

logger = logging.getLogger(__name__)

async def request_handler(context: PlaywrightCrawlingContext, keep_alive: bool, channel: aio_pika.Channel = None):
    try:
        context.log.info(f"Processing {context.request.url} ...")
        await context.page.wait_for_load_state("networkidle")
        data = await process_by_type(context)
        if keep_alive and channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data.model_dump()).encode()),
                routing_key=settings.rabbitmq_processed_data_queue,
            )
        else:
            await context.push_data(data.model_dump())
    except Exception as e:
        context.log.error(f"Error in request handler: {e}")

async def consume_urls(queue: aio_pika.Queue, crawler: PlaywrightCrawler, channel: aio_pika.Channel):
    try:
        async for message in queue:
            try:
                async with message.process():
                    url = message.body.decode()
                    context = PlaywrightCrawlingContext(url=url, crawler=crawler)
                    await request_handler(context, crawler.keep_alive, channel)
            except Exception as e:
                crawler.log.error(f"Error processing message: {e}")
    except Exception as e:
        crawler.log.error(f"Error in consume_urls: {e}")

async def setup_rabbitmq(keep_alive: bool):
    if not keep_alive:
        return None, None
    try:
        connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            login=settings.rabbitmq_user,
            password=settings.rabbitmq_password,
        )
        channel = await connection.channel()
        await channel.declare_queue(settings.rabbitmq_urls_queue, durable=True)
        await channel.declare_queue(settings.rabbitmq_processed_data_queue, durable=True)
        logger.info("RabbitMQ connection and channels established successfully.")
        return connection, channel
    except Exception as e:
        logger.error(f"Error setting up RabbitMQ connection: {e}")
        raise

async def get_location_events(
    urls: list[str],
    max_requests_per_crawl: int = 10,
    headless: bool = True,
    browser_type: str = "firefox",
    keep_alive: bool = False,
):
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=max_requests_per_crawl,
        headless=headless,
        browser_type=browser_type,
        keep_alive=keep_alive,
        request_handler_timeout=timedelta(seconds=120),
    )

    connection, channel = None, None
    if keep_alive:
        try:
            connection, channel = await setup_rabbitmq(keep_alive)
            urls_queue = await channel.get_queue(settings.rabbitmq_urls_queue)
            asyncio.create_task(consume_urls(urls_queue, crawler, channel))
        except Exception as e:
            crawler.log.error(f"Error setting up queue consumption: {e}")

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext):
        await request_handler(context, keep_alive, channel)

    try:
        await crawler.run(urls)
    except Exception as e:
        logger.error(f"Error during crawling: {e}")

    if not keep_alive:
        data = await crawler.get_data()
        crawler.log.info(f"Extracted data: {data.items}")
        return data

if __name__ == "__main__":
    asyncio.run(get_location_events(
        urls=['https://dondesang.efs.sante.fr/trouver-une-collecte/138202/sang'],
        keep_alive=True
    ))
