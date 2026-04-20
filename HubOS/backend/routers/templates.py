from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/api/templates", tags=["templates"])


class TemplateIn(BaseModel):
    name: str
    category: str = "general"  # support | presentation | tech_doc | general
    description: str | None = None
    blocks: list[dict] = []
    variables: list[dict] = []
    is_public: bool = False


class RenderIn(BaseModel):
    values: dict = {}


def _out(t: models.Template) -> dict:
    return {
        "id": t.id, "name": t.name, "category": t.category,
        "description": t.description, "blocks": t.blocks or [],
        "variables": t.variables or [], "is_public": t.is_public,
        "created_by": t.created_by,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
    }


@router.get("/")
def list_templates(category: str | None = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    qry = db.query(models.Template).filter(models.Template.workspace_id == user.workspace_id)
    if category:
        qry = qry.filter(models.Template.category == category)
    return [_out(t) for t in qry.order_by(models.Template.updated_at.desc()).all()]


@router.post("/")
def create_template(payload: TemplateIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    t = models.Template(workspace_id=user.workspace_id, created_by=user.id, **payload.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return _out(t)


@router.put("/{template_id}")
def update_template(template_id: int, payload: TemplateIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    t = db.query(models.Template).filter(
        models.Template.id == template_id, models.Template.workspace_id == user.workspace_id
    ).first()
    if not t:
        raise HTTPException(404, "Template no encontrado")
    for k, v in payload.model_dump().items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return _out(t)


@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    t = db.query(models.Template).filter(
        models.Template.id == template_id, models.Template.workspace_id == user.workspace_id
    ).first()
    if not t:
        raise HTTPException(404, "Template no encontrado")
    db.delete(t)
    db.commit()
    return {"ok": True}


@router.post("/{template_id}/render")
def render_template(template_id: int, payload: RenderIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Render blocks by substituting {{var}} tokens with provided values."""
    t = db.query(models.Template).filter(
        models.Template.id == template_id, models.Template.workspace_id == user.workspace_id
    ).first()
    if not t:
        raise HTTPException(404, "Template no encontrado")
    vals = {}
    for v in (t.variables or []):
        key = v.get("key")
        if not key:
            continue
        vals[key] = payload.values.get(key, v.get("default", ""))

    def subst(text: str) -> str:
        if not isinstance(text, str):
            return text
        for k, val in vals.items():
            text = text.replace("{{" + k + "}}", str(val))
        return text

    rendered = []
    for b in (t.blocks or []):
        nb = dict(b)
        if "content" in nb:
            nb["content"] = subst(nb["content"])
        if "title" in nb:
            nb["title"] = subst(nb["title"])
        rendered.append(nb)
    return {"name": t.name, "category": t.category, "blocks": rendered, "values": vals}
