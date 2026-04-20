"""Public endpoints — no auth required. Used by professional landing pages."""
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from database import get_db
import models

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/pro/{user_id}")
def get_public_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.id == user_id,
        models.User.role == "freelancer",
        models.User.is_active == True,
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")

    prof = db.query(models.ProfessionalProfile).options(
        joinedload(models.ProfessionalProfile.categories).joinedload(models.ProfessionalCategory.category)
    ).filter(models.ProfessionalProfile.user_id == user_id).first()

    reviews = db.query(models.Review).options(
        joinedload(models.Review.client)
    ).filter(
        models.Review.professional_id == user_id
    ).order_by(models.Review.created_at.desc()).limit(10).all()

    categories = [pc.category.name for pc in prof.categories if pc.category] if prof else []

    return {
        "user_id": user.id,
        "name": user.name,
        "avatar_url": user.avatar_url,
        "phone": user.phone,
        "bio": prof.bio if prof else None,
        "hourly_rate": prof.hourly_rate if prof else 0,
        "experience_years": prof.experience_years if prof else 0,
        "lat": prof.lat if prof else None,
        "lng": prof.lng if prof else None,
        "address": prof.address if prof else None,
        "is_available": prof.is_available if prof else False,
        "subscription_plan": prof.subscription_plan if prof else "free",
        "rating_avg": round(prof.rating_avg, 1) if prof else 0,
        "total_reviews": prof.total_reviews if prof else 0,
        "total_jobs": prof.total_jobs if prof else 0,
        "cover_url": prof.cover_url if prof else None,
        "tagline": prof.tagline if prof else None,
        "theme_color": prof.theme_color if prof else "#6366f1",
        "services_json": prof.services_json if prof else None,
        "categories": categories,
        "reviews": [
            {
                "id": r.id,
                "rating": r.rating,
                "comment": r.comment,
                "client_name": r.client.name if r.client else "Anónimo",
                "client_avatar": r.client.avatar_url if r.client else None,
                "created_at": r.created_at.isoformat(),
            }
            for r in reviews
        ],
    }
