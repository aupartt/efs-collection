import asyncio
import argparse
import logging
import sys
import aio_pika
from aio_pika.exceptions import AMQPConnectionError
import uuid

from crawlee.storages import RequestQueue
from crawlee import Request

from crawler import start_crawler
from crawler.settings import settings
from crawler.models import LocationEvents

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Crawler for location events")
parser.add_argument("--urls", nargs="+", help="List of URLs to crawl")
parser.add_argument(
    "--headless", action="store_true", help="Run browser in headless mode"
)
parser.add_argument(
    "--browser-type", type=str, default="chromium", help="Browser type to use"
)
parser.add_argument(
    "--keep-alive", action="store_true", help="Keep the crawler alive after crawling"
)
parser.add_argument(
    "--request-handled-timeout",
    type=int,
    default=60 * 2,
    help="Timeout for request handling in seconds",
)
parser.add_argument(
    "--system-info-interval",
    type=int,
    default=60 * 30,
    help="Interval for system info logging in seconds",
)
parser.add_argument(
    "--max-requests-per-crawl",
    type=int,
    default=100,
    help="Maximum number of requests to process per crawl",
)

args = parser.parse_args()


async def consume_urls(queue: aio_pika.Queue, rq: RequestQueue):
    try:
        async for message in queue:
            try:
                async with message.process():
                    url = message.body.decode()
                    _id = f"{url}:{uuid.uuid4()}"
                    await rq.add_request(Request.from_url(url, unique_key=_id))
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except Exception as e:
        logger.error(f"Error in consume_urls: {e}")


async def setup_rabbitmq(keep_alive: bool, rq: RequestQueue):
    if not keep_alive:
        return None, None
    try:
        connection = await aio_pika.connect_robust(
            url=settings.RABBITMQ_URL,
            client_properties={"connection_name": "crawler"},
        )
        channel = await connection.channel()
        urls_queue = await channel.declare_queue(
            settings.RABBITMQ_URLS_QUEUE, durable=True
        )
        await channel.declare_queue(settings.RABBITMQ_DATA_QUEUE, durable=True)

        asyncio.create_task(consume_urls(urls_queue, rq))

        logger.info("RabbitMQ connection and channels established successfully.")
        return connection, channel
    except AMQPConnectionError as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        await asyncio.sleep(5)
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error setting up RabbitMQ: {e}")


async def main(args):
    rq = await RequestQueue.open()

    _, channel = await setup_rabbitmq(args.keep_alive, rq)

    while True:
        data: LocationEvents = await start_crawler(
            urls=args.urls,
            keep_alive=args.keep_alive,
            headless=args.headless,
            browser_type=args.browser_type,
            channel=channel,
            request_queue=rq,
            request_handled_timeout=args.request_handled_timeout,
            system_info_interval=args.system_info_interval,
            max_requests_per_crawl=args.max_requests_per_crawl,
        )

        if not args.keep_alive:
            return data


if __name__ == "__main__":
    logger.info("Starting crawler...")
    asyncio.run(main(args))
