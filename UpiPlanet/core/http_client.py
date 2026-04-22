import httpx
from core.trace import request_id_ctx_var

class TracedAsyncClient(httpx.AsyncClient):
    """
    Cliente HTTP que inyecta automáticamente el X-Request-ID en 
    todas las peticiones salientes para mantener la trazabilidad distribuida.
    """
    async def request(self, method: str, url: httpx._types.URLTypes, **kwargs):
        headers = kwargs.get("headers", {})
        # Inyectar Correlation ID actual
        current_id = request_id_ctx_var.get()
        if current_id and current_id != "CORE":
            headers["X-Request-ID"] = current_id
        
        kwargs["headers"] = headers
        return await super().request(method, url, **kwargs)

# Instancia global reutilizable (usar en vez de httpx.AsyncClient directo)
http_client = TracedAsyncClient(timeout=30.0)
