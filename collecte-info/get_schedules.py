import aio_pika
import asyncio
import json

from settings import settings

async def consume_processed_data(channel: aio_pika.Channel):
    queue = await channel.get_queue("processed_data")

    async for message in queue:
        async with message.process():
            data = json.loads(message.body.decode())
            print("Received data:", data, flush=True)

async def send_url(channel: aio_pika.Channel, url: str):
    queue = await channel.get_queue("crawler_urls")
    await channel.default_exchange.publish(
        aio_pika.Message(body=url.encode()),
        routing_key=queue.name,
    )


async def main():
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    )
    channel = await connection.channel()

    tasks = [consume_processed_data(channel), send_url(channel, "https://dondesang.efs.sante.fr/trouver-une-collecte/138202/sang")]
    await asyncio.gather(*tasks)

    await connection.close()

if __name__ == "__main__":
    asyncio.run(main())
