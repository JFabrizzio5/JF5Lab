from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/schedule", tags=["schedule"])

DAY_NAMES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


class SlotCreate(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    price_per_hour: float = 0.0
    school_restricted: bool = False


class SlotUpdate(BaseModel):
    is_available: Optional[bool] = None
    price_per_hour: Optional[float] = None
    school_restricted: Optional[bool] = None


class BookingCreate(BaseModel):
    tutor_id: int
    slot_id: int
    date: str
    subject: Optional[str] = None
    notes: Optional[str] = None


class BookingStatusUpdate(BaseModel):
    status: str


@router.get("/tutors")
def list_tutors(db: Session = Depends(get_db)):
    tutors = db.query(models.User).filter(models.User.role == "tutor", models.User.is_active == True).all()
    result = []
    for t in tutors:
        slots = db.query(models.TimeSlot).filter(
            models.TimeSlot.tutor_id == t.id,
            models.TimeSlot.is_available == True
        ).all()
        result.append({
            "id": t.id,
            "name": t.name,
            "school": t.school,
            "avatar_url": t.avatar_url,
            "slot_count": len(slots)
        })
    return result


@router.get("/slots/tutor/{tutor_id}")
def get_tutor_slots(
    tutor_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth_utils.get_current_user)
):
    slots = db.query(models.TimeSlot).filter(
        models.TimeSlot.tutor_id == tutor_id
    ).all()
    tutor = db.query(models.User).filter(models.User.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")

    result = []
    for s in slots:
        if s.school_restricted and current_user and current_user.school != tutor.school:
            continue
        result.append({
            "id": s.id,
            "day_of_week": s.day_of_week,
            "day_name": DAY_NAMES[s.day_of_week],
            "start_time": s.start_time,
            "end_time": s.end_time,
            "is_available": s.is_available,
            "price_per_hour": s.price_per_hour,
            "school_restricted": s.school_restricted
        })
    return result


@router.get("/slots/my")
def my_slots(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor"))
):
    slots = db.query(models.TimeSlot).filter(
        models.TimeSlot.tutor_id == current_user.id
    ).all()
    return [{
        "id": s.id,
        "day_of_week": s.day_of_week,
        "day_name": DAY_NAMES[s.day_of_week],
        "start_time": s.start_time,
        "end_time": s.end_time,
        "is_available": s.is_available,
        "price_per_hour": s.price_per_hour,
        "school_restricted": s.school_restricted
    } for s in slots]


@router.post("/slots")
def create_slot(
    data: SlotCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor"))
):
    if data.day_of_week < 0 or data.day_of_week > 6:
        raise HTTPException(status_code=400, detail="Día inválido (0-6)")
    slot = models.TimeSlot(
        tutor_id=current_user.id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
        is_available=True,
        price_per_hour=data.price_per_hour,
        school_restricted=data.school_restricted
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return {"id": slot.id, "message": "Slot creado"}


@router.put("/slots/{slot_id}")
def update_slot(
    slot_id: int,
    data: SlotUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor"))
):
    slot = db.query(models.TimeSlot).filter(
        models.TimeSlot.id == slot_id,
        models.TimeSlot.tutor_id == current_user.id
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot no encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(slot, field, value)
    db.commit()
    return {"message": "Slot actualizado"}


@router.delete("/slots/{slot_id}")
def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("tutor"))
):
    slot = db.query(models.TimeSlot).filter(
        models.TimeSlot.id == slot_id,
        models.TimeSlot.tutor_id == current_user.id
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot no encontrado")
    db.delete(slot)
    db.commit()
    return {"message": "Slot eliminado"}


@router.post("/bookings")
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.require_role("student"))
):
    slot = db.query(models.TimeSlot).filter(
        models.TimeSlot.id == data.slot_id,
        models.TimeSlot.tutor_id == data.tutor_id,
        models.TimeSlot.is_available == True
    ).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot no disponible")

    tutor = db.query(models.User).filter(models.User.id == data.tutor_id).first()
    if slot.school_restricted and tutor.school != current_user.school:
        raise HTTPException(status_code=403, detail="Slot solo para misma escuela")

    existing = db.query(models.Booking).filter(
        models.Booking.slot_id == data.slot_id,
        models.Booking.date == data.date,
        models.Booking.status.in_(["pending", "confirmed"])
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slot ya reservado para esa fecha")

    booking = models.Booking(
        student_id=current_user.id,
        tutor_id=data.tutor_id,
        slot_id=data.slot_id,
        date=data.date,
        status="pending",
        subject=data.subject,
        notes=data.notes
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {"message": "Reserva creada", "booking_id": booking.id}


@router.get("/bookings/my")
def my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    if current_user.role == "student":
        bookings = db.query(models.Booking).options(
            joinedload(models.Booking.tutor),
            joinedload(models.Booking.slot)
        ).filter(models.Booking.student_id == current_user.id).all()
    else:
        bookings = db.query(models.Booking).options(
            joinedload(models.Booking.student),
            joinedload(models.Booking.slot)
        ).filter(models.Booking.tutor_id == current_user.id).all()

    result = []
    for b in bookings:
        item = {
            "id": b.id,
            "date": b.date,
            "status": b.status,
            "subject": b.subject,
            "notes": b.notes,
            "slot_start": b.slot.start_time if b.slot else None,
            "slot_end": b.slot.end_time if b.slot else None,
        }
        if current_user.role == "student":
            item["tutor_name"] = b.tutor.name if b.tutor else ""
            item["tutor_id"] = b.tutor_id
        else:
            item["student_name"] = b.student.name if b.student else ""
            item["student_id"] = b.student_id
        result.append(item)
    return result


@router.put("/bookings/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    data: BookingStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if current_user.role == "student" and booking.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sin permisos")
    if current_user.role == "tutor" and booking.tutor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sin permisos")

    valid_statuses = ["pending", "confirmed", "cancelled", "completed"]
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Estado inválido")

    booking.status = data.status
    db.commit()
    return {"message": "Estado actualizado"}
