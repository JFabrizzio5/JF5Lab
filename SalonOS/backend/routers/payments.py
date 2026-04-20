import stripe
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/payments", tags=["payments"])

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_CLIENT_ID = os.environ.get("STRIPE_CLIENT_ID", "")
PLATFORM_DOMAIN = os.environ.get("PLATFORM_DOMAIN", "http://localhost:3020")


class PaymentCreate(BaseModel):
    amount: float
    payment_type: str = "deposit"
    currency: str = "mxn"


def payment_out(p: models.Payment):
    return {
        "id": p.id,
        "booking_id": p.booking_id,
        "venue_id": p.venue_id,
        "amount": p.amount,
        "currency": p.currency,
        "stripe_payment_intent_id": p.stripe_payment_intent_id,
        "status": p.status,
        "platform_fee": p.platform_fee,
        "venue_amount": p.venue_amount,
        "payment_type": p.payment_type,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }


@router.post("/stripe-connect")
def get_stripe_connect_url(
    current_user: models.User = Depends(auth_utils.require_role("venue_owner")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    if not STRIPE_CLIENT_ID:
        raise HTTPException(400, "Stripe no configurado en el servidor")
    url = (
        f"https://connect.stripe.com/oauth/authorize"
        f"?response_type=code"
        f"&client_id={STRIPE_CLIENT_ID}"
        f"&scope=read_write"
        f"&redirect_uri={PLATFORM_DOMAIN}/api/payments/stripe-callback"
        f"&state={venue.id}"
    )
    return {"url": url}


@router.get("/stripe-callback")
def stripe_callback(code: str, state: int, db: Session = Depends(get_db)):
    if not stripe.api_key:
        raise HTTPException(400, "Stripe not configured")
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=code)
        account_id = response["stripe_user_id"]
    except Exception as e:
        raise HTTPException(400, f"Error de Stripe: {str(e)}")
    venue = db.query(models.Venue).filter(models.Venue.id == state).first()
    if not venue:
        raise HTTPException(404, "Venue no encontrado")
    venue.stripe_account_id = account_id
    venue.stripe_onboarding_complete = True
    db.commit()
    return RedirectResponse(f"{PLATFORM_DOMAIN}/settings?stripe=connected")


@router.post("/create-intent/{booking_id}")
def create_payment_intent(
    booking_id: int,
    data: PaymentCreate,
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db),
):
    booking = db.query(models.EventBooking).filter(models.EventBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Reserva no encontrada")
    venue = db.query(models.Venue).filter(models.Venue.id == booking.venue_id).first()

    if not venue.stripe_account_id or not stripe.api_key:
        raise HTTPException(400, "Stripe no configurado para este venue")

    amount_cents = int(data.amount * 100)
    platform_fee_cents = int(amount_cents * venue.platform_fee_percent / 100)

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=data.currency,
            application_fee_amount=platform_fee_cents,
            transfer_data={"destination": venue.stripe_account_id},
        )
    except Exception as e:
        raise HTTPException(400, f"Error de Stripe: {str(e)}")

    payment = models.Payment(
        booking_id=booking_id,
        venue_id=venue.id,
        amount=data.amount,
        currency=data.currency,
        stripe_payment_intent_id=intent.id,
        status="pending",
        platform_fee=platform_fee_cents / 100,
        venue_amount=(amount_cents - platform_fee_cents) / 100,
        payment_type=data.payment_type,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {"client_secret": intent.client_secret, "payment_id": payment.id}


@router.get("/history")
def payment_history(
    current_user: models.User = Depends(auth_utils.require_role("venue_owner", "venue_staff")),
    db: Session = Depends(get_db),
):
    venue = auth_utils.get_venue_for_user(current_user.id, db)
    payments = db.query(models.Payment).filter(
        models.Payment.venue_id == venue.id
    ).order_by(models.Payment.created_at.desc()).all()
    return [payment_out(p) for p in payments]
