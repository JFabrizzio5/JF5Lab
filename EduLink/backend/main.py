from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models

# Import routers
from routers import auth, courses, lessons, enrollments, schedule, reviews, admin

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduLink API",
    description="YouTube-like course platform for Mexican universities",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(enrollments.router)
app.include_router(schedule.router)
app.include_router(reviews.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "EduLink API", "version": "1.0.0"}


@app.get("/")
def root():
    return {"message": "EduLink API - El YouTube de cursos universitarios"}
