from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/categories", tags=["categories"])


class CategoryCreate(BaseModel):
    name: str
    icon: str = "🔧"
    description: Optional[str] = None


@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(models.Category).filter(models.Category.is_active == True).all()
    return [{"id": c.id, "name": c.name, "icon": c.icon, "description": c.description} for c in cats]


@router.post("/")
def create_category(
    data: CategoryCreate,
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    cat = models.Category(name=data.name, icon=data.icon, description=data.description)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return {"id": cat.id, "name": cat.name, "icon": cat.icon, "description": cat.description}


@router.put("/{category_id}")
def update_category(
    category_id: int,
    data: CategoryCreate,
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    cat = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    cat.name = data.name
    cat.icon = data.icon
    cat.description = data.description
    db.commit()
    return {"id": cat.id, "name": cat.name, "icon": cat.icon}


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    current_user: models.User = Depends(auth_utils.require_role("superadmin")),
    db: Session = Depends(get_db)
):
    cat = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    cat.is_active = False
    db.commit()
    return {"ok": True}
