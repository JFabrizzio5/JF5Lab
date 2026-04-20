from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional, List
import math
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/professionals", tags=["professionals"])


def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def prof_to_dict(prof: models.ProfessionalProfile, distance_km: float = None):
    user = prof.user
    cats = [pc.category.name for pc in prof.categories if pc.category]
    return {
        "id": prof.id,
        "user_id": prof.user_id,
        "name": user.name,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "phone": user.phone,
        "bio": prof.bio,
        "hourly_rate": prof.hourly_rate,
        "experience_years": prof.experience_years,
        "lat": prof.lat,
        "lng": prof.lng,
        "address": prof.address,
        "is_available": prof.is_available,
        "subscription_plan": prof.subscription_plan,
        "rating_avg": round(prof.rating_avg, 1),
        "total_reviews": prof.total_reviews,
        "total_jobs": prof.total_jobs,
        "categories": cats,
        "distance_km": round(distance_km, 2) if distance_km is not None else None,
        "cover_url": prof.cover_url,
        "tagline": prof.tagline,
        "theme_color": prof.theme_color or "#6366f1",
        "services_json": prof.services_json,
    }


@router.get("/")
def list_professionals(
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    radius_km: float = Query(50.0),
    category_id: Optional[int] = Query(None),
    min_rating: Optional[float] = Query(None),
    available_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(models.ProfessionalProfile).options(
        joinedload(models.ProfessionalProfile.user),
        joinedload(models.ProfessionalProfile.categories).joinedload(models.ProfessionalCategory.category)
    )

    if available_only:
        query = query.filter(models.ProfessionalProfile.is_available == True)

    if category_id:
        query = query.join(models.ProfessionalCategory).filter(
            models.ProfessionalCategory.category_id == category_id
        )

    if min_rating:
        query = query.filter(models.ProfessionalProfile.rating_avg >= min_rating)

    profs = query.all()

    result = []
    for p in profs:
        if not p.user or not p.user.is_active:
            continue
        distance = None
        if lat is not None and lng is not None and p.lat and p.lng:
            distance = haversine(lat, lng, p.lat, p.lng)
            if distance > radius_km:
                continue
        result.append(prof_to_dict(p, distance))

    if lat is not None and lng is not None:
        result.sort(key=lambda x: x["distance_km"] or 9999)

    return result


@router.get("/{professional_id}")
def get_professional(professional_id: int, db: Session = Depends(get_db)):
    prof = db.query(models.ProfessionalProfile).options(
        joinedload(models.ProfessionalProfile.user),
        joinedload(models.ProfessionalProfile.categories).joinedload(models.ProfessionalCategory.category)
    ).filter(models.ProfessionalProfile.id == professional_id).first()

    if not prof:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")

    return prof_to_dict(prof)


class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    hourly_rate: Optional[float] = None
    experience_years: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[str] = None
    is_available: Optional[bool] = None
    category_ids: Optional[List[int]] = None
    cover_url: Optional[str] = None
    tagline: Optional[str] = None
    theme_color: Optional[str] = None
    services_json: Optional[str] = None


@router.put("/me/profile")
def update_my_profile(
    data: ProfileUpdate,
    current_user: models.User = Depends(auth_utils.require_role("freelancer")),
    db: Session = Depends(get_db)
):
    prof = db.query(models.ProfessionalProfile).filter(
        models.ProfessionalProfile.user_id == current_user.id
    ).first()
    if not prof:
        prof = models.ProfessionalProfile(user_id=current_user.id)
        db.add(prof)

    if data.bio is not None:
        prof.bio = data.bio
    if data.hourly_rate is not None:
        prof.hourly_rate = data.hourly_rate
    if data.experience_years is not None:
        prof.experience_years = data.experience_years
    if data.lat is not None:
        prof.lat = data.lat
    if data.lng is not None:
        prof.lng = data.lng
    if data.address is not None:
        prof.address = data.address
    if data.is_available is not None:
        prof.is_available = data.is_available
    if data.cover_url is not None:
        prof.cover_url = data.cover_url
    if data.tagline is not None:
        prof.tagline = data.tagline
    if data.theme_color is not None:
        prof.theme_color = data.theme_color
    if data.services_json is not None:
        prof.services_json = data.services_json

    if data.category_ids is not None:
        db.query(models.ProfessionalCategory).filter(
            models.ProfessionalCategory.professional_id == prof.id
        ).delete()
        for cat_id in data.category_ids:
            pc = models.ProfessionalCategory(professional_id=prof.id, category_id=cat_id)
            db.add(pc)

    db.commit()
    db.refresh(prof)
    return prof_to_dict(prof)


@router.get("/me/profile")
def get_my_profile(
    current_user: models.User = Depends(auth_utils.require_role("freelancer")),
    db: Session = Depends(get_db)
):
    prof = db.query(models.ProfessionalProfile).options(
        joinedload(models.ProfessionalProfile.user),
        joinedload(models.ProfessionalProfile.categories).joinedload(models.ProfessionalCategory.category)
    ).filter(models.ProfessionalProfile.user_id == current_user.id).first()

    if not prof:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return prof_to_dict(prof)
