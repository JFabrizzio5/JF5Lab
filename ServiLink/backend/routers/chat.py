from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from jose import jwt, JWTError
from database import get_db, SessionLocal
import models
import auth as auth_utils

router = APIRouter(prefix="/chat", tags=["chat"])


# ---- WebSocket connection manager ----
class ConnectionManager:
    def __init__(self):
        # room_id -> list of (websocket, user_id)
        self.rooms: dict[int, list[tuple]] = {}

    async def connect(self, ws: WebSocket, room_id: int, user_id: int):
        await ws.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append((ws, user_id))

    def disconnect(self, ws: WebSocket, room_id: int):
        if room_id in self.rooms:
            self.rooms[room_id] = [(w, u) for w, u in self.rooms[room_id] if w != ws]

    async def broadcast(self, room_id: int, message: dict):
        if room_id not in self.rooms:
            return
        dead = []
        for ws, uid in self.rooms[room_id]:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append((ws, uid))
        for item in dead:
            self.rooms[room_id].remove(item)


manager = ConnectionManager()


def get_user_from_token(token: str, db: Session) -> Optional[models.User]:
    try:
        payload = jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return db.query(models.User).filter(models.User.id == int(user_id)).first()
    except JWTError:
        return None


# ---- REST endpoints ----

@router.get("/room/{professional_user_id}")
def get_or_create_room(
    professional_user_id: int,
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ("client", "superadmin"):
        raise HTTPException(status_code=403, detail="Solo clientes pueden iniciar chats")

    pro_user = db.query(models.User).filter(
        models.User.id == professional_user_id,
        models.User.role == "freelancer"
    ).first()
    if not pro_user:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")

    room = db.query(models.ChatRoom).filter(
        models.ChatRoom.client_id == current_user.id,
        models.ChatRoom.professional_id == professional_user_id
    ).first()

    if not room:
        room = models.ChatRoom(client_id=current_user.id, professional_id=professional_user_id)
        db.add(room)
        db.commit()
        db.refresh(room)

    return {"room_id": room.id}


@router.get("/rooms")
def list_my_rooms(
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "client":
        rooms = db.query(models.ChatRoom).options(
            joinedload(models.ChatRoom.professional),
        ).filter(models.ChatRoom.client_id == current_user.id).all()
    elif current_user.role == "freelancer":
        rooms = db.query(models.ChatRoom).options(
            joinedload(models.ChatRoom.client),
        ).filter(models.ChatRoom.professional_id == current_user.id).all()
    else:
        rooms = db.query(models.ChatRoom).options(
            joinedload(models.ChatRoom.client),
            joinedload(models.ChatRoom.professional),
        ).all()

    result = []
    for r in rooms:
        last_msg = db.query(models.ChatMessage).filter(
            models.ChatMessage.room_id == r.id
        ).order_by(models.ChatMessage.created_at.desc()).first()

        other = r.professional if current_user.role == "client" else r.client
        result.append({
            "room_id": r.id,
            "other_user": {
                "id": other.id,
                "name": other.name,
                "avatar_url": other.avatar_url,
                "role": other.role,
            },
            "last_message": last_msg.content if last_msg else None,
            "last_at": last_msg.created_at.isoformat() if last_msg else r.created_at.isoformat(),
        })

    result.sort(key=lambda x: x["last_at"], reverse=True)
    return result


@router.get("/rooms/{room_id}/messages")
def get_messages(
    room_id: int,
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    room = db.query(models.ChatRoom).filter(models.ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    if current_user.role not in ("superadmin",) and current_user.id not in (room.client_id, room.professional_id):
        raise HTTPException(status_code=403, detail="Sin acceso")

    msgs = db.query(models.ChatMessage).options(
        joinedload(models.ChatMessage.sender)
    ).filter(models.ChatMessage.room_id == room_id).order_by(models.ChatMessage.created_at).all()

    return [
        {
            "id": m.id,
            "content": m.content,
            "sender_id": m.sender_id,
            "sender_name": m.sender.name if m.sender else "?",
            "sender_avatar": m.sender.avatar_url if m.sender else None,
            "created_at": m.created_at.isoformat(),
            "is_mine": m.sender_id == current_user.id,
        }
        for m in msgs
    ]


# ---- WebSocket ----

@router.websocket("/ws/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: int,
    token: str = Query(...)
):
    db = SessionLocal()
    try:
        user = get_user_from_token(token, db)
        if not user:
            await websocket.close(code=4001)
            return

        room = db.query(models.ChatRoom).filter(models.ChatRoom.id == room_id).first()
        if not room or user.id not in (room.client_id, room.professional_id):
            await websocket.close(code=4003)
            return

        await manager.connect(websocket, room_id, user.id)

        await websocket.send_json({
            "type": "connected",
            "user_id": user.id,
            "user_name": user.name,
        })

        while True:
            data = await websocket.receive_json()

            if data.get("type") == "message" and data.get("content", "").strip():
                content = data["content"].strip()[:1000]

                msg = models.ChatMessage(
                    room_id=room_id,
                    sender_id=user.id,
                    content=content,
                )
                db.add(msg)
                db.commit()
                db.refresh(msg)

                await manager.broadcast(room_id, {
                    "type": "message",
                    "id": msg.id,
                    "content": msg.content,
                    "sender_id": user.id,
                    "sender_name": user.name,
                    "sender_avatar": user.avatar_url,
                    "created_at": msg.created_at.isoformat(),
                })

            elif data.get("type") == "typing":
                await manager.broadcast(room_id, {
                    "type": "typing",
                    "user_id": user.id,
                    "user_name": user.name,
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast(room_id, {
            "type": "user_left",
            "user_id": user.id if user else None,
        })
    finally:
        db.close()
