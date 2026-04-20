from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/sales", tags=["sales"])


class CartItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    items: List[CartItem]
    payment_method: str = "cash"
    notes: Optional[str] = ""


def sale_out(s: models.Sale) -> dict:
    return {
        "id": s.id,
        "user_id": s.user_id,
        "user_name": s.user.name if s.user else None,
        "customer_id": s.customer_id,
        "customer_name": s.customer.name if s.customer else None,
        "subtotal": s.subtotal,
        "tax": s.tax,
        "total": s.total,
        "payment_method": s.payment_method,
        "status": s.status,
        "notes": s.notes or "",
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name if item.product else None,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
            }
            for item in s.items
        ],
    }


@router.post("/")
def create_sale(
    req: SaleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    if not req.items:
        raise HTTPException(status_code=400, detail="La venta debe tener al menos un artículo")

    method_map = {
        "cash": models.PaymentMethod.cash,
        "card": models.PaymentMethod.card,
        "transfer": models.PaymentMethod.transfer,
    }
    pm = method_map.get(req.payment_method, models.PaymentMethod.cash)

    sale = models.Sale(
        user_id=current_user.id,
        customer_id=req.customer_id,
        subtotal=0,
        tax=0,
        total=0,
        payment_method=pm,
        status=models.SaleStatus.completed,
        notes=req.notes,
    )
    db.add(sale)
    db.flush()

    subtotal = 0.0
    for item in req.items:
        product = db.query(models.Product).filter_by(id=item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {product.name}")

        item_subtotal = item.unit_price * item.quantity
        subtotal += item_subtotal

        sale_item = models.SaleItem(
            sale_id=sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item_subtotal,
        )
        db.add(sale_item)

        # Deduct stock
        product.stock -= item.quantity

        # Inventory log
        inv_log = models.InventoryLog(
            product_id=item.product_id,
            change_qty=-item.quantity,
            reason=models.InventoryReason.sale,
            reference_id=sale.id,
        )
        db.add(inv_log)

    tax = round(subtotal * 0.16, 2)
    sale.subtotal = round(subtotal, 2)
    sale.tax = tax
    sale.total = round(subtotal + tax, 2)

    # Update customer total_purchases
    if req.customer_id:
        customer = db.query(models.Customer).filter_by(id=req.customer_id).first()
        if customer:
            customer.total_purchases += sale.total

    db.commit()
    db.refresh(sale)

    # Reload with relationships
    sale = (
        db.query(models.Sale)
        .options(
            joinedload(models.Sale.user),
            joinedload(models.Sale.customer),
            joinedload(models.Sale.items).joinedload(models.SaleItem.product),
        )
        .filter_by(id=sale.id)
        .first()
    )
    return sale_out(sale)


@router.get("/")
def list_sales(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
    limit: int = 100,
    offset: int = 0,
):
    sales = (
        db.query(models.Sale)
        .options(
            joinedload(models.Sale.user),
            joinedload(models.Sale.customer),
            joinedload(models.Sale.items).joinedload(models.SaleItem.product),
        )
        .order_by(models.Sale.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [sale_out(s) for s in sales]


@router.get("/{sale_id}")
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    sale = (
        db.query(models.Sale)
        .options(
            joinedload(models.Sale.user),
            joinedload(models.Sale.customer),
            joinedload(models.Sale.items).joinedload(models.SaleItem.product),
        )
        .filter_by(id=sale_id)
        .first()
    )
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return sale_out(sale)


@router.patch("/{sale_id}/cancel")
def cancel_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    sale = db.query(models.Sale).filter_by(id=sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    if sale.status != models.SaleStatus.completed:
        raise HTTPException(status_code=400, detail="Solo se pueden cancelar ventas completadas")
    sale.status = models.SaleStatus.cancelled
    # Restore stock
    for item in sale.items:
        product = db.query(models.Product).filter_by(id=item.product_id).first()
        if product:
            product.stock += item.quantity
        db.add(models.InventoryLog(
            product_id=item.product_id,
            change_qty=item.quantity,
            reason=models.InventoryReason.return_,
            reference_id=sale.id,
        ))
    db.commit()
    return {"message": "Venta cancelada"}
