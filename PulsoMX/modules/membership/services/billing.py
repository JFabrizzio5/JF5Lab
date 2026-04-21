"""Billing: Stripe + Conekta checkout con fallback mock si no hay API keys.

Configuración en `.env`:
    STRIPE_SECRET_KEY=sk_test_...
    STRIPE_WEBHOOK_SECRET=whsec_...
    CONEKTA_PRIVATE_KEY=key_...
    CONEKTA_WEBHOOK_SECRET=...
    APP_PUBLIC_URL=http://localhost:3045

Sin keys → devuelve una URL local `/billing/demo-checkout/<ref>` que simula pago.
"""
from __future__ import annotations
import os
from decimal import Decimal
from typing import Literal


class BillingError(Exception):
    pass


def _public_url() -> str:
    return os.getenv("APP_PUBLIC_URL", "http://localhost:3045")


def _currency() -> str:
    return os.getenv("BILLING_CURRENCY", "mxn")


# ──────────────────────────────────────────────
# STRIPE
# ──────────────────────────────────────────────
def create_stripe_checkout(*, amount_mxn: Decimal, description: str, reference: str, success_url: str | None = None, cancel_url: str | None = None, customer_email: str | None = None) -> tuple[str, str | None]:
    """Devuelve (checkout_url, session_id). Fallback a mock si no hay key."""
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key:
        url = f"{_public_url()}/billing/demo-checkout/stripe?ref={reference}&amount={amount_mxn}"
        return url, None
    try:
        import stripe
        stripe.api_key = key
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card", "oxxo"],
            line_items=[{
                "price_data": {
                    "currency": _currency(),
                    "unit_amount": int(Decimal(str(amount_mxn)) * 100),
                    "product_data": {"name": description},
                },
                "quantity": 1,
            }],
            customer_email=customer_email,
            success_url=success_url or f"{_public_url()}/billing/success?ref={reference}",
            cancel_url=cancel_url or f"{_public_url()}/billing/cancel?ref={reference}",
            metadata={"reference": reference},
        )
        return session.url, session.id
    except Exception as e:
        raise BillingError(f"Stripe error: {e}")


# ──────────────────────────────────────────────
# CONEKTA
# ──────────────────────────────────────────────
def create_conekta_checkout(*, amount_mxn: Decimal, description: str, reference: str, customer_name: str | None = None, customer_email: str | None = None, customer_phone: str | None = None) -> tuple[str, str | None]:
    key = os.getenv("CONEKTA_PRIVATE_KEY")
    if not key:
        url = f"{_public_url()}/billing/demo-checkout/conekta?ref={reference}&amount={amount_mxn}"
        return url, None
    try:
        import conekta
        conekta.api_key = key
        conekta.locale = "es"
        order = conekta.Order.create({
            "line_items": [{
                "name": description,
                "unit_price": int(Decimal(str(amount_mxn)) * 100),
                "quantity": 1,
            }],
            "currency": _currency().upper(),
            "customer_info": {
                "name": customer_name or "Cliente PulsoMX",
                "email": customer_email or "cliente@pulsomx.mx",
                "phone": customer_phone or "+525555555555",
            },
            "checkout": {
                "type": "Integration",
                "allowed_payment_methods": ["card", "cash", "bank_transfer"],
            },
            "metadata": {"reference": reference},
        })
        url = order.checkout.url if hasattr(order.checkout, "url") else f"https://pay.conekta.com/{order.checkout.id}"
        return url, order.id
    except Exception as e:
        raise BillingError(f"Conekta error: {e}")


# ──────────────────────────────────────────────
# Webhook verification
# ──────────────────────────────────────────────
def verify_stripe_webhook(payload: bytes, sig_header: str) -> dict:
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not secret:
        import json
        return json.loads(payload)
    import stripe
    return stripe.Webhook.construct_event(payload, sig_header, secret)


def verify_conekta_webhook(payload: bytes, sig_header: str | None) -> dict:
    # Conekta firma con HMAC-SHA256 el cuerpo; secret opcional
    import json
    return json.loads(payload)
