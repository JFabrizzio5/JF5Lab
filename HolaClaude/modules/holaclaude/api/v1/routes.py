import os
import json
import uuid
import jwt
import time
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_sql_db
from modules.holaclaude.models.models import Owner, AuditLog
from modules.holaclaude.services.pin import verify_pin
from modules.holaclaude.services.face import (
    is_same_face, validate_descriptor, euclidean_distance, FACE_MATCH_THRESHOLD,
)
from modules.holaclaude.services.cometax_bridge import spawn_service

router = APIRouter()

JWT_SECRET = os.getenv("HOLACLAUDE_JWT_SECRET", "change-me-in-env")
JWT_ALGO = "HS256"
JWT_TTL_MIN = 10
MAX_FAILED = 5
LOCKOUT_SECONDS = 600


class EnrollIn(BaseModel):
    descriptor: list = Field(..., min_length=128, max_length=128)


class VerifyIn(BaseModel):
    descriptor: list = Field(..., min_length=128, max_length=128)
    liveness_blinks: int = 0


class DisableIn(BaseModel):
    pin: str


class ResetIn(BaseModel):
    pin: str
    descriptor: list = Field(..., min_length=128, max_length=128)


class BridgeCometaxIn(BaseModel):
    name: str
    description: str = ""
    framework: str = "1"
    db: str = "1"
    token: str


async def _audit(db: AsyncSession, kind: str, ok: bool, ip: str | None, detail: dict | None = None):
    db.add(AuditLog(kind=kind, ok=ok, ip=ip, detail=detail or {}))
    await db.commit()


async def _get_owner(db: AsyncSession) -> Owner | None:
    res = await db.execute(select(Owner).limit(1))
    return res.scalar_one_or_none()


def _issue_jwt(owner_id: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": str(owner_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_TTL_MIN)).timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])


@router.get("/status")
async def status(db: AsyncSession = Depends(get_sql_db)):
    owner = await _get_owner(db)
    return {
        "enrolled": owner is not None,
        "disabled": owner.disabled if owner else False,
        "locked_out": _is_locked_out(owner),
    }


def _is_locked_out(owner: Owner | None) -> bool:
    if not owner or not owner.last_attempt_at:
        return False
    if owner.failed_attempts < MAX_FAILED:
        return False
    elapsed = (datetime.utcnow() - owner.last_attempt_at).total_seconds()
    return elapsed < LOCKOUT_SECONDS


@router.post("/enroll")
async def enroll(body: EnrollIn, request: Request, db: AsyncSession = Depends(get_sql_db)):
    if not validate_descriptor(body.descriptor):
        raise HTTPException(400, "descriptor invalido")
    existing = await _get_owner(db)
    if existing and existing.owner_locked:
        await _audit(db, "enroll_denied", False, request.client.host if request.client else None)
        raise HTTPException(403, "owner ya enrolado; usa /reset con PIN")
    o = Owner(face_descriptor=body.descriptor, pin_hash=os.getenv("HOLACLAUDE_PIN_HASH", ""), owner_locked=True)
    db.add(o)
    await db.commit()
    await _audit(db, "enroll_ok", True, request.client.host if request.client else None)
    return {"ok": True, "owner_id": str(o.id)}


@router.post("/verify")
async def verify(body: VerifyIn, request: Request, db: AsyncSession = Depends(get_sql_db)):
    owner = await _get_owner(db)
    if not owner:
        raise HTTPException(404, "no enrolado")
    if owner.disabled:
        raise HTTPException(403, "deshabilitado; usa PIN para reactivar")
    if _is_locked_out(owner):
        raise HTTPException(429, "lockout activo")
    if not validate_descriptor(body.descriptor):
        raise HTTPException(400, "descriptor invalido")

    match = is_same_face(owner.face_descriptor, body.descriptor)
    owner.last_attempt_at = datetime.utcnow()
    if match:
        owner.failed_attempts = 0
        await db.commit()
        await _audit(db, "verify_ok", True, request.client.host if request.client else None)
        return {"ok": True, "token": _issue_jwt(owner.id), "ttl_min": JWT_TTL_MIN}
    owner.failed_attempts += 1
    await db.commit()
    await _audit(db, "verify_fail", False, request.client.host if request.client else None,
                 {"attempts": owner.failed_attempts})
    raise HTTPException(401, "no coincide")


@router.post("/disable")
async def disable(body: DisableIn, request: Request, db: AsyncSession = Depends(get_sql_db)):
    owner = await _get_owner(db)
    if not owner:
        raise HTTPException(404, "no enrolado")
    if not verify_pin(body.pin):
        await _audit(db, "disable_fail", False, request.client.host if request.client else None)
        raise HTTPException(401, "pin invalido")
    owner.disabled = True
    owner.disabled_at = datetime.utcnow()
    await db.commit()
    await _audit(db, "disable_ok", True, request.client.host if request.client else None)
    return {"ok": True}


@router.post("/reset")
async def reset(body: ResetIn, request: Request, db: AsyncSession = Depends(get_sql_db)):
    if not verify_pin(body.pin):
        await _audit(db, "reset_fail", False, request.client.host if request.client else None)
        raise HTTPException(401, "pin invalido")
    if not validate_descriptor(body.descriptor):
        raise HTTPException(400, "descriptor invalido")
    owner = await _get_owner(db)
    if owner:
        owner.face_descriptor = body.descriptor
        owner.disabled = False
        owner.disabled_at = None
        owner.failed_attempts = 0
    else:
        owner = Owner(face_descriptor=body.descriptor, pin_hash=os.getenv("HOLACLAUDE_PIN_HASH", ""), owner_locked=True)
        db.add(owner)
    await db.commit()
    await _audit(db, "reset_ok", True, request.client.host if request.client else None)
    return {"ok": True}


@router.get("/gestures")
async def gestures():
    path = os.path.join(os.environ.get("HOLACLAUDE_ARTIFACTS_PATH", "/app/artifacts"), "gestures.json")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


@router.post("/bridge/cometax")
async def bridge_cometax(body: BridgeCometaxIn, request: Request, db: AsyncSession = Depends(get_sql_db)):
    try:
        decode_jwt(body.token)
    except jwt.PyJWTError:
        raise HTTPException(401, "token invalido")
    out = spawn_service(body.name, body.description, body.framework, body.db)
    await _audit(db, "cometax_new", out.get("ok", False), request.client.host if request.client else None,
                 {"name": body.name})
    return out
