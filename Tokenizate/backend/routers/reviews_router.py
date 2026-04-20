from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import get_db
from models import Editor, ReviewProcess, ReviewComment, ReviewHistory, ReviewStatus, Subscription
from schemas import (
    ReviewCreate, ReviewUpdate, ReviewStatusUpdate,
    ReviewCommentCreate, ReviewOut, ReviewListOut, ReviewCommentOut, ReviewHistoryOut
)
from auth import get_current_editor

router = APIRouter(prefix="/reviews", tags=["Reviews"])


async def _get_review_full(db: AsyncSession, review_id: int) -> ReviewProcess:
    result = await db.execute(
        select(ReviewProcess)
        .options(
            selectinload(ReviewProcess.assigned_editor).selectinload(Editor.subscription).selectinload(Subscription.plan),
            selectinload(ReviewProcess.created_by_editor).selectinload(Editor.subscription).selectinload(Subscription.plan),
            selectinload(ReviewProcess.comments).selectinload(ReviewComment.editor),
            selectinload(ReviewProcess.history).selectinload(ReviewHistory.changed_by_editor),
        )
        .where(ReviewProcess.id == review_id)
    )
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/", response_model=ReviewOut, status_code=201)
async def create_review(
    payload: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    review = ReviewProcess(
        title=payload.title,
        description=payload.description,
        content_url=payload.content_url,
        priority=payload.priority,
        assigned_editor_id=payload.assigned_editor_id,
        created_by_id=current.id,
        deadline=payload.deadline,
        status=ReviewStatus.draft
    )
    db.add(review)
    await db.flush()

    db.add(ReviewHistory(
        review_id=review.id,
        old_status=None,
        new_status=ReviewStatus.draft,
        changed_by_id=current.id,
        note="Review created"
    ))
    await db.commit()
    return await _get_review_full(db, review.id)


@router.get("/", response_model=List[ReviewListOut])
async def list_reviews(
    status: Optional[ReviewStatus] = Query(None),
    assigned_to_me: bool = Query(False),
    priority: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    query = (
        select(ReviewProcess)
        .options(
            selectinload(ReviewProcess.assigned_editor)
        )
        .order_by(ReviewProcess.created_at.desc())
    )
    if status:
        query = query.where(ReviewProcess.status == status)
    if assigned_to_me:
        query = query.where(ReviewProcess.assigned_editor_id == current.id)
    if priority:
        query = query.where(ReviewProcess.priority == priority)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/stats", tags=["Stats"])
async def get_stats(
    db: AsyncSession = Depends(get_db),
    _: Editor = Depends(get_current_editor)
):
    from sqlalchemy import func
    result = await db.execute(
        select(ReviewProcess.status, func.count(ReviewProcess.id))
        .group_by(ReviewProcess.status)
    )
    rows = result.all()
    stats = {r[0]: r[1] for r in rows}
    total = sum(stats.values())
    return {
        "total": total,
        "by_status": stats,
        "draft": stats.get("draft", 0),
        "in_review": stats.get("in_review", 0),
        "revision_required": stats.get("revision_required", 0),
        "approved": stats.get("approved", 0),
        "rejected": stats.get("rejected", 0),
    }


@router.get("/{review_id}", response_model=ReviewOut)
async def get_review(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    _: Editor = Depends(get_current_editor)
):
    return await _get_review_full(db, review_id)


@router.patch("/{review_id}", response_model=ReviewOut)
async def update_review(
    review_id: int,
    payload: ReviewUpdate,
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    result = await db.execute(select(ReviewProcess).where(ReviewProcess.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current.role not in ("admin", "senior_editor") and review.created_by_id != current.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    await db.commit()
    return await _get_review_full(db, review_id)


@router.post("/{review_id}/status", response_model=ReviewOut)
async def change_status(
    review_id: int,
    payload: ReviewStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    result = await db.execute(select(ReviewProcess).where(ReviewProcess.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    old_status = review.status
    review.status = payload.status
    db.add(ReviewHistory(
        review_id=review.id,
        old_status=old_status,
        new_status=payload.status,
        changed_by_id=current.id,
        note=payload.note
    ))
    await db.commit()
    return await _get_review_full(db, review_id)


@router.post("/{review_id}/comments", response_model=ReviewCommentOut, status_code=201)
async def add_comment(
    review_id: int,
    payload: ReviewCommentCreate,
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    result = await db.execute(select(ReviewProcess).where(ReviewProcess.id == review_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Review not found")

    comment = ReviewComment(review_id=review_id, editor_id=current.id, comment=payload.comment)
    db.add(comment)
    await db.commit()

    result2 = await db.execute(
        select(ReviewComment)
        .options(selectinload(ReviewComment.editor))
        .where(ReviewComment.id == comment.id)
    )
    return result2.scalar_one()


@router.get("/{review_id}/history", response_model=List[ReviewHistoryOut])
async def get_history(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    _: Editor = Depends(get_current_editor)
):
    result = await db.execute(
        select(ReviewHistory)
        .options(selectinload(ReviewHistory.changed_by_editor))
        .where(ReviewHistory.review_id == review_id)
        .order_by(ReviewHistory.changed_at.asc())
    )
    return result.scalars().all()


@router.delete("/{review_id}", status_code=204)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    result = await db.execute(select(ReviewProcess).where(ReviewProcess.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current.role != "admin" and review.created_by_id != current.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.delete(review)
    await db.commit()
