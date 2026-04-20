from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/events", tags=["events"])


class BookingCreate(BaseModel):
    client_id: int
    space_id: Optional[int] = None
    title: str
    event_type: str = "boda"
    start_datetime: datetime
    end_datetime: datetime
    guests_count: int = 0
    status: str = "inquiry"
    total_price: float = 0.0
    deposit_amount: float = 0.0
    notes: Optional[str] = None


class BookingUpdate(BaseModel):
    space_id: Optional[int] = None
    title: Optional[str] = None
    event_type: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    guests_count: Optional[int] = None
    status: Optional[str] = None
    total_price: Optional[float] = None
    deposit_amount: Optional[float] = None
    notes: Optional[str] = None


def booking_out(b: models.EventBooking, db: Session = None):
    out = {
        "id": b.id,
        "venue_id": b.venue_id,
        "space_id": b.space_id,
        "client_id": b.client_id,
        "title": b.title,
        "event_type": b.event_type,
        "start_datetime": b.start_datetime.isoformat() if b.start_datetime else None,
        "end_datetime": b.end_datetime.isoformat() if b.end_datetime else None,
        "guests_count": b.guests_count,
        "status": b.status,
        "total_price": b.total_price,
        "deposit_amount": b.deposit_amount,
        "notes": b.notes,
        "created_at": b.created_at.isoformat() if b.created_at else None,
    }
    if b.client:
        out["client_name"] = b.client.name
        out["client_email"] = b.client.email
        out["client_phone"] = b.client.phone
    if b.space:
        out["space_name"] = b.space.name
    return out


@router.get("/")
def list_events(
    status: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    q = db.query(models.EventBooking).filter(
        models.EventBooking.venue_id == venue.id
    )
    if status:
        q = q.filter(models.EventBooking.status == status)
    if date_from:
        q = q.filter(models.EventBooking.start_datetime >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        q = q.filter(models.EventBooking.start_datetime <= datetime.combine(date_to, datetime.max.time()))
    bookings = q.order_by(models.EventBooking.start_datetime.asc()).all()
    return [booking_out(b) for b in bookings]


@router.get("/calendar")
def calendar_events(
    year: int = Query(...),
    month: int = Query(...),
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    from calendar import monthrange
    _, days = monthrange(year, month)
    start = datetime(year, month, 1)
    end = datetime(year, month, days, 23, 59, 59)
    bookings = db.query(models.EventBooking).filter(
        models.EventBooking.venue_id == venue.id,
        models.EventBooking.start_datetime >= start,
        models.EventBooking.start_datetime <= end,
    ).all()
    return [booking_out(b) for b in bookings]


@router.post("/")
def create_event(
    data: BookingCreate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    booking = models.EventBooking(venue_id=venue.id, **data.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking_out(booking)


@router.put("/{booking_id}")
def update_event(
    booking_id: int,
    data: BookingUpdate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    booking = db.query(models.EventBooking).filter(
        models.EventBooking.id == booking_id,
        models.EventBooking.venue_id == venue.id,
    ).first()
    if not booking:
        raise HTTPException(404, "Reserva no encontrada")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(booking, field, value)
    db.commit()
    db.refresh(booking)
    return booking_out(booking)


@router.get("/stats")
def get_stats(
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    now = datetime.utcnow()
    from datetime import timedelta
    next_30 = now + timedelta(days=30)
    start_month = now.replace(day=1, hour=0, minute=0, second=0)

    total_clients = db.query(models.Client).filter(models.Client.venue_id == venue.id).count()
    upcoming = db.query(models.EventBooking).filter(
        models.EventBooking.venue_id == venue.id,
        models.EventBooking.start_datetime >= now,
        models.EventBooking.start_datetime <= next_30,
        models.EventBooking.status.notin_(["cancelled"]),
    ).count()

    payments = db.query(models.Payment).filter(
        models.Payment.venue_id == venue.id,
        models.Payment.status == "succeeded",
        models.Payment.created_at >= start_month,
    ).all()
    revenue_month = sum(p.venue_amount for p in payments)

    statuses = ["inquiry", "quote_sent", "confirmed", "deposit_paid", "completed", "cancelled"]
    by_status = {}
    for s in statuses:
        by_status[s] = db.query(models.EventBooking).filter(
            models.EventBooking.venue_id == venue.id,
            models.EventBooking.status == s,
        ).count()

    recent_bookings = db.query(models.EventBooking).filter(
        models.EventBooking.venue_id == venue.id,
    ).order_by(models.EventBooking.created_at.desc()).limit(10).all()

    return {
        "total_clients": total_clients,
        "upcoming_events": upcoming,
        "revenue_month": revenue_month,
        "by_status": by_status,
        "recent_activity": [booking_out(b) for b in recent_bookings],
    }
