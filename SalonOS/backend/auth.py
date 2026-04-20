from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
import models

SECRET_KEY = "salonos_secret_key_2024"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_token(user_id: int, role: str) -> str:
    return jwt.encode({"sub": str(user_id), "role": role}, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> models.User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Token inválido")
        user = db.query(models.User).filter(models.User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(401, "Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(401, "Token inválido")


def require_role(*roles):
    def dep(user: models.User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, "Sin permiso")
        return user
    return dep


def get_venue_for_user(user_id: int, db: Session) -> models.Venue:
    venue = db.query(models.Venue).filter(models.Venue.owner_id == user_id).first()
    if not venue:
        raise HTTPException(404, "Venue no encontrado")
    return venue
