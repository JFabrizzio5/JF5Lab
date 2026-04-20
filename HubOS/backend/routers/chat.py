"""Chat router — Evolution API multi-session integration.

Each agent creates their own instance (per-user WhatsApp). Webhook receives
messages and routes them to the right instance's conversations.
"""
import asyncio
import secrets
from datetime import datetime
from typing import Set, Dict
import base64
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, SessionLocal
from auth import get_current_user, decode_token
import models
import evolution_client

router = APIRouter(prefix="/api/chat", tags=["chat"])


# WebSocket manager per workspace -----------------------------------------
class WsManager:
    def __init__(self):
        self.rooms: Dict[int, Set[WebSocket]] = {}

    async def connect(self, ws_id: int, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(ws_id, set()).add(ws)

    def disconnect(self, ws_id: int, ws: WebSocket):
        if ws_id in self.rooms:
            self.rooms[ws_id].discard(ws)

    async def broadcast(self, ws_id: int, payload: dict):
        dead = []
        for ws in self.rooms.get(ws_id, set()):
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for d in dead:
            self.disconnect(ws_id, d)


manager = WsManager()


# Schemas -----------------------------------------------------------------
class SessionCreate(BaseModel):
    display_name: str | None = None


class SendIn(BaseModel):
    conversation_id: int
    text: str


class LinkContactIn(BaseModel):
    phone: str
    name: str | None = None


class StartConvIn(BaseModel):
    session_id: int
    contact_id: int | None = None
    phone: str | None = None       # raw phone if no contact selected (e.g. "5215512345678")
    contact_name: str | None = None
    text: str


# Sessions ----------------------------------------------------------------
def _session_out(s: models.EvolutionSession) -> dict:
    return {
        "id": s.id, "instance_name": s.instance_name,
        "display_name": s.display_name, "phone_number": s.phone_number,
        "status": s.status, "qr_code": s.qr_code,
        "created_at": s.created_at.isoformat() if s.created_at else None,
    }


async def _sync_session_status(s: models.EvolutionSession, db: Session) -> models.EvolutionSession | None:
    """Ping Evolution for real status. Updates DB. Returns None if instance is gone
    (caller should treat as deleted)."""
    try:
        status = await evolution_client.fetch_status(s.instance_name)
    except Exception as e:
        msg = str(e).lower()
        if "404" in msg or "not found" in msg or "does not exist" in msg:
            # Instance wiped on Evolution side (DEL_INSTANCE, restart tmpfs, etc).
            conv_ids = [c.id for c in db.query(models.Conversation).filter(
                models.Conversation.session_id == s.id
            ).all()]
            if conv_ids:
                db.query(models.Message).filter(models.Message.conversation_id.in_(conv_ids)).delete(synchronize_session=False)
                db.query(models.Conversation).filter(models.Conversation.id.in_(conv_ids)).delete(synchronize_session=False)
            db.delete(s)
            db.commit()
            return None
        return s  # transient error — keep DB status as-is
    state = status.get("instance", {}).get("state") or status.get("state")
    mapping = {"open": "connected", "connecting": "connecting", "close": "disconnected", "closed": "disconnected"}
    new_status = mapping.get(state, s.status)
    if new_status != s.status:
        s.status = new_status
        db.commit()
    return s


@router.get("/sessions")
async def list_sessions(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # Each user sees ONLY their own instances (session separation).
    # On every fetch we re-sync each row with Evolution's actual state, so the
    # frontend sees real status even if the CONNECTION_UPDATE webhook was missed.
    rows = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.workspace_id == user.workspace_id,
        models.EvolutionSession.user_id == user.id,
    ).all()
    synced = []
    for s in rows:
        live = await _sync_session_status(s, db)
        if live:
            synced.append(live)
    return [_session_out(s) for s in synced]


@router.post("/sessions")
async def create_session(payload: SessionCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    instance_name = f"hubos_{user.workspace_id}_{user.id}_{secrets.token_hex(3)}"
    webhook_token = secrets.token_urlsafe(16)
    s = models.EvolutionSession(
        workspace_id=user.workspace_id,
        user_id=user.id,
        instance_name=instance_name,
        display_name=payload.display_name or user.name,
        status="connecting",
    )
    # Stash webhook_token inside display_name prefix? No — store separately.
    # Simpler: derive token from instance_name (HMAC would be better).
    # For MVP we store the token in qr_code field until QR arrives; swap when QR comes.
    db.add(s)
    db.commit()
    db.refresh(s)
    try:
        await evolution_client.create_instance(instance_name, webhook_token=instance_name)
        connect = await evolution_client.connect_instance(instance_name)
        qr = connect.get("base64") or connect.get("code") or ""
        s.qr_code = qr
        db.commit()
        db.refresh(s)
    except Exception as e:
        s.status = "error"
        s.qr_code = f"error: {e}"
        db.commit()
    return _session_out(s)


@router.get("/sessions/{session_id}/qr")
async def get_qr(session_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    s = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.id == session_id,
        models.EvolutionSession.user_id == user.id,
    ).first()
    if not s:
        raise HTTPException(404, "Sesión no encontrada")
    try:
        connect = await evolution_client.connect_instance(s.instance_name)
        s.qr_code = connect.get("base64") or connect.get("code") or s.qr_code
        status = await evolution_client.fetch_status(s.instance_name)
        state = status.get("instance", {}).get("state") or status.get("state")
        if state == "open":
            s.status = "connected"
        db.commit()
    except Exception as e:
        # Evolution instance gone (e.g. DEL_INSTANCE timeout, Evolution restart
        # wiped tmpfs). Remove stale DB row so client refetches sessions list.
        msg = str(e).lower()
        if "404" in msg or "not found" in msg or "does not exist" in msg:
            db.delete(s)
            db.commit()
            raise HTTPException(404, "Sesión expirada — fue limpiada por Evolution")
        return {"qr_code": s.qr_code, "status": s.status, "error": str(e)}
    return {"qr_code": s.qr_code, "status": s.status}


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    s = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.id == session_id,
        models.EvolutionSession.user_id == user.id,
    ).first()
    if not s:
        raise HTTPException(404, "Sesión no encontrada")
    try:
        await evolution_client.logout_instance(s.instance_name)
        await evolution_client.delete_instance(s.instance_name)
    except Exception:
        pass
    db.delete(s)
    db.commit()
    return {"ok": True}


async def _perform_sync_chats(s: models.EvolutionSession, user: models.User, db: Session, fetch_msgs_per_chat: int = 10) -> dict:
    """Pull chats + contacts from Evolution and import. Optionally fetch last N
    messages per chat so the UI shows history like WhatsApp Web."""
    try:
        chats = await evolution_client.fetch_chats(s.instance_name)
        contacts_wa = await evolution_client.fetch_contacts(s.instance_name)
    except Exception:
        return {"imported": 0, "updated": 0, "contacts_imported": 0, "messages_imported": 0}

    # Evolution v2 chat entries contain: remoteJid, pushName (real contact/
    # group name), profilePicUrl, updatedAt, and lastMessage (full envelope
    # with key.remoteJidAlt that holds the real PN when remoteJid is a LID).
    # findContacts gives us the same name-by-jid map for fallbacks.
    name_by_jid = {}
    # Group contacts by pushName so we can detect the same person appearing
    # under both a @lid entry and a @s.whatsapp.net entry — a heuristic but
    # reliable bridge when a direct chat hasn't happened yet.
    name_to_jids: dict[str, list[str]] = {}
    for c in contacts_wa or []:
        jid = c.get("remoteJid") or ""
        nm = (c.get("pushName") or c.get("name") or "").strip()
        if not jid:
            continue
        if nm:
            name_by_jid[jid] = nm
            name_to_jids.setdefault(nm, []).append(jid)

    # Seed lid_pn_map from pushName twins.
    for nm, jids in name_to_jids.items():
        lids = [j for j in jids if j.endswith("@lid")]
        pns = [j for j in jids if j.endswith("@s.whatsapp.net")]
        if lids and pns:
            # If the name maps to multiple PNs we can't safely pick one — skip.
            pn = pns[0] if len(pns) == 1 else ""
            if pn:
                for lid in lids:
                    _upsert_lid_pn(db, user.workspace_id, lid, pn, nm, source="pushname")

    imported = 0
    updated = 0
    messages_imported = 0
    created_convs: list[models.Conversation] = []

    for ch in chats or []:
        # v2: `id` is a DB UUID (e.g. "cmo7n849c..."), not a JID. JID is in `remoteJid`.
        remote_jid = ch.get("remoteJid") or ""
        if not remote_jid:
            continue
        is_group = "@g.us" in remote_jid
        phone = remote_jid.split("@")[0]
        pkey = _phone_key(phone)
        # Mine the lastMessage envelope for a real PN when remoteJid is @lid.
        last_msg = ch.get("lastMessage") or {}
        last_key = last_msg.get("key") or {}
        alt_jid = last_key.get("remoteJidAlt") or ""
        real_phone = ""
        if alt_jid.endswith("@s.whatsapp.net"):
            real_phone = alt_jid.split("@")[0]
            # Authoritative LID↔PN pair direct from the chat itself.
            if remote_jid.endswith("@lid"):
                _upsert_lid_pn(db, user.workspace_id, remote_jid, alt_jid,
                               ch.get("pushName") or "", source="chat_alt")
        elif not remote_jid.endswith("@lid"):
            real_phone = phone  # already a PN-style JID
        match_key = _phone_key(real_phone) or pkey

        crm = None
        for c in db.query(models.Contact).filter(
            models.Contact.workspace_id == user.workspace_id
        ).all():
            if _phone_key(c.phone or "") == match_key and match_key:
                crm = c; break

        wa_name = ch.get("pushName") or name_by_jid.get(remote_jid) or ""
        display_name = (crm.name if crm else None) or wa_name or (real_phone or phone)
        last_msg_at = ch.get("updatedAt") or ch.get("lastMessageTimestamp")
        try:
            if isinstance(last_msg_at, (int, float)):
                last_msg_at = datetime.utcfromtimestamp(last_msg_at / 1000 if last_msg_at > 10**12 else last_msg_at)
            elif isinstance(last_msg_at, str):
                last_msg_at = datetime.fromisoformat(last_msg_at.replace("Z", ""))
        except Exception:
            last_msg_at = None

        existing = _find_matching_conv(db, None, s, remote_jid, match_key)
        if existing:
            existing.session_id = s.id
            if crm and existing.contact_id != crm.id:
                existing.contact_id = crm.id
                existing.contact_name = crm.name
            # Promote the real phone + remember the LID we came from.
            if real_phone and not is_group:
                if not existing.contact_phone or existing.contact_phone == phone:
                    existing.contact_phone = real_phone
                if remote_jid.endswith("@lid") and not existing.lid_jid:
                    existing.lid_jid = remote_jid
            if wa_name and (not existing.contact_name or existing.contact_name == phone):
                existing.contact_name = wa_name
            if last_msg_at and (not existing.last_message_at or last_msg_at > existing.last_message_at):
                existing.last_message_at = last_msg_at
            updated += 1
            created_convs.append(existing)
        else:
            conv = models.Conversation(
                workspace_id=user.workspace_id,
                session_id=s.id,
                remote_jid=remote_jid,
                lid_jid=(remote_jid if remote_jid.endswith("@lid") and real_phone else None),
                contact_id=crm.id if crm else None,
                contact_name=display_name,
                contact_phone=(real_phone or phone) if not is_group else phone,
                assigned_to=user.id,
                last_message_at=last_msg_at,
            )
            db.add(conv)
            db.flush()
            created_convs.append(conv)
            imported += 1

    # Upsert CRM contacts from WA, tagged to this session.
    # v2 exposes pushName (real contact name) — use it instead of digits.
    crm_imported = 0
    for c in contacts_wa or []:
        jid = c.get("remoteJid") or ""
        # Skip groups + anything without a PN-style JID (the CRM is for people).
        if not jid or "@g.us" in jid or "@s.whatsapp.net" not in jid:
            continue
        phone = jid.split("@")[0]
        pkey = _phone_key(phone)
        wa_name = (c.get("pushName") or c.get("name") or "").strip()
        exists = None
        for existing in db.query(models.Contact).filter(
            models.Contact.workspace_id == user.workspace_id
        ).all():
            if _phone_key(existing.phone or "") == pkey and pkey:
                exists = existing; break
        if not exists:
            db.add(models.Contact(
                workspace_id=user.workspace_id,
                owner_id=user.id,
                name=wa_name or phone,
                phone=phone,
                source="whatsapp",
                source_session_id=s.id,
            ))
            crm_imported += 1
        else:
            if not exists.source_session_id:
                exists.source_session_id = s.id
            if wa_name and (not exists.name or exists.name == phone):
                exists.name = wa_name

    db.commit()

    # Pull last N messages per conversation
    if fetch_msgs_per_chat > 0:
        for conv in created_convs[:50]:   # cap to avoid Evolution overload
            try:
                msgs = await evolution_client.fetch_messages(s.instance_name, conv.remote_jid, limit=fetch_msgs_per_chat)
            except Exception:
                msgs = []
            for m in msgs or []:
                key = m.get("key") or {}
                mid = key.get("id")
                if not mid:
                    continue
                from_me = bool(key.get("fromMe"))
                msg_content = m.get("message") or {}
                body_text, media_type = _extract_body(msg_content)
                push = m.get("pushName") or ""
                author_phone = _participant_phone(key, db, user.workspace_id)
                author_label = (
                    _resolve_author_label(db, user.workspace_id, author_phone, push)
                    if author_phone else push
                )
                # Scope dedup to THIS conversation so a duplicate conv in a
                # different workspace (seed/admin leftover) doesn't block the
                # current user from importing their own copy of the message.
                existing_msg = db.query(models.Message).filter(
                    models.Message.evolution_message_id == mid,
                    models.Message.conversation_id == conv.id,
                ).first()
                if existing_msg:
                    # Backfill fields that may have been added after the original
                    # import. The LID↔PN mapping is populated during the same
                    # sync call, so we may be able to upgrade a previously
                    # stored LID-digit `author_phone` to the resolved PN.
                    changed = False
                    raw_jid = _participant_jid(key)
                    resolved_is_pn = author_phone and raw_jid.endswith("@lid") and author_phone != raw_jid.split("@")[0]
                    if author_phone and (
                        not existing_msg.author_phone
                        or (resolved_is_pn and existing_msg.author_phone != author_phone)
                    ):
                        existing_msg.author_phone = author_phone
                        changed = True
                    if author_label and existing_msg.author_name != author_label:
                        if not existing_msg.author_name or existing_msg.author_name.isdigit():
                            existing_msg.author_name = author_label
                            changed = True
                    if changed:
                        updated += 1
                    continue
                ts = m.get("messageTimestamp")
                try:
                    ts = datetime.utcfromtimestamp(int(ts)) if ts else datetime.utcnow()
                except Exception:
                    ts = datetime.utcnow()
                db.add(models.Message(
                    conversation_id=conv.id,
                    direction="outbound" if from_me else "inbound",
                    body=body_text,
                    media_type=media_type,
                    from_me=from_me,
                    author_name=author_label,
                    author_phone=author_phone or None,
                    evolution_message_id=mid,
                    timestamp=ts,
                ))
                messages_imported += 1
                # Keep conversation preview/sort field in sync with the newest msg.
                if body_text and (not conv.last_message_at or ts > conv.last_message_at):
                    conv.last_message = body_text
                    conv.last_message_at = ts
        db.commit()

    # Auto-merge duplicates created across earlier sessions / JID shapes.
    # Group this user's conversations by normalized phone key; whichever has
    # the most messages wins, everything else gets merged into it.
    merged = 0
    by_key: dict[str, list[models.Conversation]] = {}
    for cv in db.query(models.Conversation).filter(
        models.Conversation.workspace_id == user.workspace_id,
        models.Conversation.assigned_to == user.id,
    ).all():
        k = _phone_key(cv.contact_phone or "")
        if not k:
            continue
        by_key.setdefault(k, []).append(cv)
    for k, group in by_key.items():
        if len(group) < 2:
            continue
        # Rank: most messages, then most recent, then numeric id.
        def _score(c: models.Conversation) -> tuple:
            cnt = db.query(models.Message).filter(models.Message.conversation_id == c.id).count()
            ts = c.last_message_at or datetime.min
            return (cnt, ts.timestamp() if ts != datetime.min else 0, -c.id)
        group.sort(key=_score, reverse=True)
        winner = group[0]
        for loser in group[1:]:
            # Preserve the losing jid so future inbound with that shape still
            # lands in the winner.
            if loser.remote_jid and loser.remote_jid.endswith("@lid") and not winner.lid_jid:
                winner.lid_jid = loser.remote_jid
            db.query(models.Message).filter(
                models.Message.conversation_id == loser.id
            ).update({"conversation_id": winner.id}, synchronize_session=False)
            if loser.last_message_at and (not winner.last_message_at or loser.last_message_at > winner.last_message_at):
                winner.last_message = loser.last_message
                winner.last_message_at = loser.last_message_at
            winner.unread = (winner.unread or 0) + (loser.unread or 0)
            db.delete(loser)
            merged += 1
    if merged:
        db.commit()

    return {"imported": imported, "updated": updated, "contacts_imported": crm_imported, "messages_imported": messages_imported, "merged": merged}


@router.post("/sessions/{session_id}/sync-chats")
async def sync_chats(session_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Import existing WhatsApp chats + contacts from Evolution into DB.
    Re-links any orphaned (session_id NULL) conversations that match.
    """
    s = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.id == session_id,
        models.EvolutionSession.user_id == user.id,
    ).first()
    if not s:
        raise HTTPException(404, "Sesión no encontrada")
    if s.status != "connected":
        raise HTTPException(400, "Sesión no conectada. Escanea el QR primero.")

    return await _perform_sync_chats(s, user, db, fetch_msgs_per_chat=20)


# Conversations -----------------------------------------------------------
def _conv_out(c: models.Conversation) -> dict:
    return {
        "id": c.id, "session_id": c.session_id, "contact_id": c.contact_id,
        "remote_jid": c.remote_jid, "lid_jid": c.lid_jid,
        "contact_name": c.contact_name,
        "contact_phone": c.contact_phone, "last_message": c.last_message,
        "last_message_at": c.last_message_at.isoformat() if c.last_message_at else None,
        "unread": c.unread, "status": c.status,
    }


def _msg_out(m: models.Message, db: Session | None = None, workspace_id: int | None = None) -> dict:
    # If we have DB context, resolve the author's display name via CRM on each
    # read. That way, renaming a contact updates every historical group
    # message attributed to them without a batch backfill.
    author = m.author_name or ""
    if db and workspace_id and m.author_phone:
        author = _resolve_author_label(db, workspace_id, m.author_phone, m.author_name or "")
    return {
        "id": m.id, "conversation_id": m.conversation_id,
        "direction": m.direction, "body": m.body, "media_url": m.media_url,
        "media_type": m.media_type, "from_me": m.from_me,
        "author_name": author,
        "author_phone": m.author_phone,
        "timestamp": m.timestamp.isoformat() if m.timestamp else None,
    }


@router.post("/conversations/{src_id}/merge-into/{dst_id}")
async def merge_conversations(src_id: int, dst_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Move all messages from `src_id` into `dst_id` and delete the source.
    Use for merging duplicate threads (e.g. @lid vs @s.whatsapp.net for same contact)."""
    if src_id == dst_id:
        raise HTTPException(400, "Son la misma conversación")
    src = db.query(models.Conversation).filter(
        models.Conversation.id == src_id,
        models.Conversation.workspace_id == user.workspace_id,
        models.Conversation.assigned_to == user.id,
    ).first()
    dst = db.query(models.Conversation).filter(
        models.Conversation.id == dst_id,
        models.Conversation.workspace_id == user.workspace_id,
        models.Conversation.assigned_to == user.id,
    ).first()
    if not src or not dst:
        raise HTTPException(404, "Conversación no encontrada")
    # Move messages
    db.query(models.Message).filter(models.Message.conversation_id == src_id).update(
        {"conversation_id": dst_id}, synchronize_session=False
    )
    # Take src's metadata if dst is empty-ish
    if not dst.last_message_at or (src.last_message_at and src.last_message_at > dst.last_message_at):
        dst.last_message = src.last_message
        dst.last_message_at = src.last_message_at
    dst.unread = (dst.unread or 0) + (src.unread or 0)
    db.delete(src)
    db.commit()
    return {"ok": True, "kept": dst_id, "removed": src_id}


@router.get("/conversations/{conv_id}/duplicates")
def find_duplicates(conv_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Return likely duplicate conversations for a given conv
    (same user, phone normalizes to same key)."""
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == conv_id,
        models.Conversation.workspace_id == user.workspace_id,
        models.Conversation.assigned_to == user.id,
    ).first()
    if not conv:
        raise HTTPException(404, "No encontrada")
    my_key = _phone_key(conv.contact_phone or "")
    others = db.query(models.Conversation).filter(
        models.Conversation.workspace_id == user.workspace_id,
        models.Conversation.assigned_to == user.id,
        models.Conversation.id != conv_id,
    ).all()
    # Match any with same phone_key OR same CRM contact_id
    dupes = []
    for o in others:
        if conv.contact_id and o.contact_id == conv.contact_id:
            dupes.append(o)
        elif my_key and _phone_key(o.contact_phone or "") == my_key:
            dupes.append(o)
    return [_conv_out(d) for d in dupes]


@router.post("/conversations/{conv_id}/link-contact")
async def link_contact(conv_id: int, payload: LinkContactIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Associate a conversation (often stuck on @lid) with a real phone number.
    Creates/finds a CRM contact, relinks the conversation, and re-points its
    remote_jid to `<phone>@s.whatsapp.net` so sending works."""
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == conv_id,
        models.Conversation.workspace_id == user.workspace_id,
        models.Conversation.assigned_to == user.id,
    ).first()
    if not conv:
        raise HTTPException(404, "Conversación no encontrada")

    phone = _sanitize_phone(payload.phone)
    if not phone:
        raise HTTPException(400, "Número requerido (con código país, sin +)")

    # Verify via Evolution that this number exists + get the canonical variant
    session = None
    if conv.session_id:
        session = db.query(models.EvolutionSession).filter(
            models.EvolutionSession.id == conv.session_id
        ).first()
    if not session:
        session = await _pick_active_session(user.id, db)
    if session:
        resolved = await evolution_client.resolve_number(session.instance_name, phone)
        if resolved:
            phone = resolved

    name = (payload.name or conv.contact_name or phone).strip() or phone

    # Upsert contact
    contact = db.query(models.Contact).filter(
        models.Contact.workspace_id == user.workspace_id,
        models.Contact.phone == phone,
    ).first()
    if not contact:
        contact = models.Contact(
            workspace_id=user.workspace_id,
            owner_id=user.id,
            name=name,
            phone=phone,
            source="whatsapp",
        )
        db.add(contact)
        db.flush()

    # Relink conv. Preserve the original @lid so future inbound messages
    # that still carry the LID route back to this same conversation.
    if conv.remote_jid and conv.remote_jid.endswith("@lid") and not conv.lid_jid:
        conv.lid_jid = conv.remote_jid
    conv.contact_id = contact.id
    conv.contact_name = contact.name
    conv.contact_phone = phone
    conv.remote_jid = f"{phone}@s.whatsapp.net"
    db.commit()
    db.refresh(conv)
    return {"conversation": _conv_out(conv), "contact": {"id": contact.id, "name": contact.name, "phone": contact.phone}}


@router.get("/conversations")
def list_conversations(session_id: int | None = None, all: bool = False, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Return conversations assigned to this user.
    - session_id: filter to a specific session (default behavior when sidebar selects one).
    - all=true: override, return every conversation across all sessions.
    Orphan conversations (session_id NULL) are always shown only in `all` mode
    or when attached to the requested session.
    """
    qry = db.query(models.Conversation).filter(
        models.Conversation.workspace_id == user.workspace_id,
        models.Conversation.assigned_to == user.id,
    )
    if session_id and not all:
        qry = qry.filter(models.Conversation.session_id == session_id)
    rows = qry.order_by(models.Conversation.last_message_at.desc().nullslast()).all()
    return [_conv_out(c) for c in rows]


@router.get("/messages/{msg_id}/media")
async def get_message_media(msg_id: int, token: str | None = None, db: Session = Depends(get_db)):
    """Stream decrypted WhatsApp media for a message. Uses a query-string token
    so plain <img>/<audio>/<video> tags can load directly without needing
    custom fetch + blob handling on the frontend."""
    # Support both Authorization header and ?token= query for media URLs.
    if token:
        try:
            payload = decode_token(token)
            user_id = int(payload.get("sub") or 0)
        except Exception:
            raise HTTPException(401, "Token inválido")
        user = db.query(models.User).filter(models.User.id == user_id).first()
    else:
        raise HTTPException(401, "Token requerido")
    if not user or not user.is_active:
        raise HTTPException(401, "Usuario no encontrado")

    m = db.query(models.Message).filter(models.Message.id == msg_id).first()
    if not m or not m.evolution_message_id:
        raise HTTPException(404, "Mensaje no encontrado")
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == m.conversation_id,
        models.Conversation.workspace_id == user.workspace_id,
    ).first()
    if not conv:
        raise HTTPException(404, "Conversación no encontrada")
    session = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.id == conv.session_id
    ).first() if conv.session_id else None
    if not session:
        session = await _pick_active_session(user.id, db)
    if not session:
        raise HTTPException(400, "Sin sesión WhatsApp activa")
    # Rebuild the Baileys key Evolution needs to locate the ciphertext.
    # The original jid may have been a @lid that we later promoted to
    # @s.whatsapp.net — fall back to the stored lid_jid in that case.
    key_jid = conv.lid_jid or conv.remote_jid or ""
    key = {"id": m.evolution_message_id, "remoteJid": key_jid, "fromMe": bool(m.from_me)}
    try:
        data = await evolution_client.fetch_media_base64(session.instance_name, key)
    except Exception as first_err:
        # Try the promoted PN jid if the lid one failed (or vice versa).
        alt_jid = conv.remote_jid if key_jid == conv.lid_jid else (conv.lid_jid or "")
        if alt_jid and alt_jid != key_jid:
            try:
                data = await evolution_client.fetch_media_base64(
                    session.instance_name,
                    {"id": m.evolution_message_id, "remoteJid": alt_jid, "fromMe": bool(m.from_me)},
                )
            except Exception as e:
                raise HTTPException(502, f"Error descargando media: {e}")
        else:
            raise HTTPException(502, f"Error descargando media: {first_err}")
    b64 = data.get("base64") or ""
    mime = data.get("mimetype") or "application/octet-stream"
    try:
        raw = base64.b64decode(b64)
    except Exception:
        raise HTTPException(500, "Media corrupta")
    return Response(content=raw, media_type=mime, headers={
        "Cache-Control": "private, max-age=3600",
    })


@router.post("/send-media")
async def send_media_msg(
    conversation_id: int = Form(...),
    caption: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    """Upload + forward a file to WhatsApp via Evolution v2. Derives mediatype
    from the upload's MIME so images/videos/audios/documents all work through
    the same endpoint."""
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.workspace_id == user.workspace_id,
    ).first()
    if not conv:
        raise HTTPException(404, "Conversación no encontrada")
    session = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.id == conv.session_id
    ).first() if conv.session_id else None
    if not session:
        session = await _pick_active_session(user.id, db)
    if not session:
        raise HTTPException(400, "Sesión WhatsApp no conectada")

    data = await file.read()
    if not data:
        raise HTTPException(400, "Archivo vacío")
    mimetype = file.content_type or "application/octet-stream"
    b64 = base64.b64encode(data).decode()

    if mimetype.startswith("image/"):
        mediatype = "image"
    elif mimetype.startswith("video/"):
        mediatype = "video"
    elif mimetype.startswith("audio/"):
        mediatype = "audio"
    else:
        mediatype = "document"

    number = await _resolve_send_number(session, conv, db)
    if not number and conv.remote_jid:
        number = conv.remote_jid
    if not number:
        raise HTTPException(400, "No pude determinar destino")

    try:
        if mediatype == "audio":
            # Voice notes use a dedicated endpoint so WhatsApp renders them
            # as PTT instead of a regular audio attachment.
            res = await evolution_client.send_audio(session.instance_name, number, b64)
        else:
            res = await evolution_client.send_media(
                session.instance_name, number,
                media=b64, caption=caption, media_type=mediatype,
                file_name=file.filename or "", mimetype=mimetype,
            )
    except Exception as e:
        raise HTTPException(502, str(e))

    body_preview = caption or f"[{mediatype.capitalize()}]"
    m = models.Message(
        conversation_id=conv.id,
        direction="outbound",
        body=body_preview,
        media_type=mediatype,
        from_me=True,
        author_name=user.name,
        evolution_message_id=(res.get("key") or {}).get("id"),
        timestamp=datetime.utcnow(),
    )
    db.add(m)
    conv.last_message = body_preview
    conv.last_message_at = datetime.utcnow()
    db.commit()
    db.refresh(m)
    await manager.broadcast(
        user.workspace_id,
        {"type": "message", "message": _msg_out(m, db, user.workspace_id), "conversation_id": conv.id},
    )
    return _msg_out(m, db, user.workspace_id)


@router.post("/presence")
async def emit_presence(payload: dict, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Forward the user's typing status to WhatsApp (shown to the other end as
    'escribiendo…'). Called from the composer on keystrokes, rate-limited
    client-side."""
    conv_id = int(payload.get("conversation_id") or 0)
    presence = payload.get("presence") or "composing"
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == conv_id,
        models.Conversation.workspace_id == user.workspace_id,
    ).first()
    if not conv or not conv.session_id:
        return {"ok": False}
    session = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.id == conv.session_id
    ).first()
    if not session:
        return {"ok": False}
    target = conv.remote_jid or conv.contact_phone or ""
    if not target:
        return {"ok": False}
    await evolution_client.send_presence(session.instance_name, target, presence)
    return {"ok": True}


@router.get("/conversations/{conv_id}/messages")
def list_messages(conv_id: int, limit: int = 200, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == conv_id,
        models.Conversation.workspace_id == user.workspace_id,
    ).first()
    if not conv:
        raise HTTPException(404, "Conversación no encontrada")
    msgs = db.query(models.Message).filter(
        models.Message.conversation_id == conv_id
    ).order_by(models.Message.timestamp.asc()).limit(limit).all()
    conv.unread = 0
    db.commit()
    return [_msg_out(m, db, user.workspace_id) for m in msgs]


import re


def _sanitize_phone(p: str) -> str:
    """Strip everything but digits. Evolution expects raw number with country code."""
    return re.sub(r"\D+", "", p or "")


def _phone_key(raw: str) -> str:
    """Canonical phone key for dedup. Strips non-digits; for Mexico, drops the
    leading '1' after '52' so 52NNNN and 521NNNN collide to the same key."""
    n = _sanitize_phone(raw)
    if n.startswith("521") and len(n) == 13:
        n = "52" + n[3:]
    return n


def _find_matching_conv(db: Session, user: models.User, session: models.EvolutionSession, remote_jid: str, phone_key: str) -> models.Conversation | None:
    """Find an existing conversation for this user that represents the same
    contact, regardless of JID shape (@lid vs @s.whatsapp.net) or MX-1 variant.

    Match priority:
      1. Exact remote_jid.
      2. lid_jid match (conv was linked from a @lid — inbound still uses @lid).
      3. CRM contact whose phone normalizes to the same key.
      4. Any of the user's conversations whose contact_phone normalizes to the same key.
    """
    base = db.query(models.Conversation).filter(
        models.Conversation.workspace_id == session.workspace_id,
        models.Conversation.assigned_to == session.user_id,
    )
    exact = base.filter(models.Conversation.remote_jid == remote_jid).first()
    if exact:
        return exact

    # Inbound @lid that was previously linked to a real phone — route back to
    # the same conv so the user isn't asked to re-link.
    if remote_jid and remote_jid.endswith("@lid"):
        by_lid = base.filter(models.Conversation.lid_jid == remote_jid).first()
        if by_lid:
            return by_lid

    if phone_key:
        # CRM contact lookup — if user has a contact saved for this phone,
        # fetch any conv already pointing to that contact.
        crm = db.query(models.Contact).filter(
            models.Contact.workspace_id == session.workspace_id,
        ).all()
        for c in crm:
            if _phone_key(c.phone or "") == phone_key:
                by_contact = base.filter(models.Conversation.contact_id == c.id).first()
                if by_contact:
                    return by_contact
        # Scan user's conversations by normalized phone
        for cv in base.all():
            if _phone_key(cv.contact_phone or "") == phone_key:
                return cv
    return None


@router.post("/conversations/start")
async def start_conversation(payload: StartConvIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Open a new outbound conversation: pick session + contact (or raw phone) + send first message."""
    session = db.query(models.EvolutionSession).filter(
        models.EvolutionSession.id == payload.session_id,
        models.EvolutionSession.user_id == user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Sesión no encontrada")
    if session.status != "connected":
        raise HTTPException(400, f"Sesión no conectada (estado: {session.status}). Escanea el QR primero.")

    # Resolve target phone
    contact = None
    phone = _sanitize_phone(payload.phone or "")
    name = payload.contact_name or ""
    if payload.contact_id:
        contact = db.query(models.Contact).filter(
            models.Contact.id == payload.contact_id,
            models.Contact.workspace_id == user.workspace_id,
        ).first()
        if not contact:
            raise HTTPException(404, "Contacto no encontrado")
        phone = _sanitize_phone(contact.phone or "")
        name = name or contact.name
    if not phone:
        raise HTTPException(400, "Número de teléfono requerido (con código de país, sin +)")

    remote_jid = f"{phone}@s.whatsapp.net"

    # Find existing conversation (any session, same phone) or create one.
    # Searching workspace-wide avoids creating a fresh @s.whatsapp.net thread
    # next to the historical @lid one for the same contact.
    pkey = _phone_key(phone)
    conv = _find_matching_conv(db, None, session, remote_jid, pkey)
    if conv:
        # Re-adopt any orphaned row + upgrade jid to the canonical PN form.
        if conv.session_id != session.id:
            conv.session_id = session.id
        if remote_jid.endswith("@s.whatsapp.net") and conv.remote_jid.endswith("@lid"):
            if not conv.lid_jid:
                conv.lid_jid = conv.remote_jid
            conv.remote_jid = remote_jid
            conv.contact_phone = phone
    else:
        conv = models.Conversation(
            workspace_id=user.workspace_id,
            session_id=session.id,
            contact_id=contact.id if contact else None,
            remote_jid=remote_jid,
            contact_name=name or phone,
            contact_phone=phone,
            assigned_to=user.id,
        )
        db.add(conv)
        db.flush()

    # Resolve to a WhatsApp-registered variant (MX sometimes needs the '1' after 52)
    resolved = await evolution_client.resolve_number(session.instance_name, phone)
    if not resolved:
        raise HTTPException(400, f"El número {phone} no está registrado en WhatsApp.")
    phone = resolved
    # Keep conv aligned with the resolved number
    new_jid = f"{phone}@s.whatsapp.net"
    if conv.remote_jid != new_jid:
        conv.remote_jid = new_jid
        conv.contact_phone = phone
        db.commit()
    try:
        res = await evolution_client.send_text(session.instance_name, phone, payload.text)
    except Exception as e:
        raise HTTPException(502, str(e))

    m = models.Message(
        conversation_id=conv.id,
        direction="outbound",
        body=payload.text,
        from_me=True,
        author_name=user.name,
        evolution_message_id=(res.get("key") or {}).get("id"),
        timestamp=datetime.utcnow(),
    )
    db.add(m)
    conv.last_message = payload.text
    conv.last_message_at = datetime.utcnow()
    db.commit()
    db.refresh(conv)
    db.refresh(m)
    await manager.broadcast(user.workspace_id, {"type": "message", "message": _msg_out(m), "conversation_id": conv.id})
    return {"conversation": _conv_out(conv), "message": _msg_out(m)}


def _participant_jid(key: dict) -> str:
    """Raw JID of the message sender (LID or PN)."""
    if not isinstance(key, dict):
        return ""
    alt = key.get("participantAlt") or ""
    p = key.get("participant") or ""
    if alt.endswith("@s.whatsapp.net"):
        return alt
    return p or alt


def _participant_phone(key: dict, db: Session | None = None, workspace_id: int | None = None) -> str:
    """Resolve the sender's real phone digits. Evolution v2 / Baileys v7 only
    hands us `participant: <lid>@lid` for group messages (no participantAlt),
    so we consult the LID↔PN mapping we built at sync time before falling
    back to the LID digits."""
    jid = _participant_jid(key)
    if not jid:
        return ""
    if jid.endswith("@s.whatsapp.net"):
        return jid.split("@")[0]
    if jid.endswith("@lid") and db is not None and workspace_id is not None:
        row = db.query(models.LidPnMap).filter(
            models.LidPnMap.workspace_id == workspace_id,
            models.LidPnMap.lid_jid == jid,
        ).first()
        if row and row.pn_jid.endswith("@s.whatsapp.net"):
            return row.pn_jid.split("@")[0]
    # Last resort: LID digits. Won't match CRM phones but keeps something to show.
    return jid.split("@")[0]


def _resolve_author_label(db: Session, workspace_id: int, phone: str, push_name: str) -> str:
    """Prefer the CRM's saved name so a phonebook rename updates every group
    message retroactively. Fall back to the WhatsApp pushName, then the raw
    phone number when nothing else is available."""
    if phone:
        pkey = _phone_key(phone)
        if pkey:
            for c in db.query(models.Contact).filter(
                models.Contact.workspace_id == workspace_id
            ).all():
                if _phone_key(c.phone or "") == pkey:
                    return c.name or push_name or phone
    return push_name or phone or ""


def _upsert_lid_pn(db: Session, workspace_id: int, lid_jid: str, pn_jid: str, push_name: str = "", source: str = "chat_alt") -> None:
    """Idempotent insert of a LID↔PN pair. Keeps the first-seen pairing stable
    and only upgrades the pushName when a later entry gives us a better one."""
    if not lid_jid or not pn_jid or not lid_jid.endswith("@lid") or not pn_jid.endswith("@s.whatsapp.net"):
        return
    existing = db.query(models.LidPnMap).filter(
        models.LidPnMap.workspace_id == workspace_id,
        models.LidPnMap.lid_jid == lid_jid,
    ).first()
    if existing:
        if push_name and not existing.push_name:
            existing.push_name = push_name
        return
    db.add(models.LidPnMap(
        workspace_id=workspace_id, lid_jid=lid_jid, pn_jid=pn_jid,
        push_name=push_name or None, source=source,
    ))


def _extract_body(msg_content: dict) -> tuple[str, str | None]:
    """Pull a readable body + media_type from a Baileys message envelope.
    Covers plain text, extended text, captioned media, edits, stickers,
    reactions, location, contacts — falls back to an empty body."""
    if not isinstance(msg_content, dict):
        return "", None
    # Plain text
    if msg_content.get("conversation"):
        return msg_content["conversation"], None
    # Extended text (replies, previews)
    et = msg_content.get("extendedTextMessage")
    if isinstance(et, dict) and et.get("text"):
        return et["text"], None
    # Media with caption
    for k, mtype, fallback in (
        ("imageMessage", "image", "[Imagen]"),
        ("videoMessage", "video", "[Video]"),
        ("documentMessage", "document", "[Documento]"),
        ("documentWithCaptionMessage", "document", "[Documento]"),
        ("audioMessage", "audio", "[Audio]"),
        ("pttMessage", "audio", "[Nota de voz]"),
        ("voiceMessage", "audio", "[Nota de voz]"),
        ("stickerMessage", "sticker", "[Sticker]"),
    ):
        m = msg_content.get(k)
        if isinstance(m, dict):
            cap = m.get("caption") or m.get("fileName") or ""
            return (cap or fallback), mtype
    # Reactions
    rx = msg_content.get("reactionMessage")
    if isinstance(rx, dict) and rx.get("text"):
        return f"[Reacción {rx['text']}]", None
    # Location
    loc = msg_content.get("locationMessage")
    if isinstance(loc, dict):
        return f"[Ubicación] {loc.get('name') or ''}".strip(), None
    # Contact card
    if msg_content.get("contactMessage"):
        return "[Contacto]", None
    if msg_content.get("contactsArrayMessage"):
        return "[Contactos]", None
    # Edits wrap the new content
    pm = msg_content.get("protocolMessage")
    if isinstance(pm, dict) and isinstance(pm.get("editedMessage"), dict):
        inner, mt = _extract_body(pm["editedMessage"])
        if inner:
            return inner, mt
    # View-once
    vo = msg_content.get("viewOnceMessage") or msg_content.get("viewOnceMessageV2")
    if isinstance(vo, dict) and isinstance(vo.get("message"), dict):
        return _extract_body(vo["message"])
    # Ephemeral wrapper
    eph = msg_content.get("ephemeralMessage")
    if isinstance(eph, dict) and isinstance(eph.get("message"), dict):
        return _extract_body(eph["message"])
    return "", None


async def _pick_active_session(user_id: int, db: Session) -> models.EvolutionSession | None:
    """Fallback — any connected session this user owns."""
    return db.query(models.EvolutionSession).filter(
        models.EvolutionSession.user_id == user_id,
        models.EvolutionSession.status == "connected",
    ).first()


async def _resolve_send_number(session: models.EvolutionSession, conv: models.Conversation, db: Session) -> str:
    """Pick the best phone for sending. Checks CRM contact (if linked),
    conv.contact_phone, and remote_jid. Validates via Evolution + MX variants.

    LID handling: WhatsApp's privacy LIDs (remote_jid ending in @lid) can't
    be used as a plain number. We only try CRM/contact_phone candidates,
    skipping the LID part. If nothing else works and conv has ONLY a LID,
    we return the full JID so Evolution gets a precise error.
    """
    candidates: list[str] = []
    is_lid = bool(conv.remote_jid and conv.remote_jid.endswith("@lid"))

    if conv.contact_id:
        ctc = db.query(models.Contact).filter(models.Contact.id == conv.contact_id).first()
        if ctc and ctc.phone:
            candidates.append(re.sub(r"\D+", "", ctc.phone))
    # Skip conv.contact_phone if it's the LID number (looks like a real number but isn't)
    if conv.contact_phone and not is_lid:
        candidates.append(re.sub(r"\D+", "", conv.contact_phone))
    if conv.remote_jid and not is_lid:
        candidates.append(conv.remote_jid.split("@")[0])

    seen, uniq = set(), []
    for c in candidates:
        if c and c not in seen:
            seen.add(c); uniq.append(c)

    for n in uniq:
        resolved = await evolution_client.resolve_number(session.instance_name, n)
        if resolved:
            return resolved

    # If only LID is available and we didn't find a verified variant,
    # return empty so the send layer falls back to sending via full JID.
    return "" if is_lid and not uniq else (uniq[0] if uniq else "")


@router.post("/send")
async def send_message(payload: SendIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    conv = db.query(models.Conversation).filter(
        models.Conversation.id == payload.conversation_id,
        models.Conversation.workspace_id == user.workspace_id,
    ).first()
    if not conv:
        raise HTTPException(404, "Conversación no encontrada")
    session = None
    if conv.session_id:
        session = db.query(models.EvolutionSession).filter(
            models.EvolutionSession.id == conv.session_id
        ).first()
    if not session:
        # Conversation was orphaned (session deleted). Auto-link to any active session.
        session = await _pick_active_session(user.id, db)
        if not session:
            raise HTTPException(400, "No hay sesión de WhatsApp conectada. Conecta una primero.")
        conv.session_id = session.id
        db.commit()
    number = await _resolve_send_number(session, conv, db)
    # Fallback: if we couldn't resolve a phone AND it's a LID conv, try sending
    # using the full LID JID directly. WhatsApp Web handles this natively; Baileys
    # (via Evolution) accepts a full JID as `number` in most versions.
    if not number and conv.remote_jid:
        number = conv.remote_jid
    if not number:
        raise HTTPException(400, "No pude determinar un destino para este contacto.")
    try:
        res = await evolution_client.send_text(session.instance_name, number, payload.text)
    except Exception as e:
        err = str(e)
        if conv.remote_jid and conv.remote_jid.endswith("@lid") and "exists:false" in err:
            # Evolution/Baileys couldn't deliver to the LID. Ask the user to provide the real phone.
            raise HTTPException(400,
                "Este contacto usa privacidad LID de WhatsApp. Evolution no pudo resolver "
                "el número automáticamente. Haz clic en el badge LID del chat y agrega el "
                "número real del contacto para continuar."
            )
        raise HTTPException(502, err)
    m = models.Message(
        conversation_id=conv.id,
        direction="outbound",
        body=payload.text,
        from_me=True,
        author_name=user.name,
        evolution_message_id=(res.get("key") or {}).get("id"),
        timestamp=datetime.utcnow(),
    )
    db.add(m)
    conv.last_message = payload.text
    conv.last_message_at = datetime.utcnow()
    db.commit()
    db.refresh(m)
    await manager.broadcast(user.workspace_id, {"type": "message", "message": _msg_out(m), "conversation_id": conv.id})
    return _msg_out(m)


# Webhook -----------------------------------------------------------------
@router.post("/webhook/{token}")
async def evolution_webhook(token: str, body: dict):
    """Token == instance_name. Evolution POSTs events here."""
    event = body.get("event") or ""
    data = body.get("data") or {}
    instance = body.get("instance") or token

    db = SessionLocal()
    try:
        session = db.query(models.EvolutionSession).filter(
            models.EvolutionSession.instance_name == instance
        ).first()
        if not session:
            return {"ok": False, "reason": "unknown instance"}

        if event in ("connection.update", "CONNECTION_UPDATE"):
            state = data.get("state") or data.get("status")
            prev = session.status
            if state == "open":
                session.status = "connected"
            elif state in ("close", "closed", "disconnected"):
                session.status = "disconnected"
            db.commit()

            # Auto-sync chats when a session transitions to connected.
            # Baileys populates its contact/chat store over tens of seconds after
            # pairing (full history trickles in). We run several sync waves so
            # HubOS picks up chats as they arrive, not just what existed at t=10s.
            if state == "open" and prev != "connected":
                async def _delayed_sync(session_id_local: int, user_id_local: int):
                    waves = [8, 20, 45, 90, 180]  # seconds from session start
                    prev_delay = 0
                    for delay in waves:
                        await asyncio.sleep(delay - prev_delay)
                        prev_delay = delay
                        local = SessionLocal()
                        try:
                            sess = local.query(models.EvolutionSession).filter(
                                models.EvolutionSession.id == session_id_local
                            ).first()
                            user_obj = local.query(models.User).filter(
                                models.User.id == user_id_local
                            ).first()
                            if not sess or sess.status != "connected" or not user_obj:
                                return
                            await _perform_sync_chats(sess, user_obj, local, fetch_msgs_per_chat=20)
                        except Exception as e:
                            print(f"[delayed_sync] wave @{delay}s error: {e}")
                        finally:
                            local.close()
                asyncio.create_task(_delayed_sync(session.id, session.user_id))

        elif event in ("qrcode.updated", "QRCODE_UPDATED"):
            qr = data.get("qrcode", {}).get("base64") or data.get("base64")
            if qr:
                session.qr_code = qr
                db.commit()

        elif event in ("messages.upsert", "MESSAGES_UPSERT"):
            key = data.get("key") or {}
            remote_jid = key.get("remoteJid") or ""
            # Evolution v2 exposes the LID↔PN pair directly on the message key:
            # `remoteJidAlt` is the opposite-mode JID. We prefer the PN variant
            # so conversation metadata (phone, contact match) works end-to-end
            # and fall back to the LID only when WhatsApp hid the PN.
            alt_jid = key.get("remoteJidAlt") or ""
            lid_origin = ""
            if remote_jid.endswith("@lid") and alt_jid.endswith("@s.whatsapp.net"):
                lid_origin = remote_jid
                remote_jid = alt_jid
            from_me = bool(key.get("fromMe"))
            msg_content = data.get("message") or {}
            body_text, media_type = _extract_body(msg_content)
            push_name = data.get("pushName") or ""
            phone = remote_jid.split("@")[0] if remote_jid else ""

            # Normalize the phone for dedup (handles 52/521 MX variants + @lid vs @s.whatsapp.net)
            pkey = _phone_key(phone)
            conv = _find_matching_conv(db, None, session, remote_jid, pkey)

            # CRM contact: match by any phone that normalizes to the same key
            crm_contact = None
            for c in db.query(models.Contact).filter(
                models.Contact.workspace_id == session.workspace_id
            ).all():
                if _phone_key(c.phone or "") == pkey and pkey:
                    crm_contact = c
                    break
            display_name = (crm_contact.name if crm_contact else None) or push_name or phone

            if conv:
                if not conv.session_id:
                    conv.session_id = session.id
                if crm_contact and conv.contact_id != crm_contact.id:
                    conv.contact_id = crm_contact.id
                    conv.contact_name = crm_contact.name
                # Upgrade @lid → @s.whatsapp.net once v2 hands us the real PN.
                if remote_jid.endswith("@s.whatsapp.net") and conv.remote_jid.endswith("@lid"):
                    if not conv.lid_jid:
                        conv.lid_jid = conv.remote_jid
                    conv.remote_jid = remote_jid
                    conv.contact_phone = phone
                if lid_origin and not conv.lid_jid:
                    conv.lid_jid = lid_origin
                # Backfill contact_name with pushName the first time we see one.
                if push_name and (not conv.contact_name or conv.contact_name == phone):
                    conv.contact_name = push_name
            else:
                conv = models.Conversation(
                    workspace_id=session.workspace_id,
                    session_id=session.id,
                    remote_jid=remote_jid,
                    lid_jid=lid_origin or None,
                    contact_id=crm_contact.id if crm_contact else None,
                    contact_name=display_name,
                    contact_phone=phone,
                    assigned_to=session.user_id,
                )
                db.add(conv)
                db.flush()

            # Group messages need sender attribution. For 1:1 chats the
            # conversation's contact already identifies the sender, so the
            # participant fields are typically empty.
            author_phone = _participant_phone(key, db, session.workspace_id)
            author_label = (
                _resolve_author_label(db, session.workspace_id, author_phone, push_name)
                if author_phone else push_name
            )
            # Skip duplicates: Evolution can fire MESSAGES_UPSERT for the same
            # message across history sync + regular delivery. Scoped to the
            # conversation so duplicate convs in other workspaces don't
            # swallow the insert.
            mid = key.get("id") or ""
            if mid and db.query(models.Message).filter(
                models.Message.evolution_message_id == mid,
                models.Message.conversation_id == conv.id,
            ).first():
                return {"ok": True, "dedup": True}

            # Use the real message timestamp (Evolution sends epoch seconds) so
            # out-of-order backfills don't poison the conversation preview.
            ts_raw = data.get("messageTimestamp")
            try:
                ts = datetime.utcfromtimestamp(int(ts_raw)) if ts_raw else datetime.utcnow()
            except Exception:
                ts = datetime.utcnow()

            m = models.Message(
                conversation_id=conv.id,
                direction="outbound" if from_me else "inbound",
                body=body_text,
                media_type=media_type,
                from_me=from_me,
                author_name=author_label,
                author_phone=author_phone or None,
                evolution_message_id=mid or None,
                timestamp=ts,
            )
            db.add(m)
            # Only bump the chat-list preview if this message is actually
            # newer than whatever's already shown. Otherwise a retro-delivery
            # would make the list show an older message as the "latest."
            if body_text and (not conv.last_message_at or ts >= conv.last_message_at):
                conv.last_message = body_text
                conv.last_message_at = ts
            if not from_me:
                conv.unread = (conv.unread or 0) + 1
            db.commit()
            db.refresh(m)

            # Broadcast to workspace listeners
            asyncio.create_task(manager.broadcast(
                session.workspace_id,
                {"type": "message", "message": _msg_out(m, db, session.workspace_id), "conversation_id": conv.id}
            ))

        elif event in ("presence.update", "PRESENCE_UPDATE"):
            # Forward typing / recording presence to the agent's UI so the chat
            # view can show an "escribiendo…" indicator like WhatsApp Web.
            remote_jid = data.get("id") or data.get("remoteJid") or ""
            presences = data.get("presences") or {}
            if not remote_jid and isinstance(presences, dict) and presences:
                remote_jid = next(iter(presences.keys()))
            # Pick the most informative presence across all reported participants.
            state = ""
            for v in (presences.values() if isinstance(presences, dict) else []):
                if isinstance(v, dict):
                    st = v.get("lastKnownPresence") or ""
                    if st in ("composing", "recording"):
                        state = st; break
                    state = state or st
            if not state:
                state = data.get("state") or data.get("presence") or ""
            if remote_jid:
                # Match the conversation so the frontend can filter broadcasts.
                pkey = _phone_key(remote_jid.split("@")[0])
                conv = _find_matching_conv(db, None, session, remote_jid, pkey)
                if conv:
                    asyncio.create_task(manager.broadcast(
                        session.workspace_id,
                        {"type": "presence", "conversation_id": conv.id, "state": state}
                    ))

        elif event in ("chats.set", "CHATS_SET", "chats.upsert", "CHATS_UPSERT"):
            # Bulk chat sync on initial history download. Evolution sends either
            # a list directly or wraps it in {chats: [...]}.
            items = data if isinstance(data, list) else (data.get("chats") or [])
            for ch in items:
                remote_jid = ch.get("remoteJid") or ch.get("id") or ""
                if not remote_jid or "@g.us" in remote_jid:
                    continue
                phone = remote_jid.split("@")[0]
                pkey = _phone_key(phone)
                if _find_matching_conv(db, None, session, remote_jid, pkey):
                    continue
                crm_contact = None
                for c in db.query(models.Contact).filter(
                    models.Contact.workspace_id == session.workspace_id
                ).all():
                    if _phone_key(c.phone or "") == pkey and pkey:
                        crm_contact = c; break
                display_name = (crm_contact.name if crm_contact else None) or phone
                last_ts = ch.get("updatedAt") or ch.get("lastMessageTimestamp") or ch.get("t")
                try:
                    if isinstance(last_ts, (int, float)):
                        last_ts = datetime.utcfromtimestamp(last_ts / 1000 if last_ts > 10**12 else last_ts)
                    elif isinstance(last_ts, str):
                        last_ts = datetime.fromisoformat(last_ts.replace("Z", ""))
                    else:
                        last_ts = None
                except Exception:
                    last_ts = None
                db.add(models.Conversation(
                    workspace_id=session.workspace_id,
                    session_id=session.id,
                    remote_jid=remote_jid,
                    contact_id=crm_contact.id if crm_contact else None,
                    contact_name=display_name,
                    contact_phone=phone,
                    assigned_to=session.user_id,
                    last_message_at=last_ts,
                ))
            db.commit()

        elif event in ("messages.set", "MESSAGES_SET"):
            # Historical batch. Each entry has key/message/messageTimestamp/etc.
            items = data.get("messages") if isinstance(data, dict) else data
            if not isinstance(items, list):
                items = []
            for m in items:
                key = m.get("key") or {}
                mid = key.get("id")
                remote_jid = key.get("remoteJid") or ""
                if not mid or not remote_jid:
                    continue
                phone = remote_jid.split("@")[0]
                pkey = _phone_key(phone)
                conv = _find_matching_conv(db, None, session, remote_jid, pkey)
                if not conv:
                    conv = models.Conversation(
                        workspace_id=session.workspace_id,
                        session_id=session.id,
                        remote_jid=remote_jid,
                        contact_name=phone,
                        contact_phone=phone,
                        assigned_to=session.user_id,
                    )
                    db.add(conv); db.flush()
                # Dedup scoped to this conversation so other workspaces' copies
                # of the same msg don't block our insert.
                if db.query(models.Message).filter(
                    models.Message.evolution_message_id == mid,
                    models.Message.conversation_id == conv.id,
                ).first():
                    continue
                from_me = bool(key.get("fromMe"))
                msg_content = m.get("message") or {}
                body_text, media_type = _extract_body(msg_content)
                ts = m.get("messageTimestamp")
                try:
                    ts = datetime.utcfromtimestamp(int(ts)) if ts else datetime.utcnow()
                except Exception:
                    ts = datetime.utcnow()
                push = m.get("pushName") or ""
                author_phone = _participant_phone(key, db, session.workspace_id)
                author_label = (
                    _resolve_author_label(db, session.workspace_id, author_phone, push)
                    if author_phone else push
                )
                db.add(models.Message(
                    conversation_id=conv.id,
                    direction="outbound" if from_me else "inbound",
                    body=body_text,
                    media_type=media_type,
                    from_me=from_me,
                    author_name=author_label,
                    author_phone=author_phone or None,
                    evolution_message_id=mid,
                    timestamp=ts,
                ))
                if body_text and (not conv.last_message_at or ts > conv.last_message_at):
                    conv.last_message = body_text
                    conv.last_message_at = ts
            db.commit()

        elif event in ("contacts.set", "CONTACTS_SET", "contacts.upsert", "CONTACTS_UPSERT"):
            # Upsert CRM contacts from WA's contact store.
            items = data if isinstance(data, list) else (data.get("contacts") or [])
            for c in items:
                jid = c.get("remoteJid") or c.get("id") or ""
                if not jid or "@g.us" in jid or "@s.whatsapp.net" not in jid:
                    continue
                phone = jid.split("@")[0]
                pkey = _phone_key(phone)
                exists = None
                for existing in db.query(models.Contact).filter(
                    models.Contact.workspace_id == session.workspace_id
                ).all():
                    if _phone_key(existing.phone or "") == pkey and pkey:
                        exists = existing; break
                if not exists:
                    db.add(models.Contact(
                        workspace_id=session.workspace_id,
                        owner_id=session.user_id,
                        name=c.get("pushName") or c.get("name") or phone,
                        phone=phone,
                        source="whatsapp",
                        source_session_id=session.id,
                    ))
            db.commit()

        return {"ok": True}
    finally:
        db.close()


# WebSocket ---------------------------------------------------------------
@router.websocket("/ws")
async def ws_chat(ws: WebSocket, token: str):
    try:
        payload = decode_token(token)
        ws_id = int(payload.get("ws") or 0)
        if not ws_id:
            await ws.close(code=4401)
            return
    except Exception:
        await ws.close(code=4401)
        return
    await manager.connect(ws_id, ws)
    try:
        while True:
            await ws.receive_text()  # ping/keepalive; we don't process
    except WebSocketDisconnect:
        manager.disconnect(ws_id, ws)
