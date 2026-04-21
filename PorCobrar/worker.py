import os
import asyncio
import logging
import importlib
from core.trace import request_id_ctx_var
from config.redis_config import get_redis_settings

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
APP_NAME = os.getenv("APP_NAME", "PorCobrar")

class LogFilter(logging.Filter):
    def filter(self, record):
        record.app_name = APP_NAME
        record.request_id = request_id_ctx_var.get()
        return True

format_str = "%(asctime)s - %(levelname)s - [%(app_name)s] [%(request_id)s] - %(message)s"
logging.basicConfig(level=logging.INFO, format=format_str)
for handler in logging.root.handlers: handler.addFilter(LogFilter())
logger = logging.getLogger("worker")

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.INFO)
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[sentry_logging], traces_sample_rate=1.0, enable_tracing=True, environment=ENVIRONMENT, release=f"{APP_NAME.lower()}@1.0.0")
    sentry_sdk.set_tag("app_name", APP_NAME)
    logger.info(f"🚀 {APP_NAME} (Worker) listo en {ENVIRONMENT}")

async def health_check_task(ctx):
    logger.info("💓 [HEALTH] Worker pulse OK")
    return True

functions = [health_check_task]
modules_path = os.path.join(os.path.dirname(__file__), "modules")
if os.path.exists(modules_path):
    for module_name in os.listdir(modules_path):
        tasks_path = os.path.join(modules_path, module_name, "services", "tasks.py")
        if os.path.exists(tasks_path):
            try:
                module = importlib.import_module(f"modules.{module_name}.services.tasks")
                for name in dir(module):
                    attr = getattr(module, name)
                    if callable(attr) and not name.startswith("_"):
                        functions.append(attr)
                        logger.info(f"✅ [MODULE] {module_name} -> Tarea '{name}' registrada")
            except Exception as e: logger.error(f"❌ Error cargando tareas de {module_name}: {e}")

from core.streams import streams_manager
async def stream_consumer():
    await streams_manager.connect()
    logger.info("🌊 [STREAMS] Monitor de eventos activo...")
    while True:
        try:
            if os.path.exists(modules_path):
                for module_name in os.listdir(modules_path):
                    stream_name = f"{module_name.lower()}_events"
                    events = await streams_manager.consume_events(stream_name, count=5)
                    if events:
                        for _, msg_list in events:
                            for msg_id, data in msg_list:
                                rid = data.get("request_id", "STREAM")
                                token = request_id_ctx_var.set(rid)
                                logger.info(f"📢 [EVENTO] Detectado: {data}")
                                request_id_ctx_var.reset(token)
            await asyncio.sleep(2)
        except Exception: await asyncio.sleep(5)

async def on_startup(ctx):
    logger.info(f"🚀 {APP_NAME} Worker inicializado")
    asyncio.create_task(stream_consumer())

class WorkerSettings:
    functions = functions
    redis_settings = get_redis_settings("queue")
    on_startup = on_startup
    queue_name = os.getenv("QUEUE_NAME", "arq:queue")
    max_jobs = int(os.getenv("MAX_JOBS", 10))
