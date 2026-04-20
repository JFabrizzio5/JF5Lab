from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from config.settings import settings

Base = declarative_base()

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), server_default=func.now()
    )

_engine = None
_AsyncSessionLocal = None

def _get_engine():
    global _engine, _AsyncSessionLocal
    if not _engine:
        url = settings.database_url
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        _engine = create_async_engine(url, echo=(settings.environment == "dev"), pool_size=20)
        _AsyncSessionLocal = sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)
    return _engine

async def get_db():
    _get_engine()
    async with _AsyncSessionLocal() as session:
        yield session
