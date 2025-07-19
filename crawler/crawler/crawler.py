import asyncio
from datetime import timedelta

from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

from crawler.models import LocationEvents
from crawler.locators import process_by_type


async def request_handler(context: PlaywrightCrawlingContext):
    context.log.info(f"Processing {context.request.url} ...")

    await context.page.wait_for_load_state("networkidle")

    data = await process_by_type(context)
    await context.push_data(data.model_dump())


async def get_location_events(
    urls: list[str],
    max_requests_per_crawl: int = 10,
    headless: bool = True,
    browser_type: str = "firefox",
    keep_alive: bool = False,
) -> list[LocationEvents]:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=max_requests_per_crawl,
        headless=headless,
        browser_type=browser_type,
        keep_alive=keep_alive,
        request_handler_timeout=timedelta(seconds=120),
    )

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext):
        await request_handler(context)

    await crawler.run(urls)

    # await crawler.export_data("results.json")
    data = await crawler.get_data()
    crawler.log.info(f"Extracted data: {data.items}")
    return data


if __name__ == "__main__":
    asyncio.run(
        get_location_events(
            [
                "https://efs.link/FNh76",
                "https://efs.link/RE2rS",
            ]
        )
    )
