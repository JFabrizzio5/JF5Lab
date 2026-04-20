from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/customers", tags=["customers"])


class CustomerCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = ""


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


def customer_out(c: models.Customer) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "email": c.email or "",
        "phone": c.phone or "",
        "notes": c.notes or "",
        "total_purchases": c.total_purchases,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }


@router.get("/")
def list_customers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    customers = db.query(models.Customer).order_by(models.Customer.name).all()
    return [customer_out(c) for c in customers]


@router.post("/")
def create_customer(
    req: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    c = models.Customer(**req.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return customer_out(c)


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    c = db.query(models.Customer).filter_by(id=customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer_out(c)


@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    req: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    c = db.query(models.Customer).filter_by(id=customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for field, value in req.model_dump(exclude_none=True).items():
        setattr(c, field, value)
    db.commit()
    db.refresh(c)
    return customer_out(c)
