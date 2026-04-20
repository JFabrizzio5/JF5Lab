import json
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(prefix="/public", tags=["public"])


def item_to_public_dict(item: models.RentalItem) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "category": item.category,
        "images": json.loads(item.images_json) if item.images_json else [],
        "price_per_hour": item.price_per_hour,
        "price_per_day": item.price_per_day,
        "price_per_weekend": item.price_per_weekend,
        "price_per_week": item.price_per_week,
        "quantity": item.quantity,
        "min_rental_hours": item.min_rental_hours,
        "max_rental_days": item.max_rental_days,
        "advance_booking_days": item.advance_booking_days,
        "specifications": json.loads(item.specifications_json) if item.specifications_json else {},
        "requirements": item.requirements,
        "included": json.loads(item.included_json) if item.included_json else [],
        "not_included": json.loads(item.not_included_json) if item.not_included_json else [],
        "deposit_amount": item.deposit_amount,
        "is_featured": item.is_featured,
    }


@router.get("/vendor/{slug}")
def get_vendor_public(slug: str, db: Session = Depends(get_db)):
    vendor = db.query(models.VendorProfile).filter(
        models.VendorProfile.slug == slug,
        models.VendorProfile.is_active == True,
    ).first()
    if not vendor:
        raise HTTPException(404, "Vendedor no encontrado")

    items = db.query(models.RentalItem).filter(
        models.RentalItem.vendor_id == vendor.id,
        models.RentalItem.is_active == True,
    ).order_by(models.RentalItem.is_featured.desc(), models.RentalItem.created_at.desc()).all()

    return {
        "id": vendor.id,
        "slug": vendor.slug,
        "business_name": vendor.business_name,
        "tagline": vendor.tagline,
        "description": vendor.description,
        "logo_url": vendor.logo_url,
        "cover_url": vendor.cover_url,
        "theme_color": vendor.theme_color,
        "accent_color": vendor.accent_color,
        "phone": vendor.phone,
        "email": vendor.email,
        "whatsapp": vendor.whatsapp,
        "facebook_url": vendor.facebook_url,
        "instagram_url": vendor.instagram_url,
        "tiktok_url": vendor.tiktok_url,
        "website_url": vendor.website_url,
        "address": vendor.address,
        "city": vendor.city,
        "cancellation_policy": vendor.cancellation_policy,
        "deposit_percent": vendor.deposit_percent,
        "items": [item_to_public_dict(i) for i in items],
    }


class InquiryRequest(BaseModel):
    item_id: int
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    rental_unit: str = "day"
    quantity: int = 1
    notes: Optional[str] = None


