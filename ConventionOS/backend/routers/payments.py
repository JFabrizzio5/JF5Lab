import stripe, os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db
import models, auth as auth_utils
import json, secrets

router = APIRouter(prefix="/payments", tags=["payments"])

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_CLIENT_ID = os.environ.get("STRIPE_CLIENT_ID", "")
PLATFORM_DOMAIN = os.environ.get("PLATFORM_DOMAIN", "http://localhost:3025")


@router.post("/stripe-connect/{convention_id}")
def get_stripe_connect_url(
    convention_id: int,
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    if not STRIPE_CLIENT_ID:
        raise HTTPException(400, "Stripe Connect no configurado en el servidor")
    url = (
        f"https://connect.stripe.com/oauth/authorize"
        f"?response_type=code"
        f"&client_id={STRIPE_CLIENT_ID}"
        f"&scope=read_write"
        f"&redirect_uri={PLATFORM_DOMAIN}/api/payments/stripe-callback"
        f"&state={convention_id}"
    )
    return {"url": url}


@router.get("/stripe-callback")
def stripe_callback(code: str = None, state: int = None, error: str = None, db: Session = Depends(get_db)):
    if error or not code:
        return RedirectResponse(f"{PLATFORM_DOMAIN}/organizer/settings?stripe=error")
    if not stripe.api_key:
        return RedirectResponse(f"{PLATFORM_DOMAIN}/organizer/settings?stripe=not_configured")
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=code)
        account_id = response["stripe_user_id"]
        conv = db.query(models.Convention).filter(models.Convention.id == state).first()
        if conv:
            conv.stripe_account_id = account_id
            conv.stripe_onboarding_complete = True
            db.commit()
    except Exception as e:
        return RedirectResponse(f"{PLATFORM_DOMAIN}/organizer/settings?stripe=error")
    return RedirectResponse(f"{PLATFORM_DOMAIN}/organizer/settings?stripe=connected")


class TicketPurchaseItem(BaseModel):
    ticket_type_id: int
    quantity: int


class TicketPurchaseRequest(BaseModel):
    convention_id: int
    buyer_name: str
    buyer_email: str
    buyer_phone: str = ""
    items: List[TicketPurchaseItem]


@router.post("/purchase")
def purchase_tickets(data: TicketPurchaseRequest, db: Session = Depends(get_db)):
    conv = db.query(models.Convention).filter(models.Convention.id == data.convention_id).first()
    if not conv:
        raise HTTPException(404, "Convención no encontrada")

    total = 0.0
    items_detail = []
    for item in data.items:
        tt = db.query(models.TicketType).filter(
            models.TicketType.id == item.ticket_type_id,
            models.TicketType.convention_id == data.convention_id,
            models.TicketType.is_active == True
        ).first()
        if not tt:
            raise HTTPException(404, f"Tipo de ticket {item.ticket_type_id} no encontrado")
        available = (tt.quantity_total or 9999) - tt.quantity_sold
        if item.quantity > available:
            raise HTTPException(400, f"Solo quedan {available} boletos de {tt.name}")
        subtotal = tt.price * item.quantity
        total += subtotal
        items_detail.append({
            "ticket_type_id": tt.id,
            "name": tt.name,
            "quantity": item.quantity,
            "price": tt.price,
            "subtotal": subtotal
        })

    platform_fee = round(total * conv.platform_fee_percent / 100, 2)
    organizer_amount = round(total - platform_fee, 2)

    payment = models.TicketPayment(
        convention_id=data.convention_id,
        amount=total,
        platform_fee=platform_fee,
        organizer_amount=organizer_amount,
        status="pending",
        buyer_name=data.buyer_name,
        buyer_email=data.buyer_email,
        items_json=json.dumps(items_detail),
    )
    db.add(payment)
    db.flush()

    if stripe.api_key and conv.stripe_account_id and total > 0:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency="mxn",
                application_fee_amount=int(platform_fee * 100),
                transfer_data={"destination": conv.stripe_account_id},
                metadata={"payment_id": str(payment.id), "convention": conv.slug},
            )
            payment.stripe_payment_intent_id = intent.id
            db.commit()
            return {
                "payment_id": payment.id,
                "total": total,
                "platform_fee": platform_fee,
                "organizer_amount": organizer_amount,
                "stripe_client_secret": intent.client_secret,
                "items": items_detail,
            }
        except Exception as e:
            pass

    db.commit()
    _create_tickets(payment.id, data, items_detail, db)
    return {
        "payment_id": payment.id,
        "total": total,
        "platform_fee": platform_fee,
        "organizer_amount": organizer_amount,
        "stripe_client_secret": None,
        "items": items_detail,
        "note": "Pago manual — contacta al organizador para confirmar",
    }


