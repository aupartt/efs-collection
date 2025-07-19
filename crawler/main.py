import asyncio
from crawler import get_location_events
from crawler.models import LocationEvents


if __name__ == "__main__":
    data: list[LocationEvents] = asyncio.run(
        get_location_events(
            [
                # "https://dondesang.efs.sante.fr/trouver-une-collecte/3343/sang/19-07-2025",
                "https://efs.link/FNh76",
                # "https://efs.link/RE2rS",
            ],
            headless=True,
            keep_alive=False,
        )
    )
    for event in data.items:
        print(event["url"])
