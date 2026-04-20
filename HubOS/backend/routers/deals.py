from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/api/deals", tags=["deals"])


class PipelineIn(BaseModel):
    name: str
    stages: list[str]


class DealIn(BaseModel):
    pipeline_id: int | None = None
    contact_id: int | None = None
    title: str
    value: float = 0
    currency: str = "MXN"
    stage: str = "Nuevo"
    status: str = "open"
    expected_close: str | None = None


# Pipelines ---------------------------------------------------------------
@router.get("/pipelines")
def list_pipelines(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    rows = db.query(models.Pipeline).filter(models.Pipeline.workspace_id == user.workspace_id).all()
    return [{"id": p.id, "name": p.name, "stages": p.stages or []} for p in rows]


@router.post("/pipelines")
def create_pipeline(payload: PipelineIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    p = models.Pipeline(workspace_id=user.workspace_id, **payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "name": p.name, "stages": p.stages or []}


# Deals -------------------------------------------------------------------
def _deal_out(d: models.Deal) -> dict:
    return {
        "id": d.id, "title": d.title, "value": d.value, "currency": d.currency,
        "stage": d.stage, "status": d.status, "pipeline_id": d.pipeline_id,
        "contact_id": d.contact_id,
        "contact": {"id": d.contact.id, "name": d.contact.name} if d.contact else None,
        "expected_close": d.expected_close.isoformat() if d.expected_close else None,
        "created_at": d.created_at.isoformat() if d.created_at else None,
    }


@router.get("/")
def list_deals(pipeline_id: int | None = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    qry = db.query(models.Deal).filter(models.Deal.workspace_id == user.workspace_id)
    if pipeline_id:
        qry = qry.filter(models.Deal.pipeline_id == pipeline_id)
    rows = qry.order_by(models.Deal.updated_at.desc()).all()
    return [_deal_out(d) for d in rows]


@router.post("/")
def create_deal(payload: DealIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    data = payload.model_dump()
    if data.get("expected_close"):
        try:
            data["expected_close"] = datetime.fromisoformat(data["expected_close"])
        except Exception:
            data["expected_close"] = None
    d = models.Deal(workspace_id=user.workspace_id, owner_id=user.id, **data)
    db.add(d)
    db.commit()
    db.refresh(d)
    return _deal_out(d)


@router.put("/{deal_id}")
def update_deal(deal_id: int, payload: DealIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    d = db.query(models.Deal).filter(
        models.Deal.id == deal_id, models.Deal.workspace_id == user.workspace_id
    ).first()
    if not d:
        raise HTTPException(404, "Deal no encontrado")
    data = payload.model_dump()
    if data.get("expected_close"):
        try:
            data["expected_close"] = datetime.fromisoformat(data["expected_close"])
        except Exception:
            data["expected_close"] = None
    for k, v in data.items():
        setattr(d, k, v)
    db.commit()
    db.refresh(d)
    return _deal_out(d)


@router.patch("/{deal_id}/stage")
def move_stage(deal_id: int, body: dict, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    d = db.query(models.Deal).filter(
        models.Deal.id == deal_id, models.Deal.workspace_id == user.workspace_id
    ).first()
    if not d:
        raise HTTPException(404, "Deal no encontrado")
    d.stage = body.get("stage", d.stage)
    if body.get("status"):
        d.status = body["status"]
    db.commit()
    db.refresh(d)
    return _deal_out(d)


@router.delete("/{deal_id}")
def delete_deal(deal_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    d = db.query(models.Deal).filter(
        models.Deal.id == deal_id, models.Deal.workspace_id == user.workspace_id
    ).first()
    if not d:
        raise HTTPException(404, "Deal no encontrado")
    db.delete(d)
    db.commit()
    return {"ok": True}
