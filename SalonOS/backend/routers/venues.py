from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/venues", tags=["venues"])


class VenueUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    theme_color: Optional[str] = None
    accent_color: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp_number: Optional[str] = None
    whatsapp_message: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    gallery_json: Optional[str] = None
    amenities_json: Optional[str] = None


class BranchCreate(BaseModel):
    name: str
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    phone: Optional[str] = None
    is_active: bool = True


def venue_out(v: models.Venue):
    return {
        "id": v.id,
        "owner_id": v.owner_id,
        "name": v.name,
        "slug": v.slug,
        "tagline": v.tagline,
        "description": v.description,
        "logo_url": v.logo_url,
        "cover_url": v.cover_url,
        "theme_color": v.theme_color,
        "accent_color": v.accent_color,
        "phone": v.phone,
        "email": v.email,
        "whatsapp_number": v.whatsapp_number,
        "whatsapp_message": v.whatsapp_message,
        "address": v.address,
        "city": v.city,
        "lat": v.lat,
        "lng": v.lng,
        "is_active": v.is_active,
        "stripe_account_id": v.stripe_account_id,
        "stripe_onboarding_complete": v.stripe_onboarding_complete,
        "platform_fee_percent": v.platform_fee_percent,
        "gallery_json": v.gallery_json,
        "amenities_json": v.amenities_json,
        "created_at": v.created_at.isoformat() if v.created_at else None,
    }


def branch_out(b: models.VenueBranch):
    return {
        "id": b.id,
        "venue_id": b.venue_id,
        "name": b.name,
        "address": b.address,
        "lat": b.lat,
        "lng": b.lng,
        "phone": b.phone,
        "is_active": b.is_active,
    }


@router.get("/me")
def get_my_venue(
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff", "superadmin")),
    db: Session = Depends(get_db),
):
    venue = db.query(models.Venue).filter(models.Venue.owner_id == current_user.id).first()
    if not venue:
        raise HTTPException(404, "Venue no encontrado")
    return venue_out(venue)


@router.put("/me")
def update_my_venue(
    data: VenueUpdate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(venue, field, value)
    db.commit()
    db.refresh(venue)
    return venue_out(venue)


@router.get("/me/branches")
def list_branches(
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    branches = db.query(models.VenueBranch).filter(models.VenueBranch.venue_id == venue.id).all()
    return [branch_out(b) for b in branches]


@router.post("/me/branches")
def create_branch(
    data: BranchCreate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    branch = models.VenueBranch(venue_id=venue.id, **data.model_dump())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch_out(branch)


@router.put("/me/branches/{branch_id}")
def update_branch(
    branch_id: int,
    data: BranchCreate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    branch = db.query(models.VenueBranch).filter(
        models.VenueBranch.id == branch_id,
        models.VenueBranch.venue_id == venue.id,
    ).first()
    if not branch:
        raise HTTPException(404, "Sucursal no encontrada")
    for field, value in data.model_dump().items():
        setattr(branch, field, value)
    db.commit()
    db.refresh(branch)
    return branch_out(branch)


@router.delete("/me/branches/{branch_id}")
def delete_branch(
    branch_id: int,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    branch = db.query(models.VenueBranch).filter(
        models.VenueBranch.id == branch_id,
        models.VenueBranch.venue_id == venue.id,
    ).first()
    if not branch:
        raise HTTPException(404, "Sucursal no encontrada")
    db.delete(branch)
    db.commit()
    return {"ok": True}


# Admin endpoints
@router.get("/all")
def list_all_venues(
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db),
):
    venues = db.query(models.Venue).all()
    return [venue_out(v) for v in venues]


@router.put("/{venue_id}/toggle")
def toggle_venue(
    venue_id: int,
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db),
):
    venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(404, "Venue no encontrado")
    venue.is_active = not venue.is_active
    db.commit()
    return venue_out(venue)
