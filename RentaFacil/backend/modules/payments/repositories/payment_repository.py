from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from modules.payments.models.models import Payment
from datetime import date

class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int, status: str | None = None) -> list[Payment]:
        query = select(Payment).where(Payment.user_id == user_id).options(selectinload(Payment.contract))
        if status:
            query = query.where(Payment.status == status)
        query = query.order_by(Payment.due_date.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_overdue(self, user_id: int) -> list[Payment]:
        today = date.today()
        result = await self.db.execute(
            select(Payment).where(
                Payment.user_id == user_id,
                Payment.status == "pending",
                Payment.due_date < today
            ).options(selectinload(Payment.contract)).order_by(Payment.due_date)
        )
        return result.scalars().all()

    async def get_by_id(self, payment_id: int, user_id: int) -> Payment | None:
        result = await self.db.execute(
            select(Payment).where(Payment.id == payment_id, Payment.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_contract(self, contract_id: int, user_id: int) -> list[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.contract_id == contract_id, Payment.user_id == user_id).order_by(Payment.due_date.desc())
        )
        return result.scalars().all()

    async def create(self, user_id: int, data: dict) -> Payment:
        payment = Payment(user_id=user_id, **data)
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def update(self, payment: Payment, data: dict) -> Payment:
        for k, v in data.items():
            setattr(payment, k, v)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment
