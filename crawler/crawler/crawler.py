import asyncio
import aio_pika
from datetime import timedelta
import logging

from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.storages import RequestQueue
from crawlee.configuration import Configuration
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
            from crawler.settings import settings

            await channel.default_exchange.publish(
                aio_pika.Message(body=data.model_dump_json().encode()),
                routing_key=settings.RABBITMQ_DATA_QUEUE,
            )
        else:
            await context.push_data(data.model_dump_json())

    except Exception as e:
        context.log.error(f"Error in request handler: {e}")
    finally:
        await context.page.close()


async def start_crawler(
    urls: list[str],
    headless: bool = True,
    browser_type: str = "chromium",
    keep_alive: bool = False,
    channel: aio_pika.Channel | None = None,
    request_queue: RequestQueue | None = None,
    request_handled_timeout: int = 60 * 2,
    system_info_interval: int = 60 * 30,
    max_requests_per_crawl: int = 100,
    crawler_logger: logging.Logger = None
) -> LocationEvents | None | str:
    config = Configuration.get_global_configuration()
    config.available_memory_ratio = 0.33

    # Add memory management configuration
    browser_launch_options = {
        "args": [
            "--memory-pressure-off",
            "--max_old_space_size=2048",  # Limit Node.js heap
            "--disable-dev-shm-usage",  # Reduce shared memory usage
            "--disable-extensions",
            "--disable-plugins",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
        ]
    }

    if browser_type == "chromium":
        browser_launch_options["args"].extend(
            [
                "--disable-web-security",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ]
        )

    crawler = PlaywrightCrawler(
        headless=headless,
        browser_type=browser_type,
        keep_alive=keep_alive,
        request_handler_timeout=timedelta(seconds=request_handled_timeout),
        request_manager=request_queue,
        statistics_log_format="inline",
        browser_launch_options=browser_launch_options,
        max_requests_per_crawl=max_requests_per_crawl,
        _logger=crawler_logger,
        configure_logging=False if crawler_logger else True
        # Not implemented in Python version yet
        # status_message_logging_interval=timedelta(seconds=system_info_interval),
    )

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext):
        await request_handler(context, channel)

    try:
        stats = await crawler.run(urls)
    except Exception as e:
        logger.error(f"Error during crawling: {e}")

    if not keep_alive:
        data = await crawler.get_data()
        return data
    elif stats.requests_total > max_requests_per_crawl:
        return "MAX_REQUESTS_REACHED"


if __name__ == "__main__":
    asyncio.run(
        start_crawler(
            urls=["https://dondesang.efs.sante.fr/trouver-une-collecte/138202/sang"],
            keep_alive=True,
        )
    )
