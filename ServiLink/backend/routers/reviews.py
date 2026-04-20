from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewCreate(BaseModel):
    booking_id: int
    rating: int
    comment: str = None


@router.post("/")
def create_review(
    data: ReviewCreate,
    current_user: models.User = Depends(auth_utils.require_role("client")),
    db: Session = Depends(get_db)
):
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating debe ser entre 1 y 5")

    booking = db.query(models.Booking).filter(
        models.Booking.id == data.booking_id,
        models.Booking.client_id == current_user.id,
        models.Booking.status == "completed"
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Reserva no encontrada o no completada")

    if booking.review:
        raise HTTPException(status_code=400, detail="Ya existe una reseña para esta reserva")

    review = models.Review(
        booking_id=data.booking_id,
        client_id=current_user.id,
        professional_id=booking.professional_id,
        rating=data.rating,
        comment=data.comment,
    )
    db.add(review)
    db.commit()

    prof = db.query(models.ProfessionalProfile).filter(
        models.ProfessionalProfile.user_id == booking.professional_id
    ).first()
    if prof:
        all_reviews = db.query(models.Review).filter(
            models.Review.professional_id == booking.professional_id
        ).all()
        prof.rating_avg = sum(r.rating for r in all_reviews) / len(all_reviews)
        prof.total_reviews = len(all_reviews)
        db.commit()

    db.refresh(review)
    return {
        "id": review.id,
        "booking_id": review.booking_id,
        "rating": review.rating,
        "comment": review.comment,
        "client_name": current_user.name,
        "created_at": review.created_at.isoformat(),
    }


@router.get("/professional/{user_id}")
def get_professional_reviews(user_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).options(
        joinedload(models.Review.client)
    ).filter(models.Review.professional_id == user_id).order_by(models.Review.created_at.desc()).all()

    return [
        {
            "id": r.id,
            "rating": r.rating,
            "comment": r.comment,
            "client_name": r.client.name if r.client else "Anónimo",
            "client_avatar": r.client.avatar_url if r.client else None,
            "created_at": r.created_at.isoformat(),
        }
        for r in reviews
    ]
