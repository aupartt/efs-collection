import asyncio
from crawler import get_location_events
from crawler.models import LocationEvents


if __name__ == "__main__":
    data: list[LocationEvents] = asyncio.run(
        get_location_events(
            [
                "https://dondesang.efs.sante.fr/trouver-une-collecte/3343/sang/19-07-2025",  # Url with lots of events (useful for testing)
                # "https://efs.link/FNh76",
                # "https://efs.link/RE2rS",
            ],
            headless=True,
            keep_alive=False,
        )
    )
    for location in data.items:
        print("-------------------------")
        print(location["url"])
        for event in location["events"]:
            print("-------------------------")
            print("date:", event["date"])
            print("slots:", event["slots"])
            print("type:", event["type"])
            print("schedules:", len(event["schedules"]))
