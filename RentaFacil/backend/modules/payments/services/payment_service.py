from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from modules.payments.repositories.payment_repository import PaymentRepository

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.repo = PaymentRepository(db)

    async def list_payments(self, user_id: int, status: str | None = None):
        return await self.repo.get_all(user_id, status)

    async def get_overdue(self, user_id: int):
        return await self.repo.get_overdue(user_id)

    async def get_payment(self, payment_id: int, user_id: int):
        payment = await self.repo.get_by_id(payment_id, user_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

    async def create_payment(self, user_id: int, data: dict):
        return await self.repo.create(user_id, data)

    async def mark_paid(self, payment_id: int, user_id: int, data: dict):
        payment = await self.get_payment(payment_id, user_id)
        data["status"] = "paid"
        return await self.repo.update(payment, {k: v for k, v in data.items() if v is not None})

    async def update_payment(self, payment_id: int, user_id: int, data: dict):
        payment = await self.get_payment(payment_id, user_id)
        return await self.repo.update(payment, {k: v for k, v in data.items() if v is not None})
