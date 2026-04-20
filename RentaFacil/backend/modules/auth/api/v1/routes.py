from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from config.database import get_db
from modules.auth.services.auth_service import AuthService
from core.dependencies import get_current_user

router = APIRouter(prefix="/auth/v1", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).register(body.email, body.password, body.name, body.phone)

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login(form.username, form.password)

@router.post("/login/json")
async def login_json(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login(body.email, body.password)

@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name, "phone": current_user.phone}
