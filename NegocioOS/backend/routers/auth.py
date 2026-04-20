from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
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
    business_name: str = ""


def user_out(user: models.User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "business_name": user.business_name or "",
        "avatar_url": user.avatar_url or "",
    }


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=req.email, is_active=True).first()
    if not user or not auth_utils.verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    token = auth_utils.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user": user_out(user)}


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=req.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    user = models.User(
        email=req.email,
        name=req.name,
        password_hash=auth_utils.hash_password(req.password),
        role=models.UserRole.owner,
        business_name=req.business_name,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth_utils.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user": user_out(user)}


@router.get("/me")
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return user_out(current_user)
