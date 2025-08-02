import aio_pika
import asyncio
import json
from pathlib import Path
import logging
import re
import argparse

from settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COLLECTIONS_FILE = Path("data/collections.jsonl")
SCHEDULES_FILE = Path("data/schedules.jsonl")


parser = argparse.ArgumentParser(description="CLI to retrieve schedules")
parser.add_argument(
    "--listen", action="store_true", help="Start the consumer to listen for processed data"
)

args = parser.parse_args()


async def consume_processed_data(channel: aio_pika.Channel):
    queue = await channel.get_queue("processed_data")
    async for message in queue:
        async with message.process():
            data = message.body.decode()
            _data = json.loads(data)
            _url = _data.get("url")
            _events = _data.get("events", [])

            if len(_events) == 0:
                logger.warning(f"No events found for: {_url}")
                continue

            logger.info(f"Received {len(_events)} events for: {_url}")
            with SCHEDULES_FILE.open("a", encoding="utf-8") as file:
                file.write(data + "\n")


async def send_url(channel: aio_pika.Channel, url: str):
    queue = await channel.get_queue("crawler_urls")
    await channel.default_exchange.publish(
        aio_pika.Message(body=url.encode()),
        routing_key=queue.name,
    )


def retrieve_collection_url(collections: list) -> str:
    """Retrieve url from collections,
    it doesn't matter if the url is for blood, plasma or platelets as the crawler will try to get all informations.
    """
    url = None

    for collection in collections:
        if collection.get("urlBlood"):
            url = collection["urlBlood"]
        elif collection.get("urlPlasma"):
            url = collection["urlPlasma"]
        elif collection.get("urlPlatelets"):
            url = collection["urlPlatelets"]

    if not url:
        raise ValueError("No url found in collections")

    if not re.match(r"https?://", url):
        url = f"https://{url}"

    return url


async def get_collections(channel: aio_pika.Channel):
    with open(COLLECTIONS_FILE, "r") as file:
        for line in file.readlines():
            data = json.loads(line)
            collections = data.get("collections", [])
            try:
                collection_url = retrieve_collection_url(collections)
                await send_url(channel, collection_url)
            except ValueError as e:
                logger.error(
                    f"Error retrieving collection url for {data.get('fullAddress', 'None')} - {data.get('groupCode', 'None')}: {e}"
                )


async def main():
    if not COLLECTIONS_FILE.is_file():
        logger.error(f"File {COLLECTIONS_FILE} not found")
        return
    
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    )
    channel = await connection.channel()

    try:
        if args.listen:
            logger.info("Listening for processed data...")
            await consume_processed_data(channel)
        else:
            logger.info("Sending urls to crawler...")
            await get_collections(channel)
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        await channel.close()
        await connection.close()
        logger.info("Channel closed")



if __name__ == "__main__":
    asyncio.run(main())
