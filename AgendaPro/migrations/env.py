import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys

sys.path.append(os.getcwd())
from config.database import ENVIRONMENT, Base

# --- AUTO-DISCOVERY DE MODELOS ---
def import_all_models():
    import importlib
    import os
    modules_path = os.path.join(os.getcwd(), "modules")
    if os.path.exists(modules_path):
        for module_name in os.listdir(modules_path):
            try:
                # Importamos el paquete 'models' para captar todo lo registrado en __init__.py
                importlib.import_module(f"modules.{module_name}.models")
            except ImportError:
                continue

import_all_models()
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    from dotenv import load_dotenv
    load_dotenv()
    # Alembic runs DDL including RLS policies → usar rol admin
    admin = os.getenv("DATABASE_URL_ADMIN")
    if admin:
        return admin
    suffix = f"_{ENVIRONMENT.upper()}" if ENVIRONMENT else "_DEV"
    return os.getenv(f"DATABASE_URL{suffix}") or os.getenv("DATABASE_URL_DEV")

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()
    connectable = async_engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
