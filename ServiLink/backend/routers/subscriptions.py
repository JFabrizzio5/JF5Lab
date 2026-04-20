from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

PLANS = {
    "free":    {"name": "Free",    "price": 0,    "max_services": 1,  "badge": False, "featured": False},
    "basic":   {"name": "Básico",  "price": 199,  "max_services": 5,  "badge": True,  "featured": False},
    "pro":     {"name": "Pro",     "price": 499,  "max_services": 20, "badge": True,  "featured": True},
    "premium": {"name": "Premium", "price": 999,  "max_services": -1, "badge": True,  "featured": True},
}


@router.get("/plans")
def get_plans():
    return [{"plan": k, **v} for k, v in PLANS.items()]


@router.get("/me")
def get_my_subscription(
    current_user: models.User = Depends(auth_utils.require_role("freelancer")),
    db: Session = Depends(get_db)
):
    sub = db.query(models.Subscription).filter(models.Subscription.user_id == current_user.id).first()
    if not sub:
        sub = models.Subscription(user_id=current_user.id, plan="free", price_monthly=0.0)
        db.add(sub)
        db.commit()
        db.refresh(sub)
    return {
        "plan": sub.plan,
        "status": sub.status,
        "price_monthly": sub.price_monthly,
        "expires_at": sub.expires_at.isoformat() if sub.expires_at else None,
        "plan_details": PLANS.get(sub.plan, {}),
    }


class SubscribeRequest(BaseModel):
    plan: str


@router.post("/subscribe")
def subscribe(
    data: SubscribeRequest,
    current_user: models.User = Depends(auth_utils.require_role("freelancer")),
    db: Session = Depends(get_db)
):
    if data.plan not in PLANS:
        raise HTTPException(status_code=400, detail="Plan inválido")

    sub = db.query(models.Subscription).filter(models.Subscription.user_id == current_user.id).first()
    if not sub:
        sub = models.Subscription(user_id=current_user.id)
        db.add(sub)

    plan_info = PLANS[data.plan]
    sub.plan = data.plan
    sub.price_monthly = plan_info["price"]
    sub.status = "active"
    sub.expires_at = datetime.utcnow() + timedelta(days=30)

    prof = db.query(models.ProfessionalProfile).filter(
        models.ProfessionalProfile.user_id == current_user.id
    ).first()
    if prof:
        prof.subscription_plan = data.plan

    db.commit()
    return {
        "ok": True,
        "plan": data.plan,
        "message": f"Suscripción a {plan_info['name']} activada (demo - sin pago real)",
        "expires_at": sub.expires_at.isoformat(),
    }


@router.get("/all")
def all_subscriptions(
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    subs = db.query(models.Subscription).all()
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "plan": s.plan,
            "status": s.status,
            "price_monthly": s.price_monthly,
            "expires_at": s.expires_at.isoformat() if s.expires_at else None,
        }
        for s in subs
    ]
