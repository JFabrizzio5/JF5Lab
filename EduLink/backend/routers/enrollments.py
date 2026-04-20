from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    progress: int

    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    progress: int


@router.get("/my", response_model=List[dict])
def my_enrollments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("student"))
):
    enrollments = db.query(models.Enrollment).options(
        joinedload(models.Enrollment.course).joinedload(models.Course.tutor)
    ).filter(models.Enrollment.student_id == current_user.id).all()

    result = []
    for e in enrollments:
        c = e.course
        result.append({
            "id": e.id,
            "course_id": c.id,
            "title": c.title,
            "category": c.category,
            "thumbnail_url": c.thumbnail_url,
            "tutor_name": c.tutor.name if c.tutor else "",
            "progress": e.progress,
            "enrolled_at": str(e.enrolled_at)
        })
    return result


@router.post("/{course_id}")
def enroll(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("student"))
):
    course = db.query(models.Course).options(joinedload(models.Course.tutor)).filter(
        models.Course.id == course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    if course.school_restricted and course.tutor.school != current_user.school:
        raise HTTPException(status_code=403, detail="Este curso es solo para estudiantes de la misma escuela")

    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id,
        models.Enrollment.course_id == course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este curso")

    enrollment = models.Enrollment(student_id=current_user.id, course_id=course_id, progress=0)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return {"message": "Inscripción exitosa", "enrollment_id": enrollment.id}


@router.put("/{course_id}/progress")
def update_progress(
    course_id: int,
    data: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("student"))
):
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id,
        models.Enrollment.course_id == course_id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="No estás inscrito en este curso")

    enrollment.progress = max(0, min(100, data.progress))
    db.commit()
    return {"message": "Progreso actualizado", "progress": enrollment.progress}


@router.get("/check/{course_id}")
def check_enrollment(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == current_user.id,
        models.Enrollment.course_id == course_id
    ).first()
    return {"enrolled": enrollment is not None, "progress": enrollment.progress if enrollment else 0}
