import os
import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("UPIPLANET_JWT_SECRET", "upi-planet-dev-secret")
JWT_ALGO = "HS256"
JWT_TTL_HOURS = 24


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=10)).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def issue_token(user_id: str) -> str:
    payload = {
        "sub": str(user_id),
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + timedelta(hours=JWT_TTL_HOURS)).timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_token(token: str) -> str | None:
    try:
        p = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return p.get("sub")
    except jwt.PyJWTError:
        return None
