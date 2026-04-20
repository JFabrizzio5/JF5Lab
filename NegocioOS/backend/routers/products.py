from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/products", tags=["products"])


class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = ""
    category_id: Optional[int] = None
    price: float
    cost: float = 0.0
    stock: int = 0
    min_stock: int = 5
    image_url: Optional[str] = None
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    stock: Optional[int] = None
    min_stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class StockAdjust(BaseModel):
    change_qty: int
    reason: str = "adjustment"


def product_out(p: models.Product) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "sku": p.sku,
        "description": p.description or "",
        "category_id": p.category_id,
        "category_name": p.category.name if p.category else None,
        "category_color": p.category.color if p.category else None,
        "price": p.price,
        "cost": p.cost,
        "stock": p.stock,
        "min_stock": p.min_stock,
        "image_url": p.image_url,
        "is_active": p.is_active,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "low_stock": p.stock < p.min_stock,
    }


@router.get("/")
def list_products(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    products = db.query(models.Product).filter_by(is_active=True).all()
    return [product_out(p) for p in products]


@router.get("/all")
def list_all_products(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    products = db.query(models.Product).all()
    return [product_out(p) for p in products]


@router.post("/")
def create_product(
    req: ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    if db.query(models.Product).filter_by(sku=req.sku).first():
        raise HTTPException(status_code=400, detail="SKU ya existe")
    p = models.Product(**req.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return product_out(p)


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    p = db.query(models.Product).filter_by(id=product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product_out(p)


@router.put("/{product_id}")
def update_product(
    product_id: int,
    req: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    p = db.query(models.Product).filter_by(id=product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for field, value in req.model_dump(exclude_none=True).items():
        setattr(p, field, value)
    db.commit()
    db.refresh(p)
    return product_out(p)


@router.post("/{product_id}/adjust-stock")
def adjust_stock(
    product_id: int,
    req: StockAdjust,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    p = db.query(models.Product).filter_by(id=product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    p.stock += req.change_qty
    if p.stock < 0:
        p.stock = 0
    reason_map = {
        "adjustment": models.InventoryReason.adjustment,
        "purchase": models.InventoryReason.purchase,
        "return": models.InventoryReason.return_,
    }
    log = models.InventoryLog(
        product_id=product_id,
        change_qty=req.change_qty,
        reason=reason_map.get(req.reason, models.InventoryReason.adjustment),
    )
    db.add(log)
    db.commit()
    db.refresh(p)
    return product_out(p)


@router.get("/categories/list")
def list_categories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    cats = db.query(models.Category).all()
    return [{"id": c.id, "name": c.name, "color": c.color} for c in cats]
