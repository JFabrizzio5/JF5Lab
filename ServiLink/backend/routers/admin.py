from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def get_stats(
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    total_users = db.query(models.User).count()
    total_clients = db.query(models.User).filter(models.User.role == "client").count()
    total_freelancers = db.query(models.User).filter(models.User.role == "freelancer").count()
    total_bookings = db.query(models.Booking).count()
    completed_bookings = db.query(models.Booking).filter(models.Booking.status == "completed").count()
    total_reviews = db.query(models.Review).count()
    total_categories = db.query(models.Category).filter(models.Category.is_active == True).count()

    revenue = db.query(models.Subscription).filter(
        models.Subscription.plan != "free",
        models.Subscription.status == "active"
    ).all()
    monthly_revenue = sum(s.price_monthly for s in revenue)

    return {
        "total_users": total_users,
        "total_clients": total_clients,
        "total_freelancers": total_freelancers,
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "total_reviews": total_reviews,
        "total_categories": total_categories,
        "monthly_revenue": monthly_revenue,
    }


@router.get("/users")
def list_users(
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "role": u.role,
            "is_active": u.is_active,
            "avatar_url": u.avatar_url,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]


@router.patch("/users/{user_id}/toggle")
def toggle_user(
    user_id: int,
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user.role == "superadmin":
        raise HTTPException(status_code=400, detail="No se puede desactivar un superadmin")
    user.is_active = not user.is_active
    db.commit()
    return {"id": user.id, "is_active": user.is_active}


@router.get("/bookings")
def list_all_bookings(
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import joinedload
    bookings = db.query(models.Booking).options(
        joinedload(models.Booking.client),
        joinedload(models.Booking.professional),
        joinedload(models.Booking.category),
    ).order_by(models.Booking.created_at.desc()).all()

    return [
        {
            "id": b.id,
            "status": b.status,
            "price": b.price,
            "client": b.client.name if b.client else None,
            "professional": b.professional.name if b.professional else None,
            "category": b.category.name if b.category else None,
            "created_at": b.created_at.isoformat() if b.created_at else None,
        }
        for b in bookings
    ]
