from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current_user: models.User = Depends(auth_utils.require_role("superadmin"))):
    return current_user


@router.get("/stats")
def admin_stats(
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    total_users = db.query(models.User).count()
    total_vendors = db.query(models.VendorProfile).count()
    active_vendors = db.query(models.VendorProfile).filter(models.VendorProfile.is_active == True).count()
    total_items = db.query(models.RentalItem).filter(models.RentalItem.is_active == True).count()
    total_bookings = db.query(models.Booking).count()
    return {
        "total_users": total_users,
        "total_vendors": total_vendors,
        "active_vendors": active_vendors,
        "total_items": total_items,
        "total_bookings": total_bookings,
    }


@router.get("/vendors")
def list_all_vendors(
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    vendors = db.query(models.VendorProfile).order_by(models.VendorProfile.created_at.desc()).all()
    result = []
    for v in vendors:
        user = db.query(models.User).filter(models.User.id == v.user_id).first()
        items_count = db.query(models.RentalItem).filter(
            models.RentalItem.vendor_id == v.id,
            models.RentalItem.is_active == True,
        ).count()
        bookings_count = db.query(models.Booking).filter(models.Booking.vendor_id == v.id).count()
        result.append({
            "id": v.id,
            "slug": v.slug,
            "business_name": v.business_name,
            "city": v.city,
            "theme_color": v.theme_color,
            "is_active": v.is_active,
            "stripe_onboarding_complete": v.stripe_onboarding_complete,
            "platform_fee_percent": v.platform_fee_percent,
            "items_count": items_count,
            "bookings_count": bookings_count,
            "user_email": user.email if user else None,
            "created_at": v.created_at.isoformat(),
        })
    return result


@router.put("/vendors/{vendor_id}/toggle")
def toggle_vendor(
    vendor_id: int,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.id == vendor_id).first()
    if not vendor:
        raise HTTPException(404, "Vendedor no encontrado")
    vendor.is_active = not vendor.is_active
    db.commit()
    return {"id": vendor.id, "is_active": vendor.is_active}


@router.put("/vendors/{vendor_id}/fee")
def set_platform_fee(
    vendor_id: int,
    fee: float,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.id == vendor_id).first()
    if not vendor:
        raise HTTPException(404, "Vendedor no encontrado")
    if fee < 0 or fee > 50:
        raise HTTPException(400, "Fee debe estar entre 0 y 50%")
    vendor.platform_fee_percent = fee
    db.commit()
    return {"id": vendor.id, "platform_fee_percent": vendor.platform_fee_percent}
