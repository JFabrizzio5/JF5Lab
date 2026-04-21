import logging
import json
import asyncio
import os
import redis.asyncio as aioredis
from typing import List, Dict
from fastapi import WebSocket

logger = logging.getLogger("websockets")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis = None
        self.pubsub = None
        self.channel_name = "ws_global_broadcast"

    async def connect_redis(self):
        url = os.getenv("REDIS_PUBSUB_URL", "redis://redis:6379/1")
        self.redis = await aioredis.from_url(url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(self.channel_name)
        asyncio.create_task(self._listen_to_redis())
        logger.info("🔌 [WS] Conectado a Redis Backplane para WebSockets")

    async def _listen_to_redis(self):
        """Escucha mensajes de otros servidores y los envía a clientes locales."""
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    data = json.loads(message["data"])
                    await self._local_broadcast(data["payload"])
        except Exception as e:
            logger.error(f"❌ [WS] Error en Redis Backplane: {e}")

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)

    def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)

    async def broadcast(self, message: str):
        """Publica el mensaje a Redis para que llegue a TODOS los servidores."""
        if self.redis:
            await self.redis.publish(self.channel_name, json.dumps({"payload": message}))
        else:
            await self._local_broadcast(message)

    async def _local_broadcast(self, message: str):
        """Envía el mensaje solo a las conexiones de este servidor."""
        for connections in self.active_connections.values():
            for connection in connections:
                try:
                    await connection.send_text(message)
                except:
                    pass

manager = ConnectionManager()
