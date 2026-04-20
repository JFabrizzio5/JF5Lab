from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/bookings", tags=["bookings"])


def booking_to_dict(b: models.Booking):
    return {
        "id": b.id,
        "client_id": b.client_id,
        "professional_id": b.professional_id,
        "category_id": b.category_id,
        "description": b.description,
        "status": b.status,
        "client_address": b.client_address,
        "client_lat": b.client_lat,
        "client_lng": b.client_lng,
        "price": b.price,
        "scheduled_at": b.scheduled_at.isoformat() if b.scheduled_at else None,
        "created_at": b.created_at.isoformat() if b.created_at else None,
        "client": {"id": b.client.id, "name": b.client.name, "avatar_url": b.client.avatar_url} if b.client else None,
        "professional": {"id": b.professional.id, "name": b.professional.name, "avatar_url": b.professional.avatar_url} if b.professional else None,
        "category": {"id": b.category.id, "name": b.category.name, "icon": b.category.icon} if b.category else None,
        "has_review": b.review is not None,
    }


class BookingCreate(BaseModel):
    professional_id: int
    category_id: int
    description: Optional[str] = None
    client_address: Optional[str] = None
    client_lat: Optional[float] = None
    client_lng: Optional[float] = None
    scheduled_at: Optional[datetime] = None


@router.post("/")
def create_booking(
    data: BookingCreate,
    current_user: models.User = Depends(auth_utils.require_role("client")),
    db: Session = Depends(get_db)
):
    professional_user = db.query(models.User).filter(
        models.User.id == data.professional_id,
        models.User.role == "freelancer"
    ).first()
    if not professional_user:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")

    prof_profile = db.query(models.ProfessionalProfile).filter(
        models.ProfessionalProfile.user_id == data.professional_id
    ).first()

    price = prof_profile.hourly_rate if prof_profile else 0.0

    booking = models.Booking(
        client_id=current_user.id,
        professional_id=data.professional_id,
        category_id=data.category_id,
        description=data.description,
        client_address=data.client_address,
        client_lat=data.client_lat,
        client_lng=data.client_lng,
        price=price,
        scheduled_at=data.scheduled_at,
        status="pending",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    booking = db.query(models.Booking).options(
        joinedload(models.Booking.client),
        joinedload(models.Booking.professional),
        joinedload(models.Booking.category),
        joinedload(models.Booking.review),
    ).filter(models.Booking.id == booking.id).first()

    return booking_to_dict(booking)


@router.get("/")
def list_my_bookings(
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Booking).options(
        joinedload(models.Booking.client),
        joinedload(models.Booking.professional),
        joinedload(models.Booking.category),
        joinedload(models.Booking.review),
    )

    if current_user.role == "client":
        bookings = query.filter(models.Booking.client_id == current_user.id).order_by(models.Booking.created_at.desc()).all()
    elif current_user.role == "freelancer":
        bookings = query.filter(models.Booking.professional_id == current_user.id).order_by(models.Booking.created_at.desc()).all()
    elif current_user.role == "superadmin":
        bookings = query.order_by(models.Booking.created_at.desc()).all()
    else:
        bookings = []

    return [booking_to_dict(b) for b in bookings]


@router.patch("/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    status: str,
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    valid_transitions = {
        "freelancer": {
            "pending": ["accepted", "cancelled"],
            "accepted": ["in_progress", "cancelled"],
            "in_progress": ["completed"],
        },
        "client": {
            "pending": ["cancelled"],
        },
        "superadmin": {
            "pending": ["accepted", "cancelled"],
            "accepted": ["in_progress", "cancelled"],
            "in_progress": ["completed", "cancelled"],
            "completed": [],
        }
    }

    role_transitions = valid_transitions.get(current_user.role, {})
    allowed = role_transitions.get(booking.status, [])

    if status not in allowed:
        raise HTTPException(status_code=400, detail=f"Transición inválida: {booking.status} → {status}")

    if current_user.role == "freelancer" and booking.professional_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    if current_user.role == "client" and booking.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    booking.status = status
    booking.updated_at = datetime.utcnow()

    if status == "completed":
        prof = db.query(models.ProfessionalProfile).filter(
            models.ProfessionalProfile.user_id == booking.professional_id
        ).first()
        if prof:
            prof.total_jobs += 1

    db.commit()
    db.refresh(booking)

    booking = db.query(models.Booking).options(
        joinedload(models.Booking.client),
        joinedload(models.Booking.professional),
        joinedload(models.Booking.category),
        joinedload(models.Booking.review),
    ).filter(models.Booking.id == booking.id).first()

    return booking_to_dict(booking)
