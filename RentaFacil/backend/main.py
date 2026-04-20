from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

app = FastAPI(title="RentaFácil API", version="1.0.0", description="Property rental management for LATAM landlords")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from modules.auth.api.v1.routes import router as auth_router
from modules.properties.api.v1.routes import router as properties_router
from modules.tenants.api.v1.routes import tenants_router, contracts_router
from modules.payments.api.v1.routes import router as payments_router
from modules.reports.api.v1.routes import router as reports_router

app.include_router(auth_router)
app.include_router(properties_router)
app.include_router(tenants_router)
app.include_router(contracts_router)
app.include_router(payments_router)
app.include_router(reports_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "rentafacil"}
