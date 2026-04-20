import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from database import init_db, engine
from models import Editor, Plan, PlanType
from auth import hash_password
from routers.auth_router import router as auth_router
from routers.editors_router import router as editors_router
from routers.reviews_router import router as reviews_router
from routers.billing_router import router as billing_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EditorialManager")

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8012"))


DEFAULT_PLANS = [
    {"name": PlanType.free, "display_name": "Free", "price_monthly": 0, "price_yearly": 0, "max_editors": 1, "max_reviews": 10},
    {"name": PlanType.starter, "display_name": "Starter", "price_monthly": 1900, "price_yearly": 19000, "max_editors": 5, "max_reviews": 100},
    {"name": PlanType.pro, "display_name": "Pro", "price_monthly": 4900, "price_yearly": 49000, "max_editors": 20, "max_reviews": 500},
    {"name": PlanType.enterprise, "display_name": "Enterprise", "price_monthly": 14900, "price_yearly": 149000, "max_editors": -1, "max_reviews": -1},
]


async def seed_data():
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as db:
        # Seed plans
        for plan_data in DEFAULT_PLANS:
            result = await db.execute(select(Plan).where(Plan.name == plan_data["name"]))
            if not result.scalar_one_or_none():
                db.add(Plan(**plan_data))

        # Seed admin
        result = await db.execute(select(Editor).where(Editor.email == "admin@editorial.com"))
        if not result.scalar_one_or_none():
            db.add(Editor(
                name="Admin",
                email="admin@editorial.com",
                hashed_password=hash_password("admin123"),
                role="admin",
                is_active=True
            ))
            logger.info("Default admin: admin@editorial.com / admin123")

        await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 50)
    logger.info("  EDITORIAL MANAGER — Starting")
    logger.info(f"  Port: {APP_PORT}")
    logger.info("=" * 50)
    await init_db()
    await seed_data()
    yield
    logger.info("Editorial Manager stopped")


app = FastAPI(
    title="Editorial Manager API",
    description="Gestión de editores y procesos de revisión — SaaS ready",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(editors_router)
app.include_router(reviews_router)
app.include_router(billing_router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Editorial Manager API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=False)
