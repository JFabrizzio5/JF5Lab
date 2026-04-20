from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/conventions", tags=["conventions"])


class ConventionCreate(BaseModel):
    name: str
    slug: str
    edition: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    banner_url: Optional[str] = None
    theme_color: Optional[str] = "#7c3aed"
    accent_color: Optional[str] = "#f59e0b"
    bg_color: Optional[str] = "#0a0a0f"
    font_style: Optional[str] = "modern"
    venue_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = "draft"
    max_attendees: Optional[int] = None
    website: Optional[str] = None
    social_json: Optional[str] = None
    rules_text: Optional[str] = None
    platform_fee_percent: Optional[float] = 5.0


def conv_to_dict(c: models.Convention):
    return {
        "id": c.id,
        "organizer_id": c.organizer_id,
        "name": c.name,
        "slug": c.slug,
        "edition": c.edition,
        "tagline": c.tagline,
        "description": c.description,
        "logo_url": c.logo_url,
        "cover_url": c.cover_url,
        "banner_url": c.banner_url,
        "theme_color": c.theme_color,
        "accent_color": c.accent_color,
        "bg_color": c.bg_color,
        "font_style": c.font_style,
        "venue_name": c.venue_name,
        "address": c.address,
        "city": c.city,
        "lat": c.lat,
        "lng": c.lng,
        "start_date": c.start_date.isoformat() if c.start_date else None,
        "end_date": c.end_date.isoformat() if c.end_date else None,
        "status": c.status,
        "max_attendees": c.max_attendees,
        "website": c.website,
        "social_json": c.social_json,
        "rules_text": c.rules_text,
        "stripe_account_id": c.stripe_account_id,
        "stripe_onboarding_complete": c.stripe_onboarding_complete,
        "platform_fee_percent": c.platform_fee_percent,
        "is_active": c.is_active,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }


@router.get("/")
def list_conventions(
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    if current_user.role == "superadmin":
        convs = db.query(models.Convention).all()
    else:
        convs = db.query(models.Convention).filter(
            models.Convention.organizer_id == current_user.id
        ).all()
    return [conv_to_dict(c) for c in convs]


@router.post("/")
def create_convention(
    data: ConventionCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    existing = db.query(models.Convention).filter(models.Convention.slug == data.slug).first()
    if existing:
        raise HTTPException(400, "Slug already taken")
    from datetime import datetime
    conv = models.Convention(
        organizer_id=current_user.id,
        name=data.name,
        slug=data.slug,
        edition=data.edition,
        tagline=data.tagline,
        description=data.description,
        logo_url=data.logo_url,
        cover_url=data.cover_url,
        banner_url=data.banner_url,
        theme_color=data.theme_color or "#7c3aed",
        accent_color=data.accent_color or "#f59e0b",
        bg_color=data.bg_color or "#0a0a0f",
        font_style=data.font_style or "modern",
        venue_name=data.venue_name,
        address=data.address,
        city=data.city,
        lat=data.lat,
        lng=data.lng,
        start_date=datetime.fromisoformat(data.start_date) if data.start_date else None,
        end_date=datetime.fromisoformat(data.end_date) if data.end_date else None,
        status=data.status or "draft",
        max_attendees=data.max_attendees,
        website=data.website,
        social_json=data.social_json,
        rules_text=data.rules_text,
        platform_fee_percent=data.platform_fee_percent or 5.0,
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv_to_dict(conv)


@router.get("/my")
def my_convention(
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    conv = db.query(models.Convention).filter(
        models.Convention.organizer_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(404, "No convention found")
    return conv_to_dict(conv)


@router.get("/{convention_id}")
def get_convention(
    convention_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    conv = db.query(models.Convention).filter(models.Convention.id == convention_id).first()
    if not conv:
        raise HTTPException(404, "Not found")
    if current_user.role != "superadmin" and conv.organizer_id != current_user.id:
        raise HTTPException(403, "Forbidden")
    return conv_to_dict(conv)


@router.put("/{convention_id}")
def update_convention(
    convention_id: int,
    data: ConventionCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    conv = db.query(models.Convention).filter(models.Convention.id == convention_id).first()
    if not conv:
        raise HTTPException(404, "Not found")
    if current_user.role != "superadmin" and conv.organizer_id != current_user.id:
        raise HTTPException(403, "Forbidden")
    from datetime import datetime
    # Check slug uniqueness
    if data.slug != conv.slug:
        existing = db.query(models.Convention).filter(models.Convention.slug == data.slug).first()
        if existing:
            raise HTTPException(400, "Slug already taken")
    for field in ("name", "slug", "edition", "tagline", "description", "logo_url", "cover_url",
                  "banner_url", "theme_color", "accent_color", "bg_color", "font_style",
                  "venue_name", "address", "city", "lat", "lng", "status", "max_attendees",
                  "website", "social_json", "rules_text", "platform_fee_percent"):
        val = getattr(data, field)
        if val is not None:
            setattr(conv, field, val)
    if data.start_date:
        conv.start_date = datetime.fromisoformat(data.start_date)
    if data.end_date:
        conv.end_date = datetime.fromisoformat(data.end_date)
    db.commit()
    db.refresh(conv)
    return conv_to_dict(conv)


@router.patch("/{convention_id}/status")
def update_status(
    convention_id: int,
    body: dict,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    conv = db.query(models.Convention).filter(models.Convention.id == convention_id).first()
    if not conv:
        raise HTTPException(404, "Not found")
    if current_user.role != "superadmin" and conv.organizer_id != current_user.id:
        raise HTTPException(403, "Forbidden")
    conv.status = body.get("status", conv.status)
    db.commit()
    return conv_to_dict(conv)


@router.delete("/{convention_id}")
def delete_convention(
    convention_id: int,
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    conv = db.query(models.Convention).filter(models.Convention.id == convention_id).first()
    if not conv:
        raise HTTPException(404, "Not found")
    conv.is_active = False
    db.commit()
    return {"message": "Deleted"}
