from fastapi import APIRouter, Depends, HTTPException
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
    role: str = "client"
    phone: str = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not auth_utils.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = auth_utils.create_token({"sub": str(user.id), "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "avatar_url": user.avatar_url,
            "phone": user.phone,
        }
    }


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    if data.role not in ["client", "freelancer"]:
        data.role = "client"

    avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={data.email}"
    user = models.User(
        email=data.email,
        name=data.name,
        password_hash=auth_utils.hash_password(data.password),
        role=data.role,
        avatar_url=avatar,
        phone=data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if data.role == "freelancer":
        profile = models.ProfessionalProfile(user_id=user.id)
        db.add(profile)
        sub = models.Subscription(user_id=user.id, plan="free", price_monthly=0.0)
        db.add(sub)
        db.commit()

    token = auth_utils.create_token({"sub": str(user.id), "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "avatar_url": user.avatar_url,
            "phone": user.phone,
        }
    }


@router.get("/me")
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "avatar_url": current_user.avatar_url,
        "phone": current_user.phone,
        "is_active": current_user.is_active,
    }
