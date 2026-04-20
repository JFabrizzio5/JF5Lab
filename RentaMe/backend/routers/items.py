import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str = "general"
    images_json: Optional[str] = None
    price_per_hour: Optional[float] = None
    price_per_day: Optional[float] = None
    price_per_weekend: Optional[float] = None
    price_per_week: Optional[float] = None
    quantity: int = 1
    min_rental_hours: int = 1
    max_rental_days: Optional[int] = None
    advance_booking_days: int = 0
    specifications_json: Optional[str] = None
    requirements: Optional[str] = None
    included_json: Optional[str] = None
    not_included_json: Optional[str] = None
    deposit_amount: float = 0.0
    is_featured: bool = False


class ItemUpdate(ItemCreate):
    name: Optional[str] = None
    is_active: Optional[bool] = None


def item_to_dict(item: models.RentalItem) -> dict:
    return {
        "id": item.id,
        "vendor_id": item.vendor_id,
        "name": item.name,
        "description": item.description,
        "category": item.category,
        "images_json": item.images_json,
        "images": json.loads(item.images_json) if item.images_json else [],
        "price_per_hour": item.price_per_hour,
        "price_per_day": item.price_per_day,
        "price_per_weekend": item.price_per_weekend,
        "price_per_week": item.price_per_week,
        "quantity": item.quantity,
        "min_rental_hours": item.min_rental_hours,
        "max_rental_days": item.max_rental_days,
        "advance_booking_days": item.advance_booking_days,
        "specifications_json": item.specifications_json,
        "specifications": json.loads(item.specifications_json) if item.specifications_json else {},
        "requirements": item.requirements,
        "included_json": item.included_json,
        "included": json.loads(item.included_json) if item.included_json else [],
        "not_included_json": item.not_included_json,
        "not_included": json.loads(item.not_included_json) if item.not_included_json else [],
        "deposit_amount": item.deposit_amount,
        "is_active": item.is_active,
        "is_featured": item.is_featured,
        "created_at": item.created_at.isoformat(),
    }


def get_vendor(current_user: models.User, db: Session) -> models.VendorProfile:
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        raise HTTPException(404, "Perfil de vendedor no encontrado")
    return vendor


@router.get("/")
def list_items(
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    items = db.query(models.RentalItem).filter(
        models.RentalItem.vendor_id == vendor.id,
    ).order_by(models.RentalItem.created_at.desc()).all()
    return [item_to_dict(i) for i in items]


@router.post("/")
def create_item(
    data: ItemCreate,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    item = models.RentalItem(vendor_id=vendor.id, **data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item_to_dict(item)


@router.put("/{item_id}")
def update_item(
    item_id: int,
    data: ItemUpdate,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    item = db.query(models.RentalItem).filter(
        models.RentalItem.id == item_id,
        models.RentalItem.vendor_id == vendor.id,
    ).first()
    if not item:
        raise HTTPException(404, "Artículo no encontrado")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item_to_dict(item)


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    item = db.query(models.RentalItem).filter(
        models.RentalItem.id == item_id,
        models.RentalItem.vendor_id == vendor.id,
    ).first()
    if not item:
        raise HTTPException(404, "Artículo no encontrado")
    item.is_active = False
    db.commit()
    return {"ok": True}
