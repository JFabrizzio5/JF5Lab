from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/lessons", tags=["lessons"])


class LessonCreate(BaseModel):
    title: str
    video_url: Optional[str] = None
    description: Optional[str] = None
    order: int = 1
    duration_mins: int = 0


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    video_url: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    duration_mins: Optional[int] = None


class LessonOut(BaseModel):
    id: int
    course_id: int
    title: str
    video_url: Optional[str] = None
    description: Optional[str] = None
    order: int
    duration_mins: int

    class Config:
        from_attributes = True


@router.get("/course/{course_id}", response_model=List[LessonOut])
def list_lessons(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth_utils.get_current_user)
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    lessons = db.query(models.Lesson).filter(
        models.Lesson.course_id == course_id
    ).order_by(models.Lesson.order).all()
    return lessons


@router.post("/course/{course_id}", response_model=LessonOut)
def create_lesson(
    course_id: int,
    data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor", "admin"))
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    if current_user.role != "admin" and course.tutor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sin permisos")

    lesson = models.Lesson(
        course_id=course_id,
        title=data.title,
        video_url=data.video_url,
        description=data.description,
        order=data.order,
        duration_mins=data.duration_mins
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.put("/{lesson_id}", response_model=LessonOut)
def update_lesson(
    lesson_id: int,
    data: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor", "admin"))
):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")

    course = db.query(models.Course).filter(models.Course.id == lesson.course_id).first()
    if current_user.role != "admin" and course.tutor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sin permisos")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lesson, field, value)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor", "admin"))
):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")

    course = db.query(models.Course).filter(models.Course.id == lesson.course_id).first()
    if current_user.role != "admin" and course.tutor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sin permisos")

    db.delete(lesson)
    db.commit()
    return {"message": "Lección eliminada"}
