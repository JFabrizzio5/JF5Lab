from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    thumbnail_url: Optional[str] = None
    price: float = 0.0
    school_restricted: bool = False


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    price: Optional[float] = None
    school_restricted: Optional[bool] = None
    is_published: Optional[bool] = None


class TutorOut(BaseModel):
    id: int
    name: str
    school: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class CourseOut(BaseModel):
    id: int
    tutor_id: int
    title: str
    description: Optional[str] = None
    category: str
    thumbnail_url: Optional[str] = None
    price: float
    school_restricted: bool
    is_published: bool
    tutor: Optional[TutorOut] = None
    avg_rating: Optional[float] = None
    review_count: int = 0
    lesson_count: int = 0

    class Config:
        from_attributes = True


def enrich_course(course: models.Course, db: Session) -> dict:
    reviews = db.query(models.Review).filter(models.Review.course_id == course.id).all()
    avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else None
    lesson_count = db.query(models.Lesson).filter(models.Lesson.course_id == course.id).count()
    return {
        "id": course.id,
        "tutor_id": course.tutor_id,
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "thumbnail_url": course.thumbnail_url,
        "price": course.price,
        "school_restricted": course.school_restricted,
        "is_published": course.is_published,
        "tutor": course.tutor,
        "avg_rating": avg_rating,
        "review_count": len(reviews),
        "lesson_count": lesson_count
    }


@router.get("/", response_model=List[CourseOut])
def list_courses(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth_utils.get_current_user)
):
    q = db.query(models.Course).options(joinedload(models.Course.tutor)).filter(models.Course.is_published == True)

    if category:
        q = q.filter(models.Course.category == category)
    if search:
        q = q.filter(models.Course.title.ilike(f"%{search}%"))

    courses = q.all()
    result = []
    for c in courses:
        if c.school_restricted and current_user and current_user.school != c.tutor.school:
            continue
        result.append(enrich_course(c, db))
    return result


@router.get("/my", response_model=List[CourseOut])
def my_courses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor", "admin"))
):
    courses = db.query(models.Course).options(joinedload(models.Course.tutor)).filter(
        models.Course.tutor_id == current_user.id
    ).all()
    return [enrich_course(c, db) for c in courses]


@router.get("/{course_id}", response_model=CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth_utils.get_current_user)
):
    course = db.query(models.Course).options(joinedload(models.Course.tutor)).filter(
        models.Course.id == course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return enrich_course(course, db)


@router.post("/", response_model=CourseOut)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor", "admin"))
):
    course = models.Course(
        tutor_id=current_user.id,
        title=data.title,
        description=data.description,
        category=data.category,
        thumbnail_url=data.thumbnail_url,
        price=data.price,
        school_restricted=data.school_restricted,
        is_published=True
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    # reload with tutor
    course = db.query(models.Course).options(joinedload(models.Course.tutor)).filter(
        models.Course.id == course.id
    ).first()
    return enrich_course(course, db)


@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor", "admin"))
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    if current_user.role != "admin" and course.tutor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sin permisos")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    course = db.query(models.Course).options(joinedload(models.Course.tutor)).filter(
        models.Course.id == course.id
    ).first()
    return enrich_course(course, db)


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor", "admin"))
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    if current_user.role != "admin" and course.tutor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sin permisos")
    db.delete(course)
    db.commit()
    return {"message": "Curso eliminado"}
