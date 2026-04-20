from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/speakers", tags=["speakers"])


class SpeakerCreate(BaseModel):
    convention_id: int
    name: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    twitter: Optional[str] = None
    is_keynote: Optional[bool] = False


def speaker_to_dict(s: models.Speaker):
    return {
        "id": s.id,
        "convention_id": s.convention_id,
        "name": s.name,
        "bio": s.bio,
        "photo_url": s.photo_url,
        "title": s.title,
        "company": s.company,
        "twitter": s.twitter,
        "is_keynote": s.is_keynote,
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
def list_speakers(convention_id: int, db: Session = Depends(get_db)):
    speakers = db.query(models.Speaker).filter(
        models.Speaker.convention_id == convention_id,
        models.Speaker.is_active == True
    ).all()
    return [speaker_to_dict(s) for s in speakers]


@router.post("/")
def create_speaker(
    data: SpeakerCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(data.convention_id, current_user, db)
    speaker = models.Speaker(
        convention_id=data.convention_id,
        name=data.name,
        bio=data.bio,
        photo_url=data.photo_url,
        title=data.title,
        company=data.company,
        twitter=data.twitter,
        is_keynote=data.is_keynote or False,
    )
    db.add(speaker)
    db.commit()
    db.refresh(speaker)
    return speaker_to_dict(speaker)


@router.put("/{speaker_id}")
def update_speaker(
    speaker_id: int,
    data: SpeakerCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    speaker = db.query(models.Speaker).filter(models.Speaker.id == speaker_id).first()
    if not speaker:
        raise HTTPException(404, "Not found")
    check_conv_owner(speaker.convention_id, current_user, db)
    for field in ("name", "bio", "photo_url", "title", "company", "twitter", "is_keynote"):
        val = getattr(data, field)
        if val is not None:
            setattr(speaker, field, val)
    db.commit()
    db.refresh(speaker)
    return speaker_to_dict(speaker)


@router.delete("/{speaker_id}")
def delete_speaker(
    speaker_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    speaker = db.query(models.Speaker).filter(models.Speaker.id == speaker_id).first()
    if not speaker:
        raise HTTPException(404, "Not found")
    check_conv_owner(speaker.convention_id, current_user, db)
    speaker.is_active = False
    db.commit()
    return {"message": "Deleted"}
