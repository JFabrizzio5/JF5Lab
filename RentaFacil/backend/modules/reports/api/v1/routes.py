from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from config.database import get_db
from core.dependencies import get_current_user
from modules.reports.services.report_service import ReportService

router = APIRouter(prefix="/reports/v1", tags=["reports"])

@router.get("/dashboard")
async def dashboard_stats(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await ReportService(db).get_dashboard_stats(user.id)

@router.get("/monthly")
async def monthly_report(
    year: int = Query(default=date.today().year),
    month: int = Query(default=date.today().month),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await ReportService(db).get_monthly_report(user.id, year, month)
