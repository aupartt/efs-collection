import asyncio
import argparse
import logging
import aio_pika

from crawlee.storages import RequestQueue

from crawler import start_crawler
from crawler.settings import settings
from crawler.models import LocationEvents

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Crawler for location events")
parser.add_argument("--urls", nargs="+", help="List of URLs to crawl")
parser.add_argument(
    "--max_requests_per_crawl",
    type=int,
    default=10,
    help="Maximum number of requests per crawl",
)
parser.add_argument(
    "--headless", action="store_true", help="Run browser in headless mode"
)
parser.add_argument(
    "--browser_type", type=str, default="firefox", help="Browser type to use"
)
parser.add_argument(
    "--keep_alive", action="store_true", help="Keep the crawler alive after crawling"
)

args = parser.parse_args()


async def consume_urls(queue: aio_pika.Queue, rq: RequestQueue):
    try:
        async for message in queue:
            try:
                async with message.process():
                    url = message.body.decode()
                    await rq.add_request(url)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except Exception as e:
        logger.error(f"Error in consume_urls: {e}")


async def setup_rabbitmq(keep_alive: bool, rq: RequestQueue):
    if not keep_alive:
        return None, None
    try:
        connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
        )
        channel = await connection.channel()
        urls_queue = await channel.declare_queue(
            settings.RABBITMQ_URLS_QUEUE, durable=True
        )
        await channel.declare_queue(settings.RABBITMQ_DATA_QUEUE, durable=True)

        asyncio.create_task(consume_urls(urls_queue, rq))

        logger.info("RabbitMQ connection and channels established successfully.")
        return connection, channel
    except Exception as e:
        logger.error(f"Error setting up RabbitMQ connection: {e}")
        raise


async def main(args):
    rq = await RequestQueue.open()

    _, channel = await setup_rabbitmq(args.keep_alive, rq)
    data: LocationEvents = await start_crawler(
        urls=args.urls,
        keep_alive=args.keep_alive,
        max_requests_per_crawl=args.max_requests_per_crawl,
        headless=args.headless,
        browser_type=args.browser_type,
        channel=channel,
        request_queue=rq,
    )

    if not args.keep_alive:
        return data


if __name__ == "__main__":
    logger.warning(f"Starting crawler with args: {args}")
    asyncio.run(main(args))
