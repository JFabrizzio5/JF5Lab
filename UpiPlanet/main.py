import os
import uuid
import asyncio
import logging
from contextlib import asynccontextmanager
from core.trace import request_id_ctx_var

# 1. CARGA TEMPRANA DE ENTORNO
from dotenv import load_dotenv
load_dotenv() # Carga el archivo .env maestro
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
load_dotenv(f".env.{ENVIRONMENT}", override=True) # Sobrescribe con el específico

import sentry_sdk
from sentry_sdk import metrics
from sentry_sdk.integrations.logging import LoggingIntegration
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from config.redis_config import get_redis_settings
from core.ratelimit import limiter

# --- CONFIGURACIÓN DE TRAZABILIDAD ---
APP_NAME = os.getenv("APP_NAME", "UpiPlanet")

class LogFilter(logging.Filter):
    def filter(self, record):
        record.app_name = APP_NAME
        record.request_id = request_id_ctx_var.get()
        return True

# Formato: [TIEMPO] [NIVEL] [APP_NAME] [ID_PETICION] Mensaje
format_str = "%(asctime)s - %(levelname)s - [%(app_name)s] [%(request_id)s] - %(message)s"
logging.basicConfig(level=logging.INFO, format=format_str)
for handler in logging.root.handlers:
    handler.addFilter(LogFilter())
logger = logging.getLogger("api_main")

# --- SENTRY SETUP ---
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_SAMPLE_RATE = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")) # Leer del .env

if SENTRY_DSN:
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging],
        traces_sample_rate=SENTRY_SAMPLE_RATE, # Asignación dinámica
        enable_tracing=True,
        environment=ENVIRONMENT,
        release=f"{APP_NAME.lower()}@1.0.0",
        debug=False,
        enable_logs=True
    )
    sentry_sdk.set_tag("app_name", APP_NAME)
    logger.info(f"🚀 {APP_NAME} inicializado en {ENVIRONMENT} con Sentry Logs")
    sentry_sdk.capture_message(f"🚀 {APP_NAME} inicializado en {ENVIRONMENT}")



# --- MIDDLEWARE DE REQUEST ID ---
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net"
        if ENVIRONMENT == "prod":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        token = request_id_ctx_var.set(rid)
        try:
            sentry_sdk.set_tag("request_id", rid)
            response = await call_next(request)
            response.headers["X-Request-ID"] = rid
            return response
        finally:
            request_id_ctx_var.reset(token)

from prometheus_client import Gauge, Counter
ARQ_QUEUE_DEPTH = Gauge("arq_queue_depth", "Jobs pending in Arq queue")
ARQ_SUCCESS_TOTAL = Counter("arq_success_total", "Total successful jobs")
ARQ_FAILED_TOTAL = Counter("arq_failed_total", "Total failed jobs")

async def arq_stats_poller():
    """Actualiza las métricas de Prometheus cada 5 segundos."""
    last_success = 0
    last_failed = 0
    while True:
        try:
            from core.monitor import monitor_manager
            stats = await monitor_manager.get_stats()
            ARQ_QUEUE_DEPTH.set(stats.get("pending_jobs", 0))
            diff_s = stats.get("jobs_completed", 0) - last_success
            if diff_s > 0:
                ARQ_SUCCESS_TOTAL.inc(diff_s)
                last_success = stats.get("jobs_completed", 0)
            diff_f = stats.get("jobs_failed", 0) - last_failed
            if diff_f > 0:
                ARQ_FAILED_TOTAL.inc(diff_f)
                last_failed = stats.get("jobs_failed", 0)
        except Exception:
            pass
        await asyncio.sleep(5)



# --- LIFESPAN (Infra Kickstart) ---
from core.cache import cache_manager
from core.streams import streams_manager
from core.monitor import monitor_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Iniciando {APP_NAME} en modo {ENVIRONMENT}")
    
    # FASE 0: Bootstrap Remoto
    pass # FASE 0: Sin IAM

    for attempt in range(5):
        try:
            await cache_manager.connect()
            await streams_manager.connect()
            await monitor_manager.connect()
            await limiter.connect()
            from core.websockets import manager as ws_manager
            await ws_manager.connect_redis()
            asyncio.create_task(arq_stats_poller())
            logger.info("✅ [INFRA] Infraestructura Core Conectada exitosamente")
            break
        except Exception as e:
            logger.warning(f"⏳ [INFRA] Esperando a Redis/Infra (Intento {attempt+1}/5): {e}")
            await asyncio.sleep(2)
    else:
        logger.error("❌ [INFRA] Fallo crítico: La app arrancó en modo degradado (Sin Redis).")
    yield

app = FastAPI(title=f"{APP_NAME} API", lifespan=lifespan)
app.add_middleware(RequestIDMiddleware)

app.add_middleware(SecurityHeadersMiddleware)
cors_origins = [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Instrumentator().instrument(app).expose(app)

@app.get("/queue/stats")
async def queue_stats():
    return await monitor_manager.get_stats()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    rid = request_id_ctx_var.get()
    logger.error(f"💥 [{rid}] Error no controlado: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "INTERNAL_SERVER_ERROR", "request_id": rid})

@app.get("/health")
async def health():
    return {"status": "ok", "app": APP_NAME, "id": request_id_ctx_var.get()}

@app.get("/test-sentry")
async def test_sentry():
    logger.info("🧪 Generando rastro (breadcrumb) con el ID actual")
    logger.error("❌ Error de prueba para Sentry con ID de seguimiento")
    raise ValueError(f"Fallo detectado en {APP_NAME}")

@app.get("/test-metrics")
async def test_metrics():
    metrics.count("checkout.failed", 1, attributes={"env": ENVIRONMENT})
    metrics.gauge("queue.depth", 42, attributes={"app": APP_NAME})
    metrics.distribution("cart.amount_usd", 187.5, unit="dollar")
    return {"status": "metrics_sent", "details": ["checkout.failed", "queue.depth", "cart.amount_usd"]}

modules_path = os.path.join(os.path.dirname(__file__), "modules")
if os.path.exists(modules_path):
    import importlib
    for module_name in os.listdir(modules_path):
        mod_dir = os.path.join(modules_path, module_name)
        if os.path.isdir(mod_dir) and not module_name.startswith("__"):
            api_path = os.path.join(mod_dir, "api")
            if os.path.exists(api_path):
                for version in os.listdir(api_path):
                    v_dir = os.path.join(api_path, version)
                    if os.path.isdir(v_dir) and not version.startswith("__"):
                        try:
                            route_mod = importlib.import_module(f"modules.{module_name}.api.{version}.routes")
                            app.include_router(route_mod.router, prefix=f"/{module_name.lower()}/{version}", tags=[f"{module_name.capitalize()} {version.upper()}"])
                            try:
                                ws_mod = importlib.import_module(f"modules.{module_name}.api.{version}.websocket")
                                app.include_router(ws_mod.router)
                            except ImportError: pass
                        except Exception as e: logger.error(f"❌ Error cargando módulo {module_name} ({version}): {e}")
