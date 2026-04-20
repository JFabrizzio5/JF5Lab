from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from typing import Dict, List
from database import get_db, SessionLocal
import models
import auth as auth_utils
from jose import jwt, JWTError

router = APIRouter(prefix="/chat", tags=["chat"])

SECRET_KEY = "salonos_secret_key_2024"
ALGORITHM = "HS256"

# In-memory connection manager
class ConnectionManager:
    def __init__(self):
        self.active: Dict[int, List[WebSocket]] = {}

    async def connect(self, room_id: int, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(room_id, []).append(ws)

    def disconnect(self, room_id: int, ws: WebSocket):
        if room_id in self.active:
            self.active[room_id].remove(ws)

    async def broadcast(self, room_id: int, message: dict):
        for ws in self.active.get(room_id, []):
            try:
                await ws.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


def room_out(r: models.ChatRoom):
    out = {
        "id": r.id,
        "venue_id": r.venue_id,
        "client_id": r.client_id,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }
    if r.client:
        out["client_name"] = r.client.name
        out["client_email"] = r.client.email
    last = r.messages[-1] if r.messages else None
    if last:
        out["last_message"] = last.content
        out["last_message_at"] = last.created_at.isoformat() if last.created_at else None
    else:
        out["last_message"] = None
        out["last_message_at"] = None
    return out


def message_out(m: models.ChatMessage):
    return {
        "id": m.id,
        "room_id": m.room_id,
        "sender_user_id": m.sender_user_id,
        "sender_name": m.sender_name,
        "sender_type": m.sender_type,
        "content": m.content,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }


@router.get("/rooms")
def list_rooms(
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    rooms = db.query(models.ChatRoom).filter(
        models.ChatRoom.venue_id == venue.id
    ).order_by(models.ChatRoom.created_at.desc()).all()
    return [room_out(r) for r in rooms]


@router.get("/rooms/{room_id}/messages")
def get_messages(
    room_id: int,
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    room = db.query(models.ChatRoom).filter(
        models.ChatRoom.id == room_id,
        models.ChatRoom.venue_id == venue.id,
    ).first()
    if not room:
        raise HTTPException(404, "Sala no encontrada")
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.room_id == room_id
    ).order_by(models.ChatMessage.created_at.asc()).all()
    return [message_out(m) for m in messages]


@router.websocket("/ws/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: int,
    token: str = Query(...),
):
    # Validate token
    db = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            await websocket.close(code=1008)
            return
        room = db.query(models.ChatRoom).filter(models.ChatRoom.id == room_id).first()
        if not room:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return
    finally:
        db.close()

    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content", "").strip()
            if not content:
                continue
            db2 = SessionLocal()
            try:
                msg = models.ChatMessage(
                    room_id=room_id,
                    sender_user_id=user.id,
                    sender_name=user.name,
                    sender_type="staff",
                    content=content,
                )
                db2.add(msg)
                db2.commit()
                db2.refresh(msg)
                await manager.broadcast(room_id, message_out(msg))
            finally:
                db2.close()
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
