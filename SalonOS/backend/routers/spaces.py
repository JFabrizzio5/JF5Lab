from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/spaces", tags=["spaces"])


class SpaceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: int = 50
    price_per_hour: float = 0.0
    price_event: float = 0.0
    images_json: Optional[str] = None
    amenities_json: Optional[str] = None
    floor_plan_url: Optional[str] = None
    branch_id: Optional[int] = None
    is_active: bool = True


def space_out(s: models.EventSpace):
    return {
        "id": s.id,
        "venue_id": s.venue_id,
        "branch_id": s.branch_id,
        "name": s.name,
        "description": s.description,
        "capacity": s.capacity,
        "price_per_hour": s.price_per_hour,
        "price_event": s.price_event,
        "images_json": s.images_json,
        "amenities_json": s.amenities_json,
        "floor_plan_url": s.floor_plan_url,
        "is_active": s.is_active,
    }


@router.get("/")
def list_spaces(
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    spaces = db.query(models.EventSpace).filter(models.EventSpace.venue_id == venue.id).all()
    return [space_out(s) for s in spaces]


@router.post("/")
def create_space(
    data: SpaceCreate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    space = models.EventSpace(venue_id=venue.id, **data.model_dump())
    db.add(space)
    db.commit()
    db.refresh(space)
    return space_out(space)


@router.put("/{space_id}")
def update_space(
    space_id: int,
    data: SpaceCreate,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    space = db.query(models.EventSpace).filter(
        models.EventSpace.id == space_id,
        models.EventSpace.venue_id == venue.id,
    ).first()
    if not space:
        raise HTTPException(404, "Espacio no encontrado")
    for field, value in data.model_dump().items():
        setattr(space, field, value)
    db.commit()
    db.refresh(space)
    return space_out(space)


@router.delete("/{space_id}")
def delete_space(
    space_id: int,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    space = db.query(models.EventSpace).filter(
        models.EventSpace.id == space_id,
        models.EventSpace.venue_id == venue.id,
    ).first()
    if not space:
        raise HTTPException(404, "Espacio no encontrado")
    db.delete(space)
    db.commit()
    return {"ok": True}
