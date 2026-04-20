from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str = "client"
    phone: str = None


def user_out(u: models.User):
    return {
        "id": u.id,
        "email": u.email,
        "name": u.name,
        "role": u.role,
        "avatar_url": u.avatar_url,
        "phone": u.phone,
        "is_active": u.is_active,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not auth_utils.verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Credenciales incorrectas")
    if not user.is_active:
        raise HTTPException(401, "Usuario inactivo")
    token = auth_utils.create_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer", "user": user_out(user)}


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email ya registrado")
    user = models.User(
        email=data.email,
        name=data.name,
        password_hash=auth_utils.hash_password(data.password),
        role=data.role,
        phone=data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth_utils.create_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer", "user": user_out(user)}


@router.get("/me")
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return user_out(current_user)
