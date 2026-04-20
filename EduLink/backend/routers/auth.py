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
    role: str = "student"
    school: str = "OTHER"


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    school: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    user: UserOut


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not auth_utils.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta desactivada")

    token = auth_utils.create_access_token({"sub": str(user.id)})
    return LoginResponse(
        access_token=token,
        user=UserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            school=user.school,
            avatar_url=user.avatar_url
        )
    )


@router.post("/register", response_model=LoginResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    if data.role not in ["student", "tutor"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    school_opts = ["UAM", "UNAM", "POLI", "IPN", "ITESM", "OTHER"]
    if data.school not in school_opts:
        raise HTTPException(status_code=400, detail="Escuela inválida")

    avatar = f"https://ui-avatars.com/api/?name={data.name.replace(' ', '+')}&background=f59e0b&color=fff"
    user = models.User(
        email=data.email,
        name=data.name,
        password_hash=auth_utils.get_password_hash(data.password),
        role=data.role,
        school=data.school,
        avatar_url=avatar,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = auth_utils.create_access_token({"sub": str(user.id)})
    return LoginResponse(
        access_token=token,
        user=UserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            school=user.school,
            avatar_url=user.avatar_url
        )
    )


@router.get("/me", response_model=UserOut)
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return current_user
