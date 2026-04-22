import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import jwt

from modules.holaclaude.api.v1.routes import decode_jwt
from modules.holaclaude.services.claude_bridge import send_to_claude

router = APIRouter()
logger = logging.getLogger("ws_agent")


@router.websocket("/holaclaude/v1/ws/agent")
async def ws_agent(websocket: WebSocket, token: str = Query(...)):
    try:
        payload = decode_jwt(token)
        session_id = payload["sub"]
    except jwt.PyJWTError:
        await websocket.close(code=4401)
        return

    await websocket.accept()
    await websocket.send_json({"type": "ready", "session_id": session_id})
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                msg = {"type": "text", "text": raw}
            kind = msg.get("type", "text")
            if kind == "ping":
                await websocket.send_json({"type": "pong"})
                continue
            if kind != "text":
                await websocket.send_json({"type": "error", "error": "tipo no soportado"})
                continue
            text = (msg.get("text") or "").strip()
            if not text:
                continue
            await websocket.send_json({"type": "thinking"})
            result = await send_to_claude(text, session_id)
            await websocket.send_json({"type": "reply", **result})
    except WebSocketDisconnect:
        logger.info(f"ws disconnected {session_id}")
