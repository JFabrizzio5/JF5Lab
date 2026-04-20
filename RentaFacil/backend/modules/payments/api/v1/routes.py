from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from datetime import date
from config.database import get_db
from core.dependencies import get_current_user
from modules.payments.services.payment_service import PaymentService

router = APIRouter(prefix="/payments/v1", tags=["payments"])

class PaymentCreate(BaseModel):
    contract_id: int
    amount: float
    due_date: date
    paid_date: Optional[date] = None
    status: Optional[str] = "pending"
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    due_date: Optional[date] = None
    paid_date: Optional[date] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None

@router.get("/")
async def list_payments(status: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PaymentService(db).list_payments(user.id, status)

@router.get("/overdue")
async def overdue_payments(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PaymentService(db).get_overdue(user.id)

@router.post("/")
async def create_payment(body: PaymentCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PaymentService(db).create_payment(user.id, body.model_dump())

@router.get("/{payment_id}")
async def get_payment(payment_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PaymentService(db).get_payment(payment_id, user.id)

@router.put("/{payment_id}")
async def update_payment(payment_id: int, body: PaymentUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PaymentService(db).update_payment(payment_id, user.id, body.model_dump())

@router.post("/{payment_id}/mark-paid")
async def mark_paid(payment_id: int, body: PaymentUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PaymentService(db).mark_paid(payment_id, user.id, body.model_dump())
