import time
import os
import logging
import redis.asyncio as aioredis
from fastapi import Request, HTTPException
from core.trace import request_id_ctx_var

logger = logging.getLogger("ratelimit")

class RateLimiter:
    """
    🚀 Rate Limiter distribuido usando Redis.
    Soporta límites por Usuario (JWT) o por IP.
    """
    def __init__(self):
        self.redis = None

    async def connect(self):
        url = os.getenv("REDIS_CACHE_URL", "redis://redis:6379/0")
        self.redis = await aioredis.from_url(url, decode_responses=True)

    async def check(self, request: Request, limit: int = 60, window: int = 60):
        """
        Verifica si la petición excede el límite.
        limit: Número de peticiones permitidas.
        window: Ventana de tiempo en segundos.
        """
        if not self.redis:
            await self.connect()

        # Identificar al usuario (vía IAMMiddleware si existe) o IP
        user_id = getattr(request.state, "user_id", request.client.host)
        key = f"ratelimit:{user_id}:{request.url.path}"

        try:
            current = await self.redis.get(key)
            if current and int(current) >= limit:
                rid = request_id_ctx_var.get()
                logger.warning(f"⚠️ [{rid}] Rate limit excedido para {user_id} en {request.url.path}")
                raise HTTPException(status_code=429, detail="Too many requests. Try again later.")

            # Incrementar y establecer expiración si es nuevo
            async with self.redis.pipeline(transaction=True) as pipe:
                await pipe.incr(key)
                await pipe.expire(key, window)
                await pipe.execute()
            return True
        except Exception as e:
            if isinstance(e, HTTPException): raise e
            logger.error(f"❌ Error en RateLimiter: {e}")
            return True # Fall-safe: Permitir si Redis falla

limiter = RateLimiter()
