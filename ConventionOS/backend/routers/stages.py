from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/stages", tags=["stages"])


class StageCreate(BaseModel):
    convention_id: int
    name: str
    description: Optional[str] = None
    capacity: Optional[int] = None
    color: Optional[str] = "#6366f1"
    location_in_venue: Optional[str] = None
    stream_url: Optional[str] = None


class SessionCreate(BaseModel):
    convention_id: int
    stage_id: int
    speaker_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    session_type: Optional[str] = "talk"
    start_time: str
    end_time: str
    tags_json: Optional[str] = None


def stage_to_dict(s: models.Stage):
    return {
        "id": s.id,
        "convention_id": s.convention_id,
        "name": s.name,
        "description": s.description,
        "capacity": s.capacity,
        "color": s.color,
        "location_in_venue": s.location_in_venue,
        "stream_url": s.stream_url,
        "is_active": s.is_active,
    }


def session_to_dict(s: models.Session):
    return {
        "id": s.id,
        "convention_id": s.convention_id,
        "stage_id": s.stage_id,
        "speaker_id": s.speaker_id,
        "title": s.title,
        "description": s.description,
        "session_type": s.session_type,
        "start_time": s.start_time.isoformat() if s.start_time else None,
        "end_time": s.end_time.isoformat() if s.end_time else None,
        "tags_json": s.tags_json,
        "is_active": s.is_active,
        "speaker": {
            "id": s.speaker.id,
            "name": s.speaker.name,
            "photo_url": s.speaker.photo_url,
            "title": s.speaker.title,
            "company": s.speaker.company,
        } if s.speaker else None,
    }


def check_conv_owner(conv_id: int, user: models.User, db: Session):
    conv = db.query(models.Convention).filter(models.Convention.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Convention not found")
    if user.role != "superadmin" and conv.organizer_id != user.id:
        raise HTTPException(403, "Forbidden")
    return conv


@router.get("/convention/{convention_id}")
def list_stages(convention_id: int, db: Session = Depends(get_db)):
    stages = db.query(models.Stage).filter(
        models.Stage.convention_id == convention_id,
        models.Stage.is_active == True
    ).all()
    return [stage_to_dict(s) for s in stages]


@router.post("/")
def create_stage(
    data: StageCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(data.convention_id, current_user, db)
    stage = models.Stage(
        convention_id=data.convention_id,
        name=data.name,
        description=data.description,
        capacity=data.capacity,
        color=data.color or "#6366f1",
        location_in_venue=data.location_in_venue,
        stream_url=data.stream_url,
    )
    db.add(stage)
    db.commit()
    db.refresh(stage)
    return stage_to_dict(stage)


@router.put("/{stage_id}")
def update_stage(
    stage_id: int,
    data: StageCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(404, "Not found")
    check_conv_owner(stage.convention_id, current_user, db)
    for field in ("name", "description", "capacity", "color", "location_in_venue", "stream_url"):
        val = getattr(data, field)
        if val is not None:
            setattr(stage, field, val)
    db.commit()
    db.refresh(stage)
    return stage_to_dict(stage)


@router.delete("/{stage_id}")
def delete_stage(
    stage_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(404, "Not found")
    check_conv_owner(stage.convention_id, current_user, db)
    stage.is_active = False
    db.commit()
    return {"message": "Deleted"}


# Sessions
@router.get("/{stage_id}/sessions")
def list_sessions(stage_id: int, db: Session = Depends(get_db)):
    sessions = db.query(models.Session).filter(
        models.Session.stage_id == stage_id,
        models.Session.is_active == True
    ).order_by(models.Session.start_time).all()
    return [session_to_dict(s) for s in sessions]


@router.get("/convention/{convention_id}/sessions")
def list_all_sessions(convention_id: int, db: Session = Depends(get_db)):
    sessions = db.query(models.Session).filter(
        models.Session.convention_id == convention_id,
        models.Session.is_active == True
    ).order_by(models.Session.start_time).all()
    return [session_to_dict(s) for s in sessions]


@router.post("/sessions")
def create_session(
    data: SessionCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(data.convention_id, current_user, db)
    from datetime import datetime
    session = models.Session(
        convention_id=data.convention_id,
        stage_id=data.stage_id,
        speaker_id=data.speaker_id,
        title=data.title,
        description=data.description,
        session_type=data.session_type or "talk",
        start_time=datetime.fromisoformat(data.start_time),
        end_time=datetime.fromisoformat(data.end_time),
        tags_json=data.tags_json,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session_to_dict(session)


@router.put("/sessions/{session_id}")
def update_session(
    session_id: int,
    data: SessionCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(404, "Not found")
    check_conv_owner(session.convention_id, current_user, db)
    from datetime import datetime
    session.stage_id = data.stage_id
    session.speaker_id = data.speaker_id
    session.title = data.title
    session.description = data.description
    session.session_type = data.session_type or "talk"
    session.start_time = datetime.fromisoformat(data.start_time)
    session.end_time = datetime.fromisoformat(data.end_time)
    session.tags_json = data.tags_json
    db.commit()
    db.refresh(session)
    return session_to_dict(session)


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(404, "Not found")
    check_conv_owner(session.convention_id, current_user, db)
    session.is_active = False
    db.commit()
    return {"message": "Deleted"}