@router.post("/vendor/{slug}/inquiry")
def create_inquiry(slug: str, data: InquiryRequest, db: Session = Depends(get_db)):
    vendor = db.query(models.VendorProfile).filter(
        models.VendorProfile.slug == slug,
        models.VendorProfile.is_active == True,
    ).first()
    if not vendor:
        raise HTTPException(404, "Vendedor no encontrado")

    item = db.query(models.RentalItem).filter(
        models.RentalItem.id == data.item_id,
        models.RentalItem.vendor_id == vendor.id,
        models.RentalItem.is_active == True,
    ).first()
    if not item:
        raise HTTPException(404, "Artículo no encontrado")

    # Calculate pricing
    unit_map = {
        "hour": item.price_per_hour,
        "day": item.price_per_day,
        "weekend": item.price_per_weekend,
        "week": item.price_per_week,
    }
    unit_price = unit_map.get(data.rental_unit)
    if unit_price is None:
        raise HTTPException(400, f"Unidad de renta no disponible para este artículo: {data.rental_unit}")

    # Calculate duration multiplier
    duration = data.end_datetime - data.start_datetime
    if data.rental_unit == "hour":
        multiplier = max(1, int(duration.total_seconds() / 3600))
    elif data.rental_unit == "day":
        multiplier = max(1, duration.days)
    elif data.rental_unit == "weekend":
        multiplier = 1
    elif data.rental_unit == "week":
        multiplier = max(1, duration.days // 7)
    else:
        multiplier = 1

    subtotal = unit_price * multiplier * data.quantity
    deposit_pct = vendor.deposit_percent / 100
    deposit_amount = round(subtotal * deposit_pct, 2)
    total = subtotal

    booking = models.Booking(
        vendor_id=vendor.id,
        item_id=item.id,
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        start_datetime=data.start_datetime,
        end_datetime=data.end_datetime,
        rental_unit=data.rental_unit,
        quantity=data.quantity,
        unit_price=unit_price,
        subtotal=subtotal,
        deposit_amount=deposit_amount,
        total=total,
        status="inquiry",
        notes=data.notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    wa_link = None
    if vendor.whatsapp:
        wa_link = f"https://wa.me/{vendor.whatsapp}"

    return {
        "booking_id": booking.id,
        "total": booking.total,
        "deposit_amount": booking.deposit_amount,
        "status": booking.status,
        "vendor_whatsapp_link": wa_link,
        "vendor_whatsapp": vendor.whatsapp,
        "item_name": item.name,
        "start_datetime": booking.start_datetime.isoformat(),
        "end_datetime": booking.end_datetime.isoformat(),
    }


@router.get("/vendor/{slug}/availability")
def get_availability(
    slug: str,
    item_id: Optional[int] = Query(None),
    month: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    vendor = db.query(models.VendorProfile).filter(
        models.VendorProfile.slug == slug,
        models.VendorProfile.is_active == True,
    ).first()
    if not vendor:
        raise HTTPException(404, "Vendedor no encontrado")

    q = db.query(models.AvailabilityBlock).filter(
        models.AvailabilityBlock.vendor_id == vendor.id,
    )

    if item_id:
        q = q.filter(
            (models.AvailabilityBlock.item_id == item_id) |
            (models.AvailabilityBlock.item_id == None)
        )

    if month:
        try:
            month_dt = datetime.strptime(month, "%Y-%m")
            import calendar
            last_day = calendar.monthrange(month_dt.year, month_dt.month)[1]
            month_end = month_dt.replace(day=last_day, hour=23, minute=59, second=59)
            q = q.filter(
                models.AvailabilityBlock.start_datetime <= month_end,
                models.AvailabilityBlock.end_datetime >= month_dt,
            )
        except ValueError:
            pass

    blocks = q.all()

    # Also get bookings for the month
    booking_q = db.query(models.Booking).filter(
        models.Booking.vendor_id == vendor.id,
        models.Booking.status.in_(["confirmed", "deposit_paid", "active"]),
    )
    if item_id:
        booking_q = booking_q.filter(models.Booking.item_id == item_id)
    if month:
        try:
            month_dt = datetime.strptime(month, "%Y-%m")
            import calendar
            last_day = calendar.monthrange(month_dt.year, month_dt.month)[1]
            month_end = month_dt.replace(day=last_day, hour=23, minute=59, second=59)
            booking_q = booking_q.filter(
                models.Booking.start_datetime <= month_end,
                models.Booking.end_datetime >= month_dt,
            )
        except ValueError:
            pass

    bookings = booking_q.all()

    return {
        "blocks": [
            {
                "id": b.id,
                "item_id": b.item_id,
                "start_datetime": b.start_datetime.isoformat(),
                "end_datetime": b.end_datetime.isoformat(),
                "reason": b.reason,
                "note": b.note,
                "type": "block",
            }
            for b in blocks
        ],
        "bookings": [
            {
                "id": bk.id,
                "item_id": bk.item_id,
                "start_datetime": bk.start_datetime.isoformat(),
                "end_datetime": bk.end_datetime.isoformat(),
                "status": bk.status,
                "type": "booking",
            }
            for bk in bookings
        ],
    }
