import os
import httpx
import logging

logger = logging.getLogger("claude_bridge")

CLAUDE_RUNNER_URL = os.getenv("CLAUDE_RUNNER_URL", "http://claude_runner:7788")
CLAUDE_TIMEOUT = 180.0


async def send_to_claude(message: str, session_id: str) -> dict:
    """Proxy mensaje a container claude_runner. Runner spawneara `claude -p` con cwd=/workspace."""
    payload = {"message": message[:8000], "session_id": session_id}
    async with httpx.AsyncClient(timeout=CLAUDE_TIMEOUT) as c:
        try:
            r = await c.post(f"{CLAUDE_RUNNER_URL}/run", json=payload)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            logger.error(f"claude runner error: {e}")
            return {"ok": False, "error": str(e)}
