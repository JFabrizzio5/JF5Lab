import os
import re
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
Base = declarative_base()

_sql_engine = None
_AsyncSessionLocal = None


async def get_db_url(db_type: str = "sql") -> str:
    env_suffix = f"_{ENVIRONMENT.upper()}" if ENVIRONMENT else "_DEV"
    if db_type == "sql":
        return os.getenv(f"DATABASE_URL{env_suffix}") or os.getenv("DATABASE_URL_DEV")
    return os.getenv("MONGODB_URL_DEV")


async def init_sql_engine():
    global _sql_engine, _AsyncSessionLocal
    if _sql_engine:
        return
    url = await get_db_url("sql")
    # PgBouncer transaction mode requires statement_cache_size=0 on asyncpg
    connect_args = {"statement_cache_size": 0} if "pgbouncer" in (url or "") else {}
    _sql_engine = create_async_engine(
        url,
        echo=(ENVIRONMENT == "dev"),
        pool_size=20,
        connect_args=connect_args,
    )
    try:
        async with _sql_engine.begin() as conn:
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
    except Exception:
        pass
    _AsyncSessionLocal = sessionmaker(bind=_sql_engine, class_=AsyncSession, expire_on_commit=False)


UUID_RE = re.compile(r"^[0-9a-fA-F-]{32,36}$")


async def get_sql_db(tenant_id: str | None = None):
    await init_sql_engine()
    async with _AsyncSessionLocal() as session:
        if tenant_id:
            if not UUID_RE.match(tenant_id):
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail="tenant_id invalido")
            await session.execute(text("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=tenant_id))
        yield session


async def check_db_health() -> dict:
    try:
        await init_sql_engine()
        async with _AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"sql": "ok"}
    except Exception as e:
        return {"sql": f"error: {e}"}
