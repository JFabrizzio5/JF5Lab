import os
import httpx
import logging
import sentry_sdk
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.trace import request_id_ctx_var

logger = logging.getLogger("internal_client")

class InternalServiceClient:
    """
    🚀 Cliente principal para comunicación entre microservicios.
    Maneja automáticamente Auth Forwarding, Trazabilidad y RESILIENCIA.
    """
    def __init__(self, service_name: str, base_url: Optional[str] = None):
        self.service_name = service_name.upper()
        # Descubrimiento: Prioriza base_url manual, luego variable de entorno
        self.base_url = base_url or os.getenv(f"API_{self.service_name}_URL")
        self.timeout = httpx.Timeout(30.0, connect=5.0)
        
        if not self.base_url:
            logger.warning(f"⚠️ [INTERNAL] URL para servicio {self.service_name} no configurada (API_{self.service_name}_URL)")

    def _get_headers(self, user_token: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "X-Request-ID": request_id_ctx_var.get() or "INTERNAL",
            "Content-Type": "application/json"
        }
        
        # 1. Forwarding: Si recibimos un token de usuario, lo propagamos
        if user_token:
            headers["Authorization"] = f"Bearer {user_token}"
        # 2. M2M: Si no hay usuario, usamos la App Key interna para Auth de sistema
        else:
            internal_key = os.getenv("INTERNAL_APP_KEY")
            if internal_key:
                headers["X-Internal-Key"] = internal_key
        
        # 3. Sentry Tracing: Propagación de rastro distribuido
        with sentry_sdk.configure_scope() as scope:
            # Sentry inyecta automáticamente 'sentry-trace' y 'baggage' si hay un hub activo
            pass 
                
        return headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException, httpx.RemoteProtocolError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def request(
        self, 
        method: str, 
        endpoint: str, 
        user_token: Optional[str] = None, 
        **kwargs
    ) -> httpx.Response:
        """
        Ejecuta una petición asíncrona con reintentos automáticos (Phase 3).
        Propaga el contexto de Sentry para trazabilidad distribuida (Phase 4).
        """
        if not self.base_url:
            raise Exception(f"URL de servicio {self.service_name} no definida")

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = self._get_headers(user_token)
        
        # Combinar headers adicionales si existen
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        # Sentry: Propagación de cabeceras de trazabilidad
        sentry_headers = sentry_sdk.get_traceparent()
        if sentry_headers:
            headers["sentry-trace"] = sentry_headers
        
        baggage = sentry_sdk.get_baggage()
        if baggage:
            headers["baggage"] = baggage

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                # Si es 5xx, reintentamos (aquí podrías filtrar si quieres reintentar 500s)
                if e.response.status_code >= 500:
                    logger.warning(f"⚠️ [INTERNAL] Reintentando por error {e.response.status_code} en {self.service_name}...")
                    raise e
                logger.error(f"❌ [INTERNAL] Error {e.response.status_code} llamando a {self.service_name}: {e.response.text}")
                raise e
            except Exception as e:
                logger.error(f"❌ [INTERNAL] Error de conexión con {self.service_name}: {e}")
                raise e

    async def get(self, endpoint: str, **kwargs): return await self.request("GET", endpoint, **kwargs)
    async def post(self, endpoint: str, **kwargs): return await self.request("POST", endpoint, **kwargs)
    async def put(self, endpoint: str, **kwargs): return await self.request("PUT", endpoint, **kwargs)
    async def delete(self, endpoint: str, **kwargs): return await self.request("DELETE", endpoint, **kwargs)

# Factory para crear clientes de forma sencilla
def get_service_client(service_name: str) -> InternalServiceClient:
    return InternalServiceClient(service_name)
