from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from modules.auth.repositories.auth_repository import AuthRepository
from core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)

    async def register(self, email: str, password: str, name: str, phone: str | None = None):
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = hash_password(password)
        user = await self.repo.create(email, hashed, name, phone)
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}}

    async def login(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}}