@router.post("/confirm/{payment_id}")
def confirm_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.TicketPayment).filter(models.TicketPayment.id == payment_id).first()
    if not payment:
        raise HTTPException(404, "Pago no encontrado")
    if payment.status == "succeeded":
        return {"message": "Ya confirmado"}
    payment.status = "succeeded"
    items = json.loads(payment.items_json or "[]")
    for item in items:
        tt = db.query(models.TicketType).filter(models.TicketType.id == item["ticket_type_id"]).first()
        if tt:
            for _ in range(item["quantity"]):
                ticket = models.Ticket(
                    ticket_type_id=tt.id,
                    convention_id=payment.convention_id,
                    attendee_name=payment.buyer_name,
                    attendee_email=payment.buyer_email,
                    qr_code=secrets.token_hex(8).upper(),
                    status="paid",
                    payment_id=payment.id,
                )
                db.add(ticket)
                tt.quantity_sold += 1
    db.commit()
    return {"message": "Pago confirmado", "tickets_created": True}


def _create_tickets(payment_id, data, items_detail, db):
    for item in items_detail:
        tt = db.query(models.TicketType).filter(models.TicketType.id == item["ticket_type_id"]).first()
        if tt:
            for _ in range(item["quantity"]):
                ticket = models.Ticket(
                    ticket_type_id=tt.id,
                    convention_id=tt.convention_id,
                    attendee_name=data.buyer_name,
                    attendee_email=data.buyer_email,
                    attendee_phone=data.buyer_phone,
                    qr_code=secrets.token_hex(8).upper(),
                    status="pending",
                    payment_id=payment_id,
                )
                db.add(ticket)
                tt.quantity_sold += 1
    db.commit()


@router.get("/history")
def payment_history(
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    conv = db.query(models.Convention).filter(models.Convention.organizer_id == current_user.id).first()
    if not conv:
        return []
    payments = db.query(models.TicketPayment).filter(
        models.TicketPayment.convention_id == conv.id
    ).order_by(models.TicketPayment.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "buyer_name": p.buyer_name,
            "buyer_email": p.buyer_email,
            "amount": p.amount,
            "platform_fee": p.platform_fee,
            "organizer_amount": p.organizer_amount,
            "status": p.status,
            "items": json.loads(p.items_json or "[]"),
            "created_at": p.created_at.isoformat(),
        }
        for p in payments
    ]


@router.get("/stats")
def payment_stats(
    current_user: models.User = Depends(auth_utils.require_role("organizer", "superadmin")),
    db: Session = Depends(get_db)
):
    conv = db.query(models.Convention).filter(models.Convention.organizer_id == current_user.id).first()
    if not conv:
        return {"total_revenue": 0, "platform_fees": 0, "net_to_organizer": 0, "total_payments": 0}
    payments = db.query(models.TicketPayment).filter(
        models.TicketPayment.convention_id == conv.id,
        models.TicketPayment.status == "succeeded"
    ).all()
    total_revenue = sum(p.amount for p in payments)
    platform_fees = sum(p.platform_fee for p in payments)
    net = sum(p.organizer_amount for p in payments)
    tickets_sold = db.query(models.Ticket).filter(
        models.Ticket.convention_id == conv.id,
        models.Ticket.status.in_(["paid", "checked_in"])
    ).count()
    checked_in = db.query(models.Ticket).filter(
        models.Ticket.convention_id == conv.id,
        models.Ticket.status == "checked_in"
    ).count()
    return {
        "total_revenue": total_revenue,
        "platform_fees": platform_fees,
        "net_to_organizer": net,
        "total_payments": len(payments),
        "tickets_sold": tickets_sold,
        "checked_in": checked_in,
        "convention": {"id": conv.id, "name": conv.name, "status": conv.status,
                       "stripe_onboarding_complete": conv.stripe_onboarding_complete},
    }
