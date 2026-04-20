from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models

# Import routers
from routers import auth, conventions, stages, speakers, stands, sponsors, tickets, tournaments, payments, public

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ConventionOS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(conventions.router)
app.include_router(stages.router)
app.include_router(speakers.router)
app.include_router(stands.router)
app.include_router(sponsors.router)
app.include_router(tickets.router)
app.include_router(tournaments.router)
app.include_router(payments.router)
app.include_router(public.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ConventionOS API"}
