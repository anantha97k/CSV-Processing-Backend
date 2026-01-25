
from main import redis_listener
import asyncio
from main import manager
 

async def test():
    await redis_listener()


asyncio.run(test())
