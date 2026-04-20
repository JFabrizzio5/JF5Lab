from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/api/contacts", tags=["contacts"])


class ContactIn(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    tags: list[str] = []
    notes: str | None = None
    source: str | None = "manual"


def _out(c: models.Contact) -> dict:
    return {
        "id": c.id, "name": c.name, "email": c.email, "phone": c.phone,
        "company": c.company, "tags": c.tags or [], "notes": c.notes,
        "source": c.source, "source_session_id": c.source_session_id,
        "owner_id": c.owner_id,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }


@router.get("/")
def list_contacts(q: str | None = None, session_id: int | None = None, limit: int = 200, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    qry = db.query(models.Contact).filter(models.Contact.workspace_id == user.workspace_id)
    if session_id:
        qry = qry.filter(models.Contact.source_session_id == session_id)
    if q:
        like = f"%{q}%"
        qry = qry.filter(or_(
            models.Contact.name.ilike(like),
            models.Contact.email.ilike(like),
            models.Contact.phone.ilike(like),
            models.Contact.company.ilike(like),
        ))
    rows = qry.order_by(models.Contact.updated_at.desc()).limit(limit).all()
    return [_out(c) for c in rows]


@router.post("/")
def create_contact(payload: ContactIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    c = models.Contact(
        workspace_id=user.workspace_id,
        owner_id=user.id,
        **payload.model_dump(),
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return _out(c)


@router.put("/{contact_id}")
def update_contact(contact_id: int, payload: ContactIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    c = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.workspace_id == user.workspace_id,
    ).first()
    if not c:
        raise HTTPException(404, "Contacto no encontrado")
    for k, v in payload.model_dump().items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return _out(c)


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    c = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.workspace_id == user.workspace_id,
    ).first()
    if not c:
        raise HTTPException(404, "Contacto no encontrado")
    db.delete(c)
    db.commit()
    return {"ok": True}
