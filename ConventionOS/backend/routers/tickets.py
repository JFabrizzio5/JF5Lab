from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/tickets", tags=["tickets"])


class TicketTypeCreate(BaseModel):
    convention_id: int
    name: str
    description: Optional[str] = None
    price: Optional[float] = 0.0
    quantity_total: Optional[int] = None
    benefits_json: Optional[str] = None
    color: Optional[str] = "#6366f1"
    sale_start: Optional[str] = None
    sale_end: Optional[str] = None


def tt_to_dict(t: models.TicketType):
    return {
        "id": t.id,
        "convention_id": t.convention_id,
        "name": t.name,
        "description": t.description,
        "price": t.price,
        "quantity_total": t.quantity_total,
        "quantity_sold": t.quantity_sold,
        "benefits_json": t.benefits_json,
        "color": t.color,
        "sale_start": t.sale_start.isoformat() if t.sale_start else None,
        "sale_end": t.sale_end.isoformat() if t.sale_end else None,
        "is_active": t.is_active,
    }


def ticket_to_dict(t: models.Ticket):
    return {
        "id": t.id,
        "ticket_type_id": t.ticket_type_id,
        "convention_id": t.convention_id,
        "attendee_name": t.attendee_name,
        "attendee_email": t.attendee_email,
        "attendee_phone": t.attendee_phone,
        "qr_code": t.qr_code,
        "status": t.status,
        "payment_id": t.payment_id,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "ticket_type": {"id": t.ticket_type.id, "name": t.ticket_type.name, "color": t.ticket_type.color} if t.ticket_type else None,
    }


def check_conv_owner(conv_id: int, user: models.User, db: Session):
    conv = db.query(models.Convention).filter(models.Convention.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "Convention not found")
    if user.role != "superadmin" and conv.organizer_id != user.id:
        raise HTTPException(403, "Forbidden")
    return conv


@router.get("/types/convention/{convention_id}")
def list_ticket_types(convention_id: int, db: Session = Depends(get_db)):
    tts = db.query(models.TicketType).filter(
        models.TicketType.convention_id == convention_id,
        models.TicketType.is_active == True
    ).all()
    return [tt_to_dict(t) for t in tts]


@router.post("/types")
def create_ticket_type(
    data: TicketTypeCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(data.convention_id, current_user, db)
    from datetime import datetime
    tt = models.TicketType(
        convention_id=data.convention_id,
        name=data.name,
        description=data.description,
        price=data.price or 0.0,
        quantity_total=data.quantity_total,
        benefits_json=data.benefits_json,
        color=data.color or "#6366f1",
        sale_start=datetime.fromisoformat(data.sale_start) if data.sale_start else None,
        sale_end=datetime.fromisoformat(data.sale_end) if data.sale_end else None,
    )
    db.add(tt)
    db.commit()
    db.refresh(tt)
    return tt_to_dict(tt)


@router.put("/types/{type_id}")
def update_ticket_type(
    type_id: int,
    data: TicketTypeCreate,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    tt = db.query(models.TicketType).filter(models.TicketType.id == type_id).first()
    if not tt:
        raise HTTPException(404, "Not found")
    check_conv_owner(tt.convention_id, current_user, db)
    from datetime import datetime
    for field in ("name", "description", "price", "quantity_total", "benefits_json", "color"):
        val = getattr(data, field)
        if val is not None:
            setattr(tt, field, val)
    if data.sale_start:
        tt.sale_start = datetime.fromisoformat(data.sale_start)
    if data.sale_end:
        tt.sale_end = datetime.fromisoformat(data.sale_end)
    db.commit()
    db.refresh(tt)
    return tt_to_dict(tt)


@router.delete("/types/{type_id}")
def delete_ticket_type(
    type_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    tt = db.query(models.TicketType).filter(models.TicketType.id == type_id).first()
    if not tt:
        raise HTTPException(404, "Not found")
    check_conv_owner(tt.convention_id, current_user, db)
    tt.is_active = False
    db.commit()
    return {"message": "Deleted"}


@router.get("/convention/{convention_id}")
def list_tickets(
    convention_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    check_conv_owner(convention_id, current_user, db)
    tickets = db.query(models.Ticket).filter(
        models.Ticket.convention_id == convention_id
    ).order_by(models.Ticket.created_at.desc()).all()
    return [ticket_to_dict(t) for t in tickets]


@router.patch("/{ticket_id}/checkin")
def checkin_ticket(
    ticket_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Not found")
    check_conv_owner(ticket.convention_id, current_user, db)
    ticket.status = "checked_in" if ticket.status != "checked_in" else "paid"
    db.commit()
    return ticket_to_dict(ticket)
