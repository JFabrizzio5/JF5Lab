from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from modules.payments.models.models import Payment
from modules.properties.models.models import Property
from modules.tenants.models.models import Contract
from datetime import date

class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_stats(self, user_id: int) -> dict:
        total_properties = await self.db.scalar(
            select(func.count()).where(Property.user_id == user_id).select_from(Property)
        )
        occupied = await self.db.scalar(
            select(func.count()).where(Property.user_id == user_id, Property.status == "occupied").select_from(Property)
        )
        vacant = await self.db.scalar(
            select(func.count()).where(Property.user_id == user_id, Property.status == "vacant").select_from(Property)
        )
        today = date.today()
        overdue = await self.db.scalar(
            select(func.count()).where(
                Payment.user_id == user_id,
                Payment.status == "pending",
                Payment.due_date < today
            ).select_from(Payment)
        )
        monthly_income = await self.db.scalar(
            select(func.sum(Payment.amount)).where(
                Payment.user_id == user_id,
                Payment.status == "paid",
                extract("year", Payment.paid_date) == today.year,
                extract("month", Payment.paid_date) == today.month
            ).select_from(Payment)
        )
        active_contracts = await self.db.scalar(
            select(func.count()).where(Contract.user_id == user_id, Contract.status == "active").select_from(Contract)
        )
        return {
            "total_properties": total_properties or 0,
            "occupied": occupied or 0,
            "vacant": vacant or 0,
            "overdue_payments": overdue or 0,
            "monthly_income": float(monthly_income or 0),
            "active_contracts": active_contracts or 0,
            "occupancy_rate": round((occupied / total_properties * 100) if total_properties else 0, 1)
        }

    async def get_monthly_report(self, user_id: int, year: int, month: int) -> dict:
        paid_result = await self.db.execute(
            select(func.sum(Payment.amount), func.count()).where(
                Payment.user_id == user_id,
                Payment.status == "paid",
                extract("year", Payment.paid_date) == year,
                extract("month", Payment.paid_date) == month
            ).select_from(Payment)
        )
        paid_row = paid_result.one()
        pending_result = await self.db.execute(
            select(func.sum(Payment.amount), func.count()).where(
                Payment.user_id == user_id,
                Payment.status == "pending",
                extract("year", Payment.due_date) == year,
                extract("month", Payment.due_date) == month
            ).select_from(Payment)
        )
        pending_row = pending_result.one()
        return {
            "year": year,
            "month": month,
            "paid_amount": float(paid_row[0] or 0),
            "paid_count": paid_row[1] or 0,
            "pending_amount": float(pending_row[0] or 0),
            "pending_count": pending_row[1] or 0,
        }
