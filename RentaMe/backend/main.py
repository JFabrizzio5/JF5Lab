from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

from routers import auth, vendors, items, availability, bookings, payments, public, admin

app = FastAPI(title="RentaMe API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "RentaMe API"}


app.include_router(auth.router)
app.include_router(vendors.router)
app.include_router(items.router)
app.include_router(availability.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(public.router)
app.include_router(admin.router)
