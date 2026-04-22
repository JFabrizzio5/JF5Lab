import os
import logging
import redis.asyncio as aioredis
from config.redis_config import get_redis_settings

logger = logging.getLogger("monitor")

class MonitorManager:
    """🚀 Monitor de Colas - Inspección en tiempo real de Arq"""
    def __init__(self):
        self.redis = None
        self.queue_name = os.getenv("QUEUE_NAME", "arq:queue")

    async def connect(self):
        settings = get_redis_settings("queue")
        url = f"redis://:{settings.password}@{settings.host}:{settings.port}/{settings.database}" if settings.password else f"redis://{settings.host}:{settings.port}/{settings.database}"
        self.redis = await aioredis.from_url(url, decode_responses=False)
        logger.info(f"📊 [MONITOR] Conectado a {self.queue_name}")


    async def get_stats(self):
        """Retorna estadísticas resumidas de la cola y trabajos completados."""
        depth = await self.get_queue_depth()
        # Intentar obtener contadores de Redis
        success = 0
        failed = 0
        if self.redis:
            val_s = await self.redis.get(f"{self.queue_name}:success")
            val_f = await self.redis.get(f"{self.queue_name}:failed")
            success = int(val_s) if val_s else 0
            failed = int(val_f) if val_f else 0

        return {
            "queue": self.queue_name,
            "pending_jobs": depth,
            "jobs_completed": success,
            "jobs_failed": failed,
            "status": "healthy" if self.redis else "disconnected"
        }

    async def report_success(self):
        """Incrementa el contador de éxitos en Redis."""
        if self.redis:
            await self.redis.incr(f"{self.queue_name}:success")

    async def report_failure(self):
        """Incrementa el contador de fallos en Redis."""
        if self.redis:
            await self.redis.incr(f"{self.queue_name}:failed")

monitor_manager = MonitorManager()
