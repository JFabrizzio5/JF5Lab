import os
import re
import subprocess
import logging

logger = logging.getLogger("cometax_bridge")

ARTIFACTS = os.environ.get("HOLACLAUDE_ARTIFACTS_PATH", "/app/artifacts")
LAUNCHER = "/framework/TemplateMicroservices/launcher.py"
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]{2,39}$")


def spawn_service(name: str, description: str, framework: str = "1", db: str = "1") -> dict:
    if not NAME_RE.match(name):
        return {"ok": False, "error": "nombre invalido (PascalCase 3-40 chars)"}
    if framework not in ("1", "2") or db not in ("1", "2", "3", "4", "5"):
        return {"ok": False, "error": "opcion invalida"}
    if os.path.exists(os.path.join(ARTIFACTS, name)):
        return {"ok": False, "error": f"{name} ya existe"}
    if not os.path.exists(LAUNCHER):
        return {"ok": False, "error": "launcher no montado"}

    stdin = f"{name}\n{description}\n{framework}\n{db}\n2\n"
    try:
        p = subprocess.run(
            ["python3", LAUNCHER],
            input=stdin,
            cwd=ARTIFACTS,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "ok": p.returncode == 0,
            "stdout": p.stdout[-4000:],
            "stderr": p.stderr[-2000:],
            "path": os.path.join(ARTIFACTS, name) if p.returncode == 0 else None,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    except Exception as e:
        logger.error(f"spawn_service error: {e}")
        return {"ok": False, "error": str(e)}
