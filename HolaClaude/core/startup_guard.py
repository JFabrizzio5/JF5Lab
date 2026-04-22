import os
import sys
import logging
from core.pin_constant import PIN_HASH_HARDCODED

logger = logging.getLogger("startup_guard")


def verify_pin_integrity():
    env_hash = os.getenv("HOLACLAUDE_PIN_HASH", "").strip()
    if not env_hash:
        os.environ["HOLACLAUDE_PIN_HASH"] = PIN_HASH_HARDCODED
        return
    if env_hash != PIN_HASH_HARDCODED:
        logger.error("PIN_HASH env no coincide con hash compilado. Abortando.")
        sys.exit(1)


def verify_artifacts_sandbox():
    artifacts = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts"))
    if not os.path.isdir(artifacts):
        os.makedirs(artifacts, exist_ok=True)
    os.environ["HOLACLAUDE_ARTIFACTS_PATH"] = artifacts


def run_all():
    verify_pin_integrity()
    verify_artifacts_sandbox()
    logger.info("startup_guard ok")
