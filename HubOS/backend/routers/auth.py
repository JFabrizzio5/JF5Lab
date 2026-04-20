import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
import models
from auth import hash_password, verify_password, create_token, get_current_user, decode_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str
    workspace_name: str | None = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str


def _slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "workspace"


@router.post("/register")
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(400, "Email ya registrado")
    ws_name = payload.workspace_name or f"{payload.name}'s Workspace"
    slug = _slug(ws_name)
    # de-dupe slug
    base = slug
    i = 1
    while db.query(models.Workspace).filter(models.Workspace.slug == slug).first():
        i += 1
        slug = f"{base}-{i}"
    ws = models.Workspace(name=ws_name, slug=slug)
    db.add(ws)
    db.flush()
    user = models.User(
        workspace_id=ws.id,
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
        role="owner",
    )
    db.add(user)
    # default pipeline
    pipe = models.Pipeline(
        workspace_id=ws.id,
        name="Ventas",
        stages=["Nuevo", "Contactado", "Propuesta", "Negociación", "Ganado", "Perdido"],
    )
    db.add(pipe)
    db.commit()
    db.refresh(user)
    return {
        "access_token": create_token(user.id, user.role, ws.id),
        "user": {
            "id": user.id, "email": user.email, "name": user.name,
            "role": user.role, "workspace_id": ws.id, "workspace_name": ws.name,
        },
    }


@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(403, "Usuario desactivado")
    ws = db.query(models.Workspace).filter(models.Workspace.id == user.workspace_id).first()
    return {
        "access_token": create_token(user.id, user.role, user.workspace_id),
        "user": {
            "id": user.id, "email": user.email, "name": user.name,
            "role": user.role, "workspace_id": user.workspace_id,
            "workspace_name": ws.name if ws else None,
        },
    }


@router.get("/me")
def me(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    ws = db.query(models.Workspace).filter(models.Workspace.id == user.workspace_id).first()
    return {
        "id": user.id, "email": user.email, "name": user.name,
        "role": user.role, "workspace_id": user.workspace_id,
        "workspace_name": ws.name if ws else None,
    }


async def _wipe_user_sessions(user_id: int, db: Session) -> int:
    """Logout: remove Evolution WhatsApp pairings + session rows.
    Conversations/messages SURVIVE (session_id goes NULL via FK ON DELETE SET NULL).
    On re-pair, user sees full history.
    """
    import evolution_client
    sessions = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.user_id == user_id
    ).all()
    for s in sessions:
        try:
            await evolution_client.logout_instance(s.instance_name)
            await evolution_client.delete_instance(s.instance_name)
        except Exception:
            pass
        db.delete(s)
    db.commit()
    return len(sessions)


@router.post("/logout_beacon")
async def logout_beacon(t: str, db: Session = Depends(get_db)):
    """Beacon endpoint — no Authorization header (sendBeacon limitation). Token via query param."""
    try:
        payload = decode_token(t)
        user_id = int(payload.get("sub") or 0)
    except Exception:
        return {"ok": False}
    if user_id:
        await _wipe_user_sessions(user_id, db)
    return {"ok": True}


@router.post("/logout")
async def logout(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """On logout: delete ALL of this user's Evolution WhatsApp instances.

    Public-server safety: never leave paired WhatsApp sessions behind.
    """
    cleared = await _wipe_user_sessions(user.id, db)
    return {"ok": True, "cleared": cleared}
