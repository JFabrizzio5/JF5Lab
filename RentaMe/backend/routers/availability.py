from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/availability", tags=["availability"])


class BlockCreate(BaseModel):
    item_id: Optional[int] = None
    start_datetime: datetime
    end_datetime: datetime
    reason: str = "blocked"
    note: Optional[str] = None


def block_to_dict(b: models.AvailabilityBlock) -> dict:
    return {
        "id": b.id,
        "vendor_id": b.vendor_id,
        "item_id": b.item_id,
        "start_datetime": b.start_datetime.isoformat(),
        "end_datetime": b.end_datetime.isoformat(),
        "reason": b.reason,
        "note": b.note,
    }


def get_vendor(current_user: models.User, db: Session) -> models.VendorProfile:
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        raise HTTPException(404, "Perfil de vendedor no encontrado")
    return vendor


@router.get("/")
def list_blocks(
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    blocks = db.query(models.AvailabilityBlock).filter(
        models.AvailabilityBlock.vendor_id == vendor.id,
    ).order_by(models.AvailabilityBlock.start_datetime).all()
    return [block_to_dict(b) for b in blocks]


@router.post("/")
def create_block(
    data: BlockCreate,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)

    if data.item_id:
        item = db.query(models.RentalItem).filter(
            models.RentalItem.id == data.item_id,
            models.RentalItem.vendor_id == vendor.id,
        ).first()
        if not item:
            raise HTTPException(404, "Artículo no encontrado")

    block = models.AvailabilityBlock(
        vendor_id=vendor.id,
        item_id=data.item_id,
        start_datetime=data.start_datetime,
        end_datetime=data.end_datetime,
        reason=data.reason,
        note=data.note,
    )
    db.add(block)
    db.commit()
    db.refresh(block)
    return block_to_dict(block)


@router.delete("/{block_id}")
def delete_block(
    block_id: int,
    current_user: models.User = Depends(auth_utils.require_role("vendor", "superadmin")),
    db: Session = Depends(get_db),
):
    vendor = get_vendor(current_user, db)
    block = db.query(models.AvailabilityBlock).filter(
        models.AvailabilityBlock.id == block_id,
        models.AvailabilityBlock.vendor_id == vendor.id,
    ).first()
    if not block:
        raise HTTPException(404, "Bloqueo no encontrado")
    db.delete(block)
    db.commit()
    return {"ok": True}
