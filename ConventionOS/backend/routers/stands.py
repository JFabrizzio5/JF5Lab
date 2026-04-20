from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/stands", tags=["stands"])


class StandCreate(BaseModel):
    convention_id: int
    number: str
    name: Optional[str] = None
    category: Optional[str] = "general"
    size: Optional[str] = "standard"
    price: Optional[float] = 0.0
    status: Optional[str] = "available"
    x_pos: Optional[float] = None
    y_pos: Optional[float] = None
    width: Optional[float] = 5.0
    height: Optional[float] = 5.0
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None


def stand_to_dict(s: models.Stand):
    return {
        "id": s.id,
        "convention_id": s.convention_id,
        "number": s.number,
        "name": s.name,
        "category": s.category,
        "size": s.size,
        "price": s.price,
        "status": s.status,
        "x_pos": s.x_pos,
        "y_pos": s.y_pos,
        "width": s.width,
        "height": s.height,
        "contact_name": s.contact_name,
        "contact_email": s.contact_email,
        "contact_phone": s.contact_phone,
        "description": s.description,
    }


def check_conv_owner(conv_id: int, user: models.User, db: Session):
    conv = db.query(models.Convention).filter(models.Convention.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Convention not found")
    if user.role != "superadmin" and conv.organizer_id != user.id:
        raise HTTPException(403, "Forbidden")
    return conv


@router.get("/convention/{convention_id}")
def list_stands(convention_id: int, db: Session = Depends(get_db)):
    stands = db.query(models.Stand).filter(
        models.Stand.convention_id == convention_id
    ).all()
    return [stand_to_dict(s) for s in stands]


@router.post("/")
def create_stand(
    data: StandCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(data.convention_id, current_user, db)
    stand = models.Stand(
        convention_id=data.convention_id,
        number=data.number,
        name=data.name,
        category=data.category or "general",
        size=data.size or "standard",
        price=data.price or 0.0,
        status=data.status or "available",
        x_pos=data.x_pos,
        y_pos=data.y_pos,
        width=data.width or 5.0,
        height=data.height or 5.0,
        contact_name=data.contact_name,
        contact_email=data.contact_email,
        contact_phone=data.contact_phone,
        description=data.description,
    )
    db.add(stand)
    db.commit()
    db.refresh(stand)
    return stand_to_dict(stand)


@router.put("/{stand_id}")
def update_stand(
    stand_id: int,
    data: StandCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    stand = db.query(models.Stand).filter(models.Stand.id == stand_id).first()
    if not stand:
        raise HTTPException(404, "Not found")
    check_conv_owner(stand.convention_id, current_user, db)
    for field in ("number", "name", "category", "size", "price", "status",
                  "x_pos", "y_pos", "width", "height", "contact_name",
                  "contact_email", "contact_phone", "description"):
        val = getattr(data, field)
        if val is not None:
            setattr(stand, field, val)
    db.commit()
    db.refresh(stand)
    return stand_to_dict(stand)


@router.delete("/{stand_id}")
def delete_stand(
    stand_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    stand = db.query(models.Stand).filter(models.Stand.id == stand_id).first()
    if not stand:
        raise HTTPException(404, "Not found")
    check_conv_owner(stand.convention_id, current_user, db)
    db.delete(stand)
    db.commit()
    return {"message": "Deleted"}
