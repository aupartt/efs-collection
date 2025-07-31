import asyncio
import aio_pika
import argparse
import logging
from crawler import get_location_events
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


if __name__ == "__main__":
    logger.warning(f"Starting crawler with args: {args}")
    try:
        data: list[LocationEvents] = asyncio.run(
            get_location_events(
                args.urls,
                max_requests_per_crawl=args.max_requests_per_crawl,
                headless=args.headless,
                browser_type=args.browser_type,
                keep_alive=args.keep_alive
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
    except Exception as e:
        logger.error(f"An error occurred during crawling: {e}")
