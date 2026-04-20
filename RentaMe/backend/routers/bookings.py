from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/bookings", tags=["bookings"])


class StatusUpdate(BaseModel):
    status: str


class NotesUpdate(BaseModel):
    internal_notes: str


VALID_STATUSES = {"inquiry", "quote_sent", "confirmed", "deposit_paid", "active", "completed", "cancelled"}


def booking_to_dict(b: models.Booking) -> dict:
    return {
        "id": b.id,
        "vendor_id": b.vendor_id,
        "item_id": b.item_id,
        "item_name": b.item.name if b.item else None,
        "item_category": b.item.category if b.item else None,
        "customer_name": b.customer_name,
        "customer_email": b.customer_email,
        "customer_phone": b.customer_phone,
        "start_datetime": b.start_datetime.isoformat(),
        "end_datetime": b.end_datetime.isoformat(),
        "rental_unit": b.rental_unit,
        "quantity": b.quantity,
        "unit_price": b.unit_price,
        "subtotal": b.subtotal,
        "deposit_amount": b.deposit_amount,
        "total": b.total,
        "status": b.status,
        "notes": b.notes,
        "internal_notes": b.internal_notes,
        "created_at": b.created_at.isoformat(),
    }


def get_vendor(current_user: models.User, db: Session) -> models.VendorProfile:
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        raise HTTPException(404, "Perfil de vendedor no encontrado")
    return vendor


@router.get("/")
def list_bookings(
    status: Optional[str] = Query(None),
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    q = db.query(models.Booking).filter(models.Booking.vendor_id == vendor.id)
    if status:
        q = q.filter(models.Booking.status == status)
    bookings = q.order_by(models.Booking.created_at.desc()).all()
    return [booking_to_dict(b) for b in bookings]


@router.put("/{booking_id}/status")
def update_status(
    booking_id: int,
    data: StatusUpdate,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    if data.status not in VALID_STATUSES:
        raise HTTPException(400, f"Estado inválido. Válidos: {VALID_STATUSES}")
    vendor = get_vendor(current_user, db)
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id,
        models.Booking.vendor_id == vendor.id,
    ).first()
    if not booking:
        raise HTTPException(404, "Reserva no encontrada")
    booking.status = data.status
    db.commit()
    db.refresh(booking)
    return booking_to_dict(booking)


@router.put("/{booking_id}/notes")
def update_notes(
    booking_id: int,
    data: NotesUpdate,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id,
        models.Booking.vendor_id == vendor.id,
    ).first()
    if not booking:
        raise HTTPException(404, "Reserva no encontrada")
    booking.internal_notes = data.internal_notes
    db.commit()
    db.refresh(booking)
    return booking_to_dict(booking)
