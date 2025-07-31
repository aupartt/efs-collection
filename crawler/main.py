import asyncio
import aio_pika
import argparse

from crawler import get_location_events
from crawler.settings import settings
from crawler.models import LocationEvents


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


def setup_rabbitmq(keep_alive: bool) -> tuple:
    if not keep_alive:
        return None, None

    async def async_setup():
        connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            login=settings.rabbitmq_user,
            password=settings.rabbitmq_password,
        )
        channel = await connection.channel()

        await channel.declare_queue(settings.rabbitmq_urls_queue, durable=True)
        await channel.declare_queue(
            settings.rabbitmq_processed_data_queue, durable=True
        )

        return connection, channel

    # Use asyncio to run the asynchronous function synchronously
    loop = asyncio.get_event_loop()
    connection, channel = loop.run_until_complete(async_setup())
    return connection, channel


if __name__ == "__main__":
    connection, channel = setup_rabbitmq(args.keep_alive)

    data: list[LocationEvents] = asyncio.run(
        get_location_events(
            args.urls,
            max_requests_per_crawl=args.max_requests_per_crawl,
            headless=args.headless,
            browser_type=args.browser_type,
            keep_alive=args.keep_alive,
            connection=connection,
            channel=channel,
        )
    )

    if not args.keep_alive:
        for location in data.items:
            print("-------------------------")
            print(location["url"])
            for event in location["events"]:
                print(event)
            print("-------------------------")
        print(f"Total locations: {len(data.items)}")
        # print(data.items)
