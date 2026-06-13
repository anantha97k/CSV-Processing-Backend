from redis import Redis
import asyncio

pub = Redis()


async def redis_listener(manager):
    pubsub = pub.pubsub()
    pubsub.subscribe("processing", "completed")
    while True:
        message = pubsub.get_message()
        if message and message["type"] == "message":
            try:
                data = message["data"]
                data = data.decode("utf-8")
                if message["channel"] == b"processing":
                    response = {"status": "processing", "filename": data}
                    await manager.broadcast(response)
                elif message["channel"] == b"completed":
                    response = {"status": "completed", "filename": data}
                    await manager.broadcast(response)
            except BaseException:
                pass
        await asyncio.sleep(10)
