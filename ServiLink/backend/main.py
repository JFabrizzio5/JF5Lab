from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

from routers import auth, professionals, bookings, reviews, categories, subscriptions, admin, chat, public

app = FastAPI(
    title="ServiLink API",
    description="Marketplace de servicios profesionales — tipo Rappi pero de servicios",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(professionals.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(categories.router)
app.include_router(subscriptions.router)
app.include_router(admin.router)
app.include_router(chat.router)
app.include_router(public.router)


@app.get("/")
def root():
    return {"status": "ok", "app": "ServiLink API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
