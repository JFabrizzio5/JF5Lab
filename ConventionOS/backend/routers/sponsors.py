from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/sponsors", tags=["sponsors"])


class SponsorCreate(BaseModel):
    convention_id: int
    name: str
    logo_url: Optional[str] = None
    website: Optional[str] = None
    tier: Optional[str] = "bronze"
    amount_sponsored: Optional[float] = 0.0


def sponsor_to_dict(s: models.Sponsor):
    return {
        "id": s.id,
        "convention_id": s.convention_id,
        "name": s.name,
        "logo_url": s.logo_url,
        "website": s.website,
        "tier": s.tier,
        "amount_sponsored": s.amount_sponsored,
        "is_active": s.is_active,
    }


def check_conv_owner(conv_id: int, user: models.User, db: Session):
    conv = db.query(models.Convention).filter(models.Convention.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Convention not found")
    if user.role != "superadmin" and conv.organizer_id != user.id:
        raise HTTPException(403, "Forbidden")
    return conv


@router.get("/convention/{convention_id}")
def list_sponsors(convention_id: int, db: Session = Depends(get_db)):
    sponsors = db.query(models.Sponsor).filter(
        models.Sponsor.convention_id == convention_id,
        models.Sponsor.is_active == True
    ).all()
    return [sponsor_to_dict(s) for s in sponsors]


@router.post("/")
def create_sponsor(
    data: SponsorCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(data.convention_id, current_user, db)
    sponsor = models.Sponsor(
        convention_id=data.convention_id,
        name=data.name,
        logo_url=data.logo_url,
        website=data.website,
        tier=data.tier or "bronze",
        amount_sponsored=data.amount_sponsored or 0.0,
    )
    db.add(sponsor)
    db.commit()
    db.refresh(sponsor)
    return sponsor_to_dict(sponsor)


@router.put("/{sponsor_id}")
def update_sponsor(
    sponsor_id: int,
    data: SponsorCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(404, "Not found")
    check_conv_owner(sponsor.convention_id, current_user, db)
    for field in ("name", "logo_url", "website", "tier", "amount_sponsored"):
        val = getattr(data, field)
        if val is not None:
            setattr(sponsor, field, val)
    db.commit()
    db.refresh(sponsor)
    return sponsor_to_dict(sponsor)


@router.delete("/{sponsor_id}")
def delete_sponsor(
    sponsor_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(404, "Not found")
    check_conv_owner(sponsor.convention_id, current_user, db)
    sponsor.is_active = False
    db.commit()
    return {"message": "Deleted"}
