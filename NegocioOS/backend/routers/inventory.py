from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/logs")
def get_inventory_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
    limit: int = 100,
):
    logs = (
        db.query(models.InventoryLog)
        .options(joinedload(models.InventoryLog.product))
        .order_by(models.InventoryLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": log.id,
            "product_id": log.product_id,
            "product_name": log.product.name if log.product else None,
            "change_qty": log.change_qty,
            "reason": log.reason,
            "reference_id": log.reference_id,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]


@router.get("/low-stock")
def get_low_stock(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    products = db.query(models.Product).filter(
        models.Product.is_active == True,
        models.Product.stock < models.Product.min_stock
    ).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "stock": p.stock,
            "min_stock": p.min_stock,
            "category_name": p.category.name if p.category else None,
        }
        for p in products
    ]
