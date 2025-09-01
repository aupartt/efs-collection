import logging
from datetime import timedelta

from crawlee.crawlers import BeautifulSoupCrawler

from crawler.handlers import collect_handler
from crawler.models import LocationEvents

logger = logging.getLogger(__name__)


async def start_crawler(
    urls: list[str],
    request_handled_timeout: int = 60 * 2,
    max_request_retries: int = 3,
    max_requests_per_crawl: int = 100,
    crawler_logger: logging.Logger = None,
    statistics_log_format: str = "inline",
    parser: str = "html.parser",
) -> LocationEvents | None:
    crawler = BeautifulSoupCrawler(
        max_request_retries=max_request_retries,
        request_handler_timeout=timedelta(seconds=request_handled_timeout),
        statistics_log_format=statistics_log_format,
        max_requests_per_crawl=max_requests_per_crawl,
        parser=parser,
        configure_logging=False,  # if crawler_logger else True,
        request_handler=collect_handler,
        # _logger=crawler_logger,
    )

    try:
        stats = await crawler.run(urls)
        logger.info("Crawler ended.", extra=stats.to_dict())
        data = await crawler.get_data()
        return data.items
    except Exception as e:
        logger.error(f"Error during crawling: {e}")
