"""Evolution API client — wraps the REST calls we use for multi-session WhatsApp.

Each agent in HubOS can create their OWN instance (`instance_name`) tied to their
own WhatsApp number. All API calls are namespaced by `instance_name`, so sessions
are fully separated on the Evolution side.
"""
import os
import httpx

EVOLUTION_URL = os.environ.get("EVOLUTION_API_URL", "http://evolution_api:8080").rstrip("/")
EVOLUTION_KEY = os.environ.get("EVOLUTION_API_KEY", "change_me")
WEBHOOK_BASE = os.environ.get("EVOLUTION_WEBHOOK_BASE", "http://hubos_backend:8070").rstrip("/")


def _headers() -> dict:
    return {"apikey": EVOLUTION_KEY, "Content-Type": "application/json"}


async def create_instance(instance_name: str, webhook_token: str) -> dict:
    """Create a new Evolution instance and register our webhook.

    Payload follows Evolution API v2 shape: webhook is a nested object with
    `enabled`/`url`/`events`/`byEvents`/`base64`, and `integration` selects the
    Baileys v7 backend (which exposes LID↔PN mapping — the whole reason we're
    on v2)."""
    url = f"{EVOLUTION_URL}/instance/create"
    webhook_url = f"{WEBHOOK_BASE}/api/chat/webhook/{webhook_token}"
    payload = {
        "instanceName": instance_name,
        "qrcode": True,
        "integration": "WHATSAPP-BAILEYS",
        # Pull historic chats/messages from the phone, like WhatsApp Web.
        "syncFullHistory": True,
        "alwaysOnline": False,
        "readMessages": False,
        "readStatus": False,
        "groupsIgnore": True,
        "webhook": {
            "enabled": True,
            "url": webhook_url,
            "byEvents": False,
            "base64": True,
            "events": [
                "MESSAGES_UPSERT",
                "MESSAGES_SET",
                "CHATS_SET",
                "CHATS_UPSERT",
                "CONTACTS_SET",
                "CONTACTS_UPSERT",
                "PRESENCE_UPDATE",
                "CONNECTION_UPDATE",
                "QRCODE_UPDATED",
            ],
        },
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload, headers=_headers())
        if r.status_code >= 400:
            raise RuntimeError(f"Evolution create_instance {r.status_code}: {r.text[:300]}")
        return r.json()


async def connect_instance(instance_name: str) -> dict:
    """Fetch QR / pairing code for connection."""
    url = f"{EVOLUTION_URL}/instance/connect/{instance_name}"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, headers=_headers())
        r.raise_for_status()
        return r.json()


async def fetch_status(instance_name: str) -> dict:
    url = f"{EVOLUTION_URL}/instance/connectionState/{instance_name}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers())
        r.raise_for_status()
        return r.json()


async def logout_instance(instance_name: str) -> dict:
    url = f"{EVOLUTION_URL}/instance/logout/{instance_name}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.delete(url, headers=_headers())
        if r.status_code >= 400:
            return {"error": r.text}
        return r.json()


async def delete_instance(instance_name: str) -> dict:
    url = f"{EVOLUTION_URL}/instance/delete/{instance_name}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.delete(url, headers=_headers())
        if r.status_code >= 400:
            return {"error": r.text}
        return r.json()


async def check_number_exists(instance_name: str, number: str) -> tuple[bool, str]:
    """Returns (exists, resolved_jid). v1.8 endpoint."""
    url = f"{EVOLUTION_URL}/chat/whatsappNumbers/{instance_name}"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json={"numbers": [number]}, headers=_headers())
        if r.status_code >= 400:
            return False, ""
        data = r.json()
        if isinstance(data, list) and data:
            d = data[0]
            return bool(d.get("exists")), d.get("jid") or ""
        return False, ""


def _mx_variants(num: str) -> list[str]:
    """Mexican WhatsApp is fiddly: numbers registered before 2020 use '52' (no 1
    after), newer use '521'. Try both."""
    n = num.lstrip("+").strip()
    out = [n]
    if n.startswith("521") and len(n) == 13:
        out.append("52" + n[3:])   # strip the 1
    elif n.startswith("52") and len(n) == 12:
        out.append("521" + n[2:])  # add the 1
    # dedupe preserving order
    seen, res = set(), []
    for v in out:
        if v not in seen:
            seen.add(v); res.append(v)
    return res


async def resolve_number(instance_name: str, number: str) -> str | None:
    """Find a valid WhatsApp-registered variant of `number` (tries MX shapes).
    Returns the variant that `exists:true` or None if none match."""
    for v in _mx_variants(number):
        ok, _jid = await check_number_exists(instance_name, v)
        if ok:
            return v
    return None


async def send_text(instance_name: str, number: str, text: str) -> dict:
    """v2 payload is flat: `{number, text, delay}`. `number` can be a plain
    digits phone or a full JID (`<digits>@lid` / `<digits>@s.whatsapp.net`).
    Evolution v2 + Baileys v7 resolves the LID internally."""
    url = f"{EVOLUTION_URL}/message/sendText/{instance_name}"
    payload = {
        "number": number,
        "text": text,
        "delay": 500,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload, headers=_headers())
        if r.status_code >= 400:
            try:
                err = r.json()
            except Exception:
                err = {"raw": r.text[:300]}
            msg = err.get("message") or err.get("response", {}).get("message") or err
            if isinstance(msg, list) and msg and isinstance(msg[0], dict) and msg[0].get("exists") is False:
                raise RuntimeError(
                    f"exists:false for {msg[0].get('number', number)}"
                )
            raise RuntimeError(f"Evolution {r.status_code}: {msg}")
        return r.json()


