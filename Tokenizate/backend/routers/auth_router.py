from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import get_db
from models import Editor, Subscription
from schemas import Token, LoginRequest
from auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Editor)
        .options(selectinload(Editor.subscription).selectinload(Subscription.plan))
        .where(Editor.email == payload.email)
    )
    editor = result.scalar_one_or_none()
    if not editor or not verify_password(payload.password, editor.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not editor.is_active:
        raise HTTPException(status_code=403, detail="Account inactive")

    token = create_access_token({"sub": str(editor.id)})
    return {"access_token": token, "token_type": "bearer", "editor": editor}
