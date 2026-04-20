from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewCreate(BaseModel):
    course_id: Optional[int] = None
    booking_id: Optional[int] = None
    rating: int
    comment: Optional[str] = None


class ReviewOut(BaseModel):
    id: int
    course_id: Optional[int] = None
    booking_id: Optional[int] = None
    reviewer_id: int
    reviewer_name: str
    rating: int
    comment: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/course/{course_id}", response_model=List[ReviewOut])
def course_reviews(course_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.course_id == course_id).all()
    result = []
    for r in reviews:
        result.append(ReviewOut(
            id=r.id,
            course_id=r.course_id,
            booking_id=r.booking_id,
            reviewer_id=r.reviewer_id,
            reviewer_name=r.reviewer.name if r.reviewer else "Anónimo",
            rating=r.rating,
            comment=r.comment
        ))
    return result


@router.post("/", response_model=ReviewOut)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    if not data.course_id and not data.booking_id:
        raise HTTPException(status_code=400, detail="Debe especificar course_id o booking_id")

    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating debe ser entre 1 y 5")

    if data.course_id:
        existing = db.query(models.Review).filter(
            models.Review.course_id == data.course_id,
            models.Review.reviewer_id == current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Ya has reseñado este curso")

    review = models.Review(
        course_id=data.course_id,
        booking_id=data.booking_id,
        reviewer_id=current_user.id,
        rating=data.rating,
        comment=data.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return ReviewOut(
        id=review.id,
        course_id=review.course_id,
        booking_id=review.booking_id,
        reviewer_id=review.reviewer_id,
        reviewer_name=current_user.name,
        rating=review.rating,
        comment=review.comment
    )
