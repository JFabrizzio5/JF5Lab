from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/vendors", tags=["vendors"])


class VendorProfileUpdate(BaseModel):
    business_name: Optional[str] = None
    slug: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    theme_color: Optional[str] = None
    accent_color: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    tiktok_url: Optional[str] = None
    website_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    cancellation_policy: Optional[str] = None
    deposit_percent: Optional[float] = None


def vendor_to_dict(v: models.VendorProfile) -> dict:
    return {
        "id": v.id,
        "user_id": v.user_id,
        "slug": v.slug,
        "business_name": v.business_name,
        "tagline": v.tagline,
        "description": v.description,
        "logo_url": v.logo_url,
        "cover_url": v.cover_url,
        "theme_color": v.theme_color,
        "accent_color": v.accent_color,
        "phone": v.phone,
        "email": v.email,
        "whatsapp": v.whatsapp,
        "facebook_url": v.facebook_url,
        "instagram_url": v.instagram_url,
        "tiktok_url": v.tiktok_url,
        "website_url": v.website_url,
        "address": v.address,
        "city": v.city,
        "lat": v.lat,
        "lng": v.lng,
        "cancellation_policy": v.cancellation_policy,
        "deposit_percent": v.deposit_percent,
        "stripe_account_id": v.stripe_account_id,
        "stripe_onboarding_complete": v.stripe_onboarding_complete,
        "platform_fee_percent": v.platform_fee_percent,
        "is_active": v.is_active,
        "created_at": v.created_at.isoformat(),
    }


@router.get("/me")
def get_my_profile(
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        raise HTTPException(404, "Perfil de vendedor no encontrado")
    return vendor_to_dict(vendor)


@router.put("/me")
def update_my_profile(
    data: VendorProfileUpdate,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        raise HTTPException(404, "Perfil de vendedor no encontrado")

    # Check slug uniqueness if changing
    if data.slug and data.slug != vendor.slug:
        existing = db.query(models.VendorProfile).filter(
            models.VendorProfile.slug == data.slug,
            models.VendorProfile.id != vendor.id,
        ).first()
        if existing:
            raise HTTPException(400, "Ese slug ya está en uso")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(vendor, field, value)

    db.commit()
    db.refresh(vendor)
    return vendor_to_dict(vendor)


@router.get("/me/stats")
def get_my_stats(
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        raise HTTPException(404, "Perfil de vendedor no encontrado")

    now = datetime.utcnow()
    total_items = db.query(models.RentalItem).filter(
        models.RentalItem.vendor_id == vendor.id,
        models.RentalItem.is_active == True,
    ).count()

    total_bookings = db.query(models.Booking).filter(models.Booking.vendor_id == vendor.id).count()

    pending_bookings = db.query(models.Booking).filter(
        models.Booking.vendor_id == vendor.id,
        models.Booking.status.in_(["inquiry", "quote_sent"]),
    ).count()

    # Revenue this month from payments
    revenue_this_month = db.query(func.sum(models.Payment.vendor_amount)).filter(
        models.Payment.vendor_id == vendor.id,
        models.Payment.status == "succeeded",
        extract("month", models.Payment.created_at) == now.month,
        extract("year", models.Payment.created_at) == now.year,
    ).scalar() or 0.0

    return {
        "total_items": total_items,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "revenue_this_month": revenue_this_month,
    }
