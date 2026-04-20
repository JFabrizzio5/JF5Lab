import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/api/content", tags=["content"])


class ContentIn(BaseModel):
    kind: str = "page"
    title: str
    slug: str | None = None
    body: str | None = None
    blocks: list[dict] = []
    status: str = "draft"
    cover_url: str | None = None


def _slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "page"


def _out(c: models.Content) -> dict:
    return {
        "id": c.id, "kind": c.kind, "title": c.title, "slug": c.slug,
        "body": c.body, "blocks": c.blocks or [], "status": c.status,
        "cover_url": c.cover_url, "author_id": c.author_id,
        "published_at": c.published_at.isoformat() if c.published_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    }


@router.get("/")
def list_content(kind: str | None = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    qry = db.query(models.Content).filter(models.Content.workspace_id == user.workspace_id)
    if kind:
        qry = qry.filter(models.Content.kind == kind)
    return [_out(c) for c in qry.order_by(models.Content.updated_at.desc()).all()]


@router.post("/")
def create_content(payload: ContentIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    data = payload.model_dump()
    if not data.get("slug"):
        data["slug"] = _slugify(data["title"])
    if data["status"] == "published":
        data["published_at"] = datetime.utcnow()
    c = models.Content(workspace_id=user.workspace_id, author_id=user.id, **data)
    db.add(c)
    db.commit()
    db.refresh(c)
    return _out(c)


@router.put("/{content_id}")
def update_content(content_id: int, payload: ContentIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    c = db.query(models.Content).filter(
        models.Content.id == content_id, models.Content.workspace_id == user.workspace_id
    ).first()
    if not c:
        raise HTTPException(404, "No encontrado")
    data = payload.model_dump()
    if data.get("status") == "published" and c.status != "published":
        data["published_at"] = datetime.utcnow()
    for k, v in data.items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return _out(c)


@router.delete("/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    c = db.query(models.Content).filter(
        models.Content.id == content_id, models.Content.workspace_id == user.workspace_id
    ).first()
    if not c:
        raise HTTPException(404, "No encontrado")
    db.delete(c)
    db.commit()
    return {"ok": True}


# Public read-only endpoint by slug (for CMS rendering)
@router.get("/public/{workspace_slug}/{slug}")
def public_fetch(workspace_slug: str, slug: str, db: Session = Depends(get_db)):
    ws = db.query(models.Workspace).filter(models.Workspace.slug == workspace_slug).first()
    if not ws:
        raise HTTPException(404, "Workspace no existe")
    c = db.query(models.Content).filter(
        models.Content.workspace_id == ws.id,
        models.Content.slug == slug,
        models.Content.status == "published",
    ).first()
    if not c:
        raise HTTPException(404, "Contenido no encontrado")
    return _out(c)
