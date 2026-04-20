import json
import redis.asyncio as aioredis
import os
import functools
import logging

logger = logging.getLogger("cache")

class CacheManager:
    """🚀 Manejador de Cache Global - Implementa @cached()"""
    def __init__(self):
        self.redis = None

    async def connect(self):
        url = os.getenv("REDIS_CACHE_URL", "redis://redis:6379/0") # DB 0 para Cache
        self.redis = await aioredis.from_url(url, decode_responses=True)
        logger.info("⚡ [CACHE] Redis Cache Conectado (Optimización Activa)")

    async def get(self, key: str):
        if not self.redis: return None
        value = await self.redis.get(f"cache:{key}")
        return json.loads(value) if value else None

    async def set(self, key: str, value: any, ttl: int = 300):
        if self.redis:
            await self.redis.setex(f"cache:{key}", ttl, json.dumps(value))

    def cached(self, ttl: int = 300):
        """Tutorial: @cached(ttl=60) sobre cualquier función asíncrona."""
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                key = f"{func.__name__}:{args}:{kwargs}"
                cached_val = await self.get(key)
                if cached_val: return cached_val
                result = await func(*args, **kwargs)
                await self.set(key, result, ttl)
                return result
            return wrapper
        return decorator

cache_manager = CacheManager()
