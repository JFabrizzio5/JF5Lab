from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
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
    role: str = "attendee"


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    role: str
    avatar_url: str | None = None
    phone: str | None = None

    class Config:
        from_attributes = True


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    if data.role not in ("attendee", "organizer"):
        data.role = "attendee"
    user = models.User(
        email=data.email,
        name=data.name,
        password_hash=auth_utils.hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth_utils.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": UserOut.from_orm(user)}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth_utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    if not user.is_active:
        raise HTTPException(403, "Account disabled")
    token = auth_utils.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": UserOut.from_orm(user)}


@router.get("/me")
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return UserOut.from_orm(current_user)


@router.put("/me")
def update_me(
    data: dict,
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    for field in ("name", "phone", "avatar_url"):
        if field in data:
            setattr(current_user, field, data[field])
    if "password" in data and data["password"]:
        current_user.password_hash = auth_utils.hash_password(data["password"])
    db.commit()
    db.refresh(current_user)
    return UserOut.from_orm(current_user)
