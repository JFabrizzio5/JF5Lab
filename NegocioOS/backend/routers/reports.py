from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/revenue")
def revenue_last_30_days(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    """Daily revenue for the last 30 days."""
    since = datetime.utcnow() - timedelta(days=30)
    sales = (
        db.query(models.Sale)
        .filter(
            models.Sale.created_at >= since,
            models.Sale.status == models.SaleStatus.completed,
        )
        .all()
    )

    # Group by date
    daily = {}
    for s in sales:
        day = s.created_at.strftime("%Y-%m-%d")
        daily[day] = daily.get(day, 0) + s.total

    # Fill missing days
    result = []
    for i in range(30):
        day = (datetime.utcnow() - timedelta(days=29 - i)).strftime("%Y-%m-%d")
        result.append({"date": day, "total": round(daily.get(day, 0), 2)})

    return result


@router.get("/top-products")
def top_products(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    """Top 5 products by quantity sold."""
    since = datetime.utcnow() - timedelta(days=30)
    rows = (
        db.query(
            models.Product.name,
            func.sum(models.SaleItem.quantity).label("total_qty"),
            func.sum(models.SaleItem.subtotal).label("total_revenue"),
        )
        .join(models.SaleItem, models.SaleItem.product_id == models.Product.id)
        .join(models.Sale, models.Sale.id == models.SaleItem.sale_id)
        .filter(
            models.Sale.created_at >= since,
            models.Sale.status == models.SaleStatus.completed,
        )
        .group_by(models.Product.id, models.Product.name)
        .order_by(func.sum(models.SaleItem.quantity).desc())
        .limit(5)
        .all()
    )
    return [
        {"name": r.name, "total_qty": int(r.total_qty), "total_revenue": round(r.total_revenue, 2)}
        for r in rows
    ]


@router.get("/payment-methods")
def payment_method_breakdown(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    """Sales count and revenue by payment method (last 30 days)."""
    since = datetime.utcnow() - timedelta(days=30)
    rows = (
        db.query(
            models.Sale.payment_method,
            func.count(models.Sale.id).label("count"),
            func.sum(models.Sale.total).label("revenue"),
        )
        .filter(
            models.Sale.created_at >= since,
            models.Sale.status == models.SaleStatus.completed,
        )
        .group_by(models.Sale.payment_method)
        .all()
    )
    return [
        {"method": r.payment_method, "count": int(r.count), "revenue": round(r.revenue or 0, 2)}
        for r in rows
    ]


@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    """Quick KPI summary."""
    since_30 = datetime.utcnow() - timedelta(days=30)
    since_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    total_sales_today = (
        db.query(func.sum(models.Sale.total))
        .filter(
            models.Sale.created_at >= since_today,
            models.Sale.status == models.SaleStatus.completed,
        )
        .scalar() or 0
    )
    total_sales_30 = (
        db.query(func.sum(models.Sale.total))
        .filter(
            models.Sale.created_at >= since_30,
            models.Sale.status == models.SaleStatus.completed,
        )
        .scalar() or 0
    )
    total_products = db.query(func.count(models.Product.id)).filter_by(is_active=True).scalar() or 0
    low_stock_count = db.query(func.count(models.Product.id)).filter(
        models.Product.is_active == True,
        models.Product.stock < models.Product.min_stock,
    ).scalar() or 0
    total_customers = db.query(func.count(models.Customer.id)).scalar() or 0
    sales_count_30 = (
        db.query(func.count(models.Sale.id))
        .filter(
            models.Sale.created_at >= since_30,
            models.Sale.status == models.SaleStatus.completed,
        )
        .scalar() or 0
    )

    return {
        "total_sales_today": round(total_sales_today, 2),
        "total_sales_30_days": round(total_sales_30, 2),
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "total_customers": total_customers,
        "sales_count_30_days": sales_count_30,
    }
