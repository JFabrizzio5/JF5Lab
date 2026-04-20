from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    source: str = "web"


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None


def client_out(c: models.Client):
    return {
        "id": c.id,
        "venue_id": c.venue_id,
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "notes": c.notes,
        "source": c.source,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }


def booking_out(b: models.EventBooking):
    return {
        "id": b.id,
        "title": b.title,
        "event_type": b.event_type,
        "start_datetime": b.start_datetime.isoformat() if b.start_datetime else None,
        "end_datetime": b.end_datetime.isoformat() if b.end_datetime else None,
        "guests_count": b.guests_count,
        "status": b.status,
        "total_price": b.total_price,
        "deposit_amount": b.deposit_amount,
        "notes": b.notes,
        "space_id": b.space_id,
        "created_at": b.created_at.isoformat() if b.created_at else None,
    }


@router.get("/")
def list_clients(
    search: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    q = db.query(models.Client).filter(models.Client.venue_id == venue.id)
    if search:
        q = q.filter(
            (models.Client.name.ilike(f"%{search}%")) |
            (models.Client.email.ilike(f"%{search}%")) |
            (models.Client.phone.ilike(f"%{search}%"))
        )
    if source:
        q = q.filter(models.Client.source == source)
    clients = q.order_by(models.Client.created_at.desc()).all()
    result = []
    for c in clients:
        out = client_out(c)
        out["event_count"] = db.query(models.EventBooking).filter(
            models.EventBooking.client_id == c.id
        ).count()
        result.append(out)
    return result


@router.post("/")
def create_client(
    data: ClientCreate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    client = models.Client(venue_id=venue.id, **data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client_out(client)


@router.get("/{client_id}")
def get_client(
    client_id: int,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    client = db.query(models.Client).filter(
        models.Client.id == client_id,
        models.Client.venue_id == venue.id,
    ).first()
    if not client:
        raise HTTPException(404, "Cliente no encontrado")
    out = client_out(client)
    bookings = db.query(models.EventBooking).filter(
        models.EventBooking.client_id == client_id
    ).order_by(models.EventBooking.created_at.desc()).all()
    out["bookings"] = [booking_out(b) for b in bookings]
    return out


@router.put("/{client_id}")
def update_client(
    client_id: int,
    data: ClientUpdate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    client = db.query(models.Client).filter(
        models.Client.id == client_id,
        models.Client.venue_id == venue.id,
    ).first()
    if not client:
        raise HTTPException(404, "Cliente no encontrado")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client_out(client)
