from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/admin", tags=["admin"])


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = None
    school: Optional[str] = None


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("admin"))
):
    total_users = db.query(models.User).count()
    total_students = db.query(models.User).filter(models.User.role == "student").count()
    total_tutors = db.query(models.User).filter(models.User.role == "tutor").count()
    total_courses = db.query(models.Course).count()
    published_courses = db.query(models.Course).filter(models.Course.is_published == True).count()
    total_enrollments = db.query(models.Enrollment).count()
    total_bookings = db.query(models.Booking).count()

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_tutors": total_tutors,
        "total_courses": total_courses,
        "published_courses": published_courses,
        "total_enrollments": total_enrollments,
        "total_bookings": total_bookings
    }


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("admin"))
):
    users = db.query(models.User).all()
    return [{
        "id": u.id,
        "email": u.email,
        "name": u.name,
        "role": u.role,
        "school": u.school,
        "is_active": u.is_active,
        "avatar_url": u.avatar_url
    } for u in users]


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("admin"))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    return {"message": "Usuario actualizado"}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("admin"))
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado"}


@router.get("/courses")
def list_all_courses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("admin"))
):
    courses = db.query(models.Course).all()
    return [{
        "id": c.id,
        "title": c.title,
        "category": c.category,
        "tutor_id": c.tutor_id,
        "price": c.price,
        "school_restricted": c.school_restricted,
        "is_published": c.is_published
    } for c in courses]


@router.put("/courses/{course_id}/toggle")
def toggle_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("admin"))
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    course.is_published = not course.is_published
    db.commit()
    return {"message": "Estado del curso actualizado", "is_published": course.is_published}
