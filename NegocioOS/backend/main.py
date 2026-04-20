from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models  # noqa: ensures all models are registered

from routers import auth, products, sales, inventory, customers, reports, rag

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NegocioOS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(inventory.router)
app.include_router(customers.router)
app.include_router(reports.router)
app.include_router(rag.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": "NegocioOS", "version": "1.0.0"}