async def send_media(instance_name: str, number: str, media_url: str, caption: str = "", media_type: str = "image") -> dict:
    """v2 flat payload — `mediatype` + `media` + `caption` at the top level."""
    url = f"{EVOLUTION_URL}/message/sendMedia/{instance_name}"
    payload = {
        "number": number,
        "mediatype": media_type,
        "media": media_url,
        "caption": caption,
        "delay": 500,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload, headers=_headers())
        if r.status_code >= 400:
            raise RuntimeError(f"Evolution sendMedia {r.status_code}: {r.text[:300]}")
        return r.json()


async def fetch_chats(instance_name: str) -> list:
    """v1.8 supports both GET and POST for findChats. Try POST first (accepts
    filters), fall back to GET if the server version only wires up one."""
    url = f"{EVOLUTION_URL}/chat/findChats/{instance_name}"
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(url, json={}, headers=_headers())
            if r.status_code < 400:
                data = r.json()
                if isinstance(data, list) and data:
                    return data
        except Exception:
            pass
        try:
            r = await client.get(url, headers=_headers())
            if r.status_code < 400:
                data = r.json()
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []


async def fetch_contacts(instance_name: str) -> list:
    url = f"{EVOLUTION_URL}/chat/findContacts/{instance_name}"
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(url, json={"where": {}}, headers=_headers())
            if r.status_code < 400:
                data = r.json()
                if isinstance(data, list) and data:
                    return data
        except Exception:
            pass
        try:
            r = await client.get(url, headers=_headers())
            if r.status_code < 400:
                data = r.json()
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []


async def resolve_lid_to_pn(instance_name: str, lid: str) -> str | None:
    """Given a `<digits>@lid` identifier, try to find the real phone number.

    Baileys (via STORE_CONTACTS=true) keeps a contact table with both the
    LID and the PN. We scan findContacts looking for an entry whose id/jid
    matches the LID and return the canonical phone from a companion field.
    """
    lid_digits = lid.split("@")[0] if "@" in lid else lid
    if not lid_digits:
        return None
    contacts = await fetch_contacts(instance_name)
    for c in contacts or []:
        cid = c.get("id") or c.get("remoteJid") or ""
        if cid.split("@")[0] == lid_digits:
            # Evolution/Baileys contact entries sometimes have "pn" / "phoneNumber" / "senderPn"
            for k in ("pn", "phoneNumber", "senderPn", "verifiedPhoneNumber"):
                v = c.get(k)
                if v:
                    digits = "".join(ch for ch in str(v) if ch.isdigit())
                    if digits:
                        return digits
    return None


async def fetch_messages(instance_name: str, remote_jid: str, limit: int = 50) -> list:
    """v2 wraps the result in `{messages: {records: [...], total, pages, ...}}`.
    v1.8 returned the array directly. Unwrap either shape so callers always
    get a flat list of message objects."""
    url = f"{EVOLUTION_URL}/chat/findMessages/{instance_name}"
    payload = {"where": {"key": {"remoteJid": remote_jid}}, "limit": limit}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload, headers=_headers())
        if r.status_code >= 400:
            return []
        data = r.json()
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            inner = data.get("messages")
            if isinstance(inner, list):
                return inner
            if isinstance(inner, dict):
                return inner.get("records") or []
        return []


async def fetch_media_base64(instance_name: str, evolution_message_id: str) -> dict:
    """Decrypt + return the media attached to a WhatsApp message.
    Evolution v2 returns `{mediaType, fileName, mimetype, base64, buffer}`."""
    url = f"{EVOLUTION_URL}/chat/getBase64FromMediaMessage/{instance_name}"
    payload = {"message": {"key": {"id": evolution_message_id}}, "convertToMp4": False}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload, headers=_headers())
        if r.status_code >= 400:
            raise RuntimeError(f"Evolution media {r.status_code}: {r.text[:300]}")
        return r.json()


async def send_presence(instance_name: str, number: str, presence: str = "composing", delay_ms: int = 1200) -> dict:
    """Broadcast a presence update (composing / recording / paused) to the
    recipient. Used by the typing indicator while the agent is drafting."""
    url = f"{EVOLUTION_URL}/chat/sendPresence/{instance_name}"
    payload = {"number": number, "presence": presence, "delay": delay_ms}
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.post(url, json=payload, headers=_headers())
            return r.json() if r.status_code < 400 else {}
        except Exception:
            return {}


async def restart_instance(instance_name: str) -> dict:
    """Force Baileys to rewire its socket. Useful to re-trigger a history sync."""
    url = f"{EVOLUTION_URL}/instance/restart/{instance_name}"
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            r = await client.put(url, headers=_headers())
            if r.status_code < 400:
                return r.json()
        except Exception:
            pass
    return {}
