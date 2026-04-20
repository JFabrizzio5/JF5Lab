from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import get_db
from models import Editor, Subscription
from schemas import EditorCreate, EditorOut, EditorUpdate
from auth import hash_password, get_current_editor, get_admin_editor

router = APIRouter(prefix="/editors", tags=["Editors"])


async def _get_editor_full(db: AsyncSession, editor_id: int) -> Editor:
    result = await db.execute(
        select(Editor)
        .options(selectinload(Editor.subscription).selectinload(Subscription.plan))
        .where(Editor.id == editor_id)
    )
    return result.scalar_one_or_none()


@router.post("/", response_model=EditorOut, status_code=201)
async def create_editor(
    payload: EditorCreate,
    db: AsyncSession = Depends(get_db),
    _: Editor = Depends(get_admin_editor)
):
    result = await db.execute(select(Editor).where(Editor.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    editor = Editor(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role
    )
    db.add(editor)
    await db.commit()
    return await _get_editor_full(db, editor.id)


@router.get("/", response_model=List[EditorOut])
async def list_editors(
    db: AsyncSession = Depends(get_db),
    _: Editor = Depends(get_current_editor)
):
    result = await db.execute(
        select(Editor)
        .options(selectinload(Editor.subscription).selectinload(Subscription.plan))
        .order_by(Editor.created_at.desc())
    )
    return result.scalars().all()


@router.get("/me", response_model=EditorOut)
async def get_me(current: Editor = Depends(get_current_editor)):
    return current


@router.get("/{editor_id}", response_model=EditorOut)
async def get_editor(
    editor_id: int,
    db: AsyncSession = Depends(get_db),
    _: Editor = Depends(get_current_editor)
):
    editor = await _get_editor_full(db, editor_id)
    if not editor:
        raise HTTPException(status_code=404, detail="Editor not found")
    return editor


@router.patch("/{editor_id}", response_model=EditorOut)
async def update_editor(
    editor_id: int,
    payload: EditorUpdate,
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    if current.role != "admin" and current.id != editor_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    editor = await _get_editor_full(db, editor_id)
    if not editor:
        raise HTTPException(status_code=404, detail="Editor not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(editor, field, value)

    await db.commit()
    return await _get_editor_full(db, editor_id)


@router.delete("/{editor_id}", status_code=204)
async def delete_editor(
    editor_id: int,
    db: AsyncSession = Depends(get_db),
    _: Editor = Depends(get_admin_editor)
):
    result = await db.execute(select(Editor).where(Editor.id == editor_id))
    editor = result.scalar_one_or_none()
    if not editor:
        raise HTTPException(status_code=404, detail="Editor not found")
    await db.delete(editor)
    await db.commit()
