import os
from arq.connections import RedisSettings

# URLs especializadas para evitar ruido entre servicios
REDIS_CACHE_URL = os.getenv("REDIS_CACHE_URL", "redis://redis:6379/0")
REDIS_PUBSUB_URL = os.getenv("REDIS_PUBSUB_URL", "redis://redis:6379/1")
REDIS_QUEUE_URL = os.getenv("REDIS_QUEUE_URL", "redis://redis:6379/2")

def get_redis_settings(url_type="queue"):
    """Parsea el DSN de Redis para devolver la configuración compatible con ARQ/Otras."""
    from urllib.parse import urlparse
    import os
    
    # Lectura dinámica para asegurar que load_dotenv() ya haya corrido
    c_url = os.getenv("REDIS_CACHE_URL", "redis://redis:6379/0")
    p_url = os.getenv("REDIS_PUBSUB_URL", "redis://redis:6379/1")
    q_url = os.getenv("REDIS_QUEUE_URL", "redis://redis:6379/2")
    
    url_str = q_url if url_type == "queue" else p_url
    if url_type == "cache": url_str = c_url
    
    url = urlparse(url_str)
    return RedisSettings(
        host=url.hostname or 'redis',
        port=url.port or 6379,
        database=int(url.path.strip('/') or 0),
        password=url.password
    )
