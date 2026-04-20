from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models

router = APIRouter(prefix="/public", tags=["public"])


class InquiryCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    event_type: str = "boda"
    start_datetime: datetime
    guests_count: int = 0
    notes: Optional[str] = None
    source: str = "web"


class PublicChatCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


def venue_public_out(v: models.Venue, db: Session):
    branches = db.query(models.VenueBranch).filter(
        models.VenueBranch.venue_id == v.id,
        models.VenueBranch.is_active == True,
    ).all()

    spaces = db.query(models.EventSpace).filter(
        models.EventSpace.venue_id == v.id,
        models.EventSpace.is_active == True,
    ).all()

    return {
        "id": v.id,
        "name": v.name,
        "slug": v.slug,
        "tagline": v.tagline,
        "description": v.description,
        "logo_url": v.logo_url,
        "cover_url": v.cover_url,
        "theme_color": v.theme_color,
        "accent_color": v.accent_color,
        "phone": v.phone,
        "email": v.email,
        "whatsapp_number": v.whatsapp_number,
        "whatsapp_message": v.whatsapp_message,
        "address": v.address,
        "city": v.city,
        "lat": v.lat,
        "lng": v.lng,
        "gallery_json": v.gallery_json,
        "amenities_json": v.amenities_json,
        "branches": [
            {
                "id": b.id,
                "name": b.name,
                "address": b.address,
                "lat": b.lat,
                "lng": b.lng,
                "phone": b.phone,
            }
            for b in branches
        ],
        "spaces": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "capacity": s.capacity,
                "price_per_hour": s.price_per_hour,
                "price_event": s.price_event,
                "images_json": s.images_json,
                "amenities_json": s.amenities_json,
                "floor_plan_url": s.floor_plan_url,
            }
            for s in spaces
        ],
    }


@router.get("/venue/{slug}")
def get_public_venue(slug: str, db: Session = Depends(get_db)):
    venue = db.query(models.Venue).filter(
        models.Venue.slug == slug,
        models.Venue.is_active == True,
    ).first()
    if not venue:
        raise HTTPException(404, "Venue no encontrado")
    return venue_public_out(venue, db)


@router.post("/venue/{slug}/inquiry")
def submit_inquiry(slug: str, data: InquiryCreate, db: Session = Depends(get_db)):
    venue = db.query(models.Venue).filter(
        models.Venue.slug == slug,
        models.Venue.is_active == True,
    ).first()
    if not venue:
        raise HTTPException(404, "Venue no encontrado")

    # Find or create client
    client = None
    if data.email:
        client = db.query(models.Client).filter(
            models.Client.venue_id == venue.id,
            models.Client.email == data.email,
        ).first()

    if not client:
        client = models.Client(
            venue_id=venue.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            source=data.source,
        )
        db.add(client)
        db.flush()

    end_dt = datetime(
        data.start_datetime.year,
        data.start_datetime.month,
        data.start_datetime.day,
        23, 59, 59
    )

    booking = models.EventBooking(
        venue_id=venue.id,
        client_id=client.id,
        title=f"Consulta: {data.event_type} - {data.name}",
        event_type=data.event_type,
        start_datetime=data.start_datetime,
        end_datetime=end_dt,
        guests_count=data.guests_count,
        status="inquiry",
        notes=data.notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "ok": True,
        "client_id": client.id,
        "booking_id": booking.id,
        "message": "Tu solicitud ha sido enviada. Te contactaremos pronto.",
    }


@router.post("/venue/{slug}/chat")
def get_or_create_chat(slug: str, data: PublicChatCreate, db: Session = Depends(get_db)):
    venue = db.query(models.Venue).filter(
        models.Venue.slug == slug,
        models.Venue.is_active == True,
    ).first()
    if not venue:
        raise HTTPException(404, "Venue no encontrado")

    # Find or create client by email
    client = db.query(models.Client).filter(
        models.Client.venue_id == venue.id,
        models.Client.email == data.email,
    ).first()

    if not client:
        client = models.Client(
            venue_id=venue.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            source="web",
        )
        db.add(client)
        db.flush()

    # Find or create chat room
    room = db.query(models.ChatRoom).filter(
        models.ChatRoom.venue_id == venue.id,
        models.ChatRoom.client_id == client.id,
    ).first()

    if not room:
        room = models.ChatRoom(venue_id=venue.id, client_id=client.id)
        db.add(room)
        db.commit()
        db.refresh(room)
    else:
        db.commit()

    return {
        "room_id": room.id,
        "client_id": client.id,
        "client_name": client.name,
    }
