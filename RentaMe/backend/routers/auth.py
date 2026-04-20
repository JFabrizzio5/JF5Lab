from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str = "customer"
    slug: str = None
    business_name: str = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str
    name: str


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    if data.role not in ("customer", "vendor"):
        data.role = "customer"

    user = models.User(
        email=data.email,
        name=data.name,
        password_hash=auth_utils.hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if data.role == "vendor":
        slug = data.slug or data.email.split("@")[0].replace(".", "-").lower()
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while db.query(models.VendorProfile).filter(models.VendorProfile.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        vendor = models.VendorProfile(
            user_id=user.id,
            slug=slug,
            business_name=data.business_name or data.name,
        )
        db.add(vendor)
        db.commit()

    token = auth_utils.create_access_token(user.id, user.role)
    return TokenResponse(access_token=token, user_id=user.id, role=user.role, name=user.name)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not auth_utils.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")
    token = auth_utils.create_access_token(user.id, user.role)
    return TokenResponse(access_token=token, user_id=user.id, role=user.role, name=user.name)


@router.get("/me")
def get_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "avatar_url": current_user.avatar_url,
        "phone": current_user.phone,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat(),
    }
