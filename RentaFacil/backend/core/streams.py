import json
import redis.asyncio as aioredis
import os
import logging
from datetime import datetime

logger = logging.getLogger("streams")

class StreamsManager:
    """Redis Streams es 10x más eficiente que PubSub normal para eventos masivos."""
    def __init__(self):
        self.redis = None

    async def connect(self):
        url = os.getenv("REDIS_PUBSUB_URL", "redis://redis:6379/1") # DB 1 para Streams
        self.redis = await aioredis.from_url(url, decode_responses=True)
        logger.info("🌊 [STREAMS] Redis Streams Conectado (Infraestructura de Alta Performance)")

    async def add_event(self, stream_name: str, data: dict):
        """XADD: Agrega un evento al rastro de Streams."""
        if self.redis:
            data["_timestamp"] = datetime.now().isoformat()
            await self.redis.xadd(stream_name, {"payload": json.dumps(data)})

    async def get_stats(self, stream_name: str):
        if self.redis:
            return await self.redis.xlen(stream_name)

    async def consume_events(self, stream_name: str, count: int = 10, block: int = 5000):
        """XREAD: Lee eventos del stream (Bloqueante para eficiencia)."""
        if self.redis:
            # Lee eventos nuevos desde el inicio (0) o el final ($)
            return await self.redis.xread({stream_name: "0-0"}, count=count, block=block)

streams_manager = StreamsManager()
