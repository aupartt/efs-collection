import asyncio
from crawler import get_event_data
from crawler.models import EventCollection


if __name__ == "__main__":
    data: list[EventCollection] = asyncio.run(
        get_event_data(
            [
                "https://efs.link/FNh76",
                "https://efs.link/RE2rS",
            ]
        )
    )

    print(data)
