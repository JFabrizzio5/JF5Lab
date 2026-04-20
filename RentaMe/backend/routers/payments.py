import stripe
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/payments", tags=["payments"])
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_CLIENT_ID = os.environ.get("STRIPE_CLIENT_ID", "")
PLATFORM_DOMAIN = os.environ.get("PLATFORM_DOMAIN", "http://localhost:3030")


@router.post("/stripe-connect")
def get_stripe_connect_url(
    current_user: models.User = Depends(auth_utils.require_role("vendor")),
    db: Session = Depends(get_db),
):
    if not STRIPE_CLIENT_ID:
        raise HTTPException(400, "Stripe Connect no configurado. Agrega STRIPE_CLIENT_ID al servidor.")
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        raise HTTPException(404, "Perfil de vendedor no encontrado")
    url = (
        f"https://connect.stripe.com/oauth/authorize"
        f"?response_type=code&client_id={STRIPE_CLIENT_ID}&scope=read_write"
        f"&redirect_uri={PLATFORM_DOMAIN}/api/payments/stripe-callback"
        f"&state={vendor.id}"
    )
    return {"url": url}


@router.get("/stripe-callback")
def stripe_callback(
    code: str = None,
    state: int = None,
    error: str = None,
    db: Session = Depends(get_db),
):
    if error or not code:
        return RedirectResponse(f"{PLATFORM_DOMAIN}/vendor/settings?stripe=error")
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=code)
        vendor = db.query(models.VendorProfile).filter(models.VendorProfile.id == state).first()
        if vendor:
            vendor.stripe_account_id = response["stripe_user_id"]
            vendor.stripe_onboarding_complete = True
            db.commit()
    except Exception:
        return RedirectResponse(f"{PLATFORM_DOMAIN}/vendor/settings?stripe=error")
    return RedirectResponse(f"{PLATFORM_DOMAIN}/vendor/settings?stripe=connected")


class PaymentRequest(BaseModel):
    booking_id: int
    amount: float
    payment_type: str = "deposit"


@router.post("/create-intent")
def create_intent(data: PaymentRequest, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == data.booking_id).first()
    if not booking:
        raise HTTPException(404, "Reserva no encontrada")
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.id == booking.vendor_id).first()
    if not vendor or not vendor.stripe_account_id or not stripe.api_key:
        raise HTTPException(400, "Pagos Stripe no configurados para este vendedor")

    amount_cents = int(data.amount * 100)
    fee_cents = int(amount_cents * vendor.platform_fee_percent / 100)

    intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency="mxn",
        application_fee_amount=fee_cents,
        transfer_data={"destination": vendor.stripe_account_id},
        metadata={"booking_id": str(booking.id)},
    )

    payment = models.Payment(
        booking_id=booking.id,
        vendor_id=vendor.id,
        amount=data.amount,
        stripe_payment_intent_id=intent.id,
        status="pending",
        platform_fee=fee_cents / 100,
        vendor_amount=(amount_cents - fee_cents) / 100,
        payment_type=data.payment_type,
    )
    db.add(payment)
    db.commit()
    return {"client_secret": intent.client_secret, "payment_id": payment.id}


@router.get("/history")
def payment_history(
    current_user: models.User = Depends(auth_utils.require_role("vendor")),
    db: Session = Depends(get_db),
):
    vendor = db.query(models.VendorProfile).filter(models.VendorProfile.user_id == current_user.id).first()
    if not vendor:
        return []
    payments = (
        db.query(models.Payment)
        .filter(models.Payment.vendor_id == vendor.id)
        .order_by(models.Payment.created_at.desc())
        .limit(100)
        .all()
    )
    return [
        {
            "id": p.id,
            "booking_id": p.booking_id,
            "amount": p.amount,
            "platform_fee": p.platform_fee,
            "vendor_amount": p.vendor_amount,
            "status": p.status,
            "payment_type": p.payment_type,
            "created_at": p.created_at.isoformat(),
        }
        for p in payments
    ]
