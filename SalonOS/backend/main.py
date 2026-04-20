from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models

# Import routers
from routers import auth, venues, spaces, clients, events, payments, chat, public

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SalonOS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(venues.router)
app.include_router(spaces.router)
app.include_router(clients.router)
app.include_router(events.router)
app.include_router(payments.router)
app.include_router(chat.router)
app.include_router(public.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "SalonOS API"}
