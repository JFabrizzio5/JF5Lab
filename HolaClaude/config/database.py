import asyncio
import os
from fastapi import HTTPException

# Carga de Ambiente Dynamica (dev / prod / docker)
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

async def get_db_url(db_type: str) -> str:
    """Devuelve la configuración local (dev/prod) o llama al IAM si no está definida."""
    env_suffix = f"_{ENVIRONMENT.upper()}" if ENVIRONMENT else "_DEV"
    if db_type == "sql":
        url = os.getenv(f"DATABASE_URL{env_suffix}")
        if url: return url
        return os.getenv("DATABASE_URL_DEV") # Fallback local
    if db_type == "excel":
        url = os.getenv(f"EXCEL_STORAGE_PATH{env_suffix}") or os.getenv("EXCEL_STORAGE_PATH")
        if url: return url
        return os.path.join("storage", "data.xlsx")
    else:
        url = os.getenv(f"MONGODB_URL{env_suffix}")
        if url: return url
        return os.getenv("MONGODB_URL_DEV")

async def check_db_health() -> dict:
    """Verifica la conectividad real con las bases de datos configuradas."""
    results = {}

    # Verificar SQL
    try:
        from sqlalchemy import text
        await init_sql_engine()
        async with _AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        results["sql"] = "Conectado"
    except Exception as e:
        results["sql"] = f"Error: {str(e)}"
    return results

Base = None

# ==========================================
# Configuración PostgreSQL (SQLAlchemy)
# ==========================================
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Base para todos los modelos del proyecto (Necesaria para Alembic)
Base = declarative_base()

_sql_engine = None
_AsyncSessionLocal = None

async def init_sql_engine():
    global _sql_engine, _AsyncSessionLocal
    if not _sql_engine:
        url = await get_db_url("sql")
        _sql_engine = create_async_engine(
            url, 
            echo=(ENVIRONMENT == "dev"),
            pool_size=20
        )
        
        # Activar soporte vectorial en PostgreSQL automáticamente
        from sqlalchemy import text
        try:
            async with _sql_engine.begin() as conn:
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        except Exception as e:
            pass # Si el usuario no tiene permisos o ya existe, omitir
            
        _AsyncSessionLocal = sessionmaker(
            bind=_sql_engine, class_=AsyncSession, expire_on_commit=False
        )

async def get_sql_db(tenant_id: str = None):
    await init_sql_engine()
    async with _AsyncSessionLocal() as session:
        if tenant_id:
            from sqlalchemy import text
            import re
            # Validación estricta para evitar SQL Injection en el search_path
            if not re.match(r"^[a-zA-Z0-9_]+$", tenant_id):
                raise ValueError("Formato de tenant_id inválido")
            await session.execute(text(f'SET search_path TO "tenant_{tenant_id}"'))
        yield session
