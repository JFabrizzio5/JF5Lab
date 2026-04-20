from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


class TournamentCreate(BaseModel):
    convention_id: int
    name: str
    game: Optional[str] = None
    format: Optional[str] = "single_elim"
    max_participants: Optional[int] = 32
    prize_pool: Optional[float] = 0.0
    prize_description: Optional[str] = None
    entry_fee: Optional[float] = 0.0
    start_time: Optional[str] = None
    status: Optional[str] = "open"
    stage_id: Optional[int] = None
    rules_url: Optional[str] = None


class RegistrationCreate(BaseModel):
    tournament_id: int
    player_name: str
    player_email: str
    player_tag: Optional[str] = None


def tournament_to_dict(t: models.Tournament):
    return {
        "id": t.id,
        "convention_id": t.convention_id,
        "name": t.name,
        "game": t.game,
        "format": t.format,
        "max_participants": t.max_participants,
        "participants_count": t.participants_count,
        "prize_pool": t.prize_pool,
        "prize_description": t.prize_description,
        "entry_fee": t.entry_fee,
        "start_time": t.start_time.isoformat() if t.start_time else None,
        "status": t.status,
        "stage_id": t.stage_id,
        "rules_url": t.rules_url,
        "is_active": t.is_active,
    }


def reg_to_dict(r: models.TournamentRegistration):
    return {
        "id": r.id,
        "tournament_id": r.tournament_id,
        "player_name": r.player_name,
        "player_email": r.player_email,
        "player_tag": r.player_tag,
        "status": r.status,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


def check_conv_owner(conv_id: int, user: models.User, db: Session):
    conv = db.query(models.Convention).filter(models.Convention.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Convention not found")
    if user.role != "superadmin" and conv.organizer_id != user.id:
        raise HTTPException(403, "Forbidden")
    return conv


@router.get("/convention/{convention_id}")
def list_tournaments(convention_id: int, db: Session = Depends(get_db)):
    ts = db.query(models.Tournament).filter(
        models.Tournament.convention_id == convention_id,
        models.Tournament.is_active == True
    ).all()
    return [tournament_to_dict(t) for t in ts]


@router.post("/")
def create_tournament(
    data: TournamentCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(data.convention_id, current_user, db)
    from datetime import datetime
    t = models.Tournament(
        convention_id=data.convention_id,
        name=data.name,
        game=data.game,
        format=data.format or "single_elim",
        max_participants=data.max_participants or 32,
        prize_pool=data.prize_pool or 0.0,
        prize_description=data.prize_description,
        entry_fee=data.entry_fee or 0.0,
        start_time=datetime.fromisoformat(data.start_time) if data.start_time else None,
        status=data.status or "open",
        stage_id=data.stage_id,
        rules_url=data.rules_url,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return tournament_to_dict(t)


@router.put("/{tournament_id}")
def update_tournament(
    tournament_id: int,
    data: TournamentCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    t = db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    if not t:
        raise HTTPException(404, "Not found")
    check_conv_owner(t.convention_id, current_user, db)
    from datetime import datetime
    for field in ("name", "game", "format", "max_participants", "prize_pool",
                  "prize_description", "entry_fee", "status", "stage_id", "rules_url"):
        val = getattr(data, field)
        if val is not None:
            setattr(t, field, val)
    if data.start_time:
        t.start_time = datetime.fromisoformat(data.start_time)
    db.commit()
    db.refresh(t)
    return tournament_to_dict(t)


@router.delete("/{tournament_id}")
def delete_tournament(
    tournament_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    t = db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    if not t:
        raise HTTPException(404, "Not found")
    check_conv_owner(t.convention_id, current_user, db)
    t.is_active = False
    db.commit()
    return {"message": "Deleted"}


@router.get("/{tournament_id}/registrations")
def list_registrations(tournament_id: int, db: Session = Depends(get_db)):
    regs = db.query(models.TournamentRegistration).filter(
        models.TournamentRegistration.tournament_id == tournament_id
    ).order_by(models.TournamentRegistration.created_at.desc()).all()
    return [reg_to_dict(r) for r in regs]


@router.post("/register")
def register_player(data: RegistrationCreate, db: Session = Depends(get_db)):
    t = db.query(models.Tournament).filter(
        models.Tournament.id == data.tournament_id,
        models.Tournament.is_active == True
    ).first()
    if not t:
        raise HTTPException(404, "Tournament not found")
    if t.status != "open":
        raise HTTPException(400, "Tournament is not open for registration")
    if t.participants_count >= t.max_participants:
        raise HTTPException(400, "Tournament is full")
    # Check duplicate
    existing = db.query(models.TournamentRegistration).filter(
        models.TournamentRegistration.tournament_id == data.tournament_id,
        models.TournamentRegistration.player_email == data.player_email
    ).first()
    if existing:
        raise HTTPException(400, "Already registered with this email")
    reg = models.TournamentRegistration(
        tournament_id=data.tournament_id,
        player_name=data.player_name,
        player_email=data.player_email,
        player_tag=data.player_tag,
    )
    db.add(reg)
    t.participants_count += 1
    db.commit()
    db.refresh(reg)
    return reg_to_dict(reg)


@router.patch("/registrations/{reg_id}/status")
def update_reg_status(
    reg_id: int,
    body: dict,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    reg = db.query(models.TournamentRegistration).filter(
        models.TournamentRegistration.id == reg_id
    ).first()
    if not reg:
        raise HTTPException(404, "Not found")
    reg.status = body.get("status", reg.status)
    db.commit()
    return reg_to_dict(reg)
