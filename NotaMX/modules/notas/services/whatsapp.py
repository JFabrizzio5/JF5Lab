"""WhatsApp Cloud API (Meta) wrapper, con fallback a log si no hay token."""
from __future__ import annotations
import os
import logging
import httpx

logger = logging.getLogger("notamx.whatsapp")


async def send_text(to_phone: str, body: str) -> tuple[bool, str]:
    """Devuelve (ok, status_msg). Fallback a logger si no hay token."""
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    if not token or not phone_id:
        logger.info(f"[WA-MOCK] -> {to_phone}: {body[:120]}")
        return False, "no-token (logged only)"
    url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone.lstrip("+"),
        "type": "text",
        "text": {"body": body[:4096]},
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(url, headers=headers, json=payload)
            if r.status_code >= 300:
                return False, f"http {r.status_code}: {r.text[:200]}"
            data = r.json()
            mid = data.get("messages", [{}])[0].get("id", "")
            return True, f"sent ({mid})"
    except Exception as e:
        return False, f"error: {e}"
