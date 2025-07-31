import aio_pika
import asyncio
import json

RABBITMQ_URL = "amqp://guest:guest@0.0.0.0:5672"

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


async def main(host: str="localhost", port: int=5672, login: str="guest", password: str = "guest"):
    connection = await aio_pika.connect_robust(host=host, port=port, login=login, password=password)
    channel = await connection.channel()

    tasks = [consume_processed_data(channel), send_url(channel, "https://dondesang.efs.sante.fr/trouver-une-collecte/138202/sang")]
    await asyncio.gather(*tasks)

    await connection.close()

if __name__ == "__main__":
    asyncio.run(main(host="localhost"))