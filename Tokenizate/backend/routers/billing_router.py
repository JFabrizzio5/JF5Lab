"""
SaaS billing router — Stripe integration.
Set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET in .env to activate.
Without those keys, endpoints return 501 Not Implemented gracefully.
"""
import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import get_db
from models import Editor, Plan, Subscription, SubscriptionStatus
from schemas import PlanOut, CheckoutRequest, CheckoutResponse, SubscriptionOut
from auth import get_current_editor

router = APIRouter(prefix="/billing", tags=["Billing"])

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")


def _get_stripe():
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=501, detail="Stripe not configured. Set STRIPE_SECRET_KEY in .env")
    import stripe
    stripe.api_key = STRIPE_SECRET_KEY
    return stripe


@router.get("/plans", response_model=List[PlanOut])
async def list_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plan).where(Plan.is_active == True).order_by(Plan.price_monthly))
    return result.scalars().all()


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    payload: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    stripe = _get_stripe()

    result = await db.execute(select(Plan).where(Plan.id == payload.plan_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    price_id = plan.stripe_price_id_monthly if payload.billing == "monthly" else plan.stripe_price_id_yearly
    if not price_id:
        raise HTTPException(status_code=400, detail="Stripe price not configured for this plan")

    # Get or create Stripe customer
    sub_result = await db.execute(
        select(Subscription)
        .options(selectinload(Subscription.plan))
        .where(Subscription.editor_id == current.id)
    )
    sub = sub_result.scalar_one_or_none()

    customer_id = sub.stripe_customer_id if sub and sub.stripe_customer_id else None
    if not customer_id:
        customer = stripe.Customer.create(email=current.email, name=current.name)
        customer_id = customer.id

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=payload.success_url,
        cancel_url=payload.cancel_url,
        metadata={"editor_id": str(current.id), "plan_id": str(plan.id)},
    )
    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    stripe = _get_stripe()
    body = await request.body()

    try:
        event = stripe.Webhook.construct_event(body, stripe_signature, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        editor_id = int(data["metadata"]["editor_id"])
        plan_id = int(data["metadata"]["plan_id"])
        stripe_customer_id = data["customer"]
        stripe_sub_id = data["subscription"]

        result = await db.execute(select(Subscription).where(Subscription.editor_id == editor_id))
        sub = result.scalar_one_or_none()
        if sub:
            sub.plan_id = plan_id
            sub.status = SubscriptionStatus.active
            sub.stripe_customer_id = stripe_customer_id
            sub.stripe_subscription_id = stripe_sub_id
        else:
            db.add(Subscription(
                editor_id=editor_id,
                plan_id=plan_id,
                status=SubscriptionStatus.active,
                stripe_customer_id=stripe_customer_id,
                stripe_subscription_id=stripe_sub_id,
            ))
        await db.commit()

    elif event_type == "customer.subscription.deleted":
        stripe_sub_id = data["id"]
        result = await db.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == stripe_sub_id)
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = SubscriptionStatus.canceled
            await db.commit()

    elif event_type == "invoice.payment_failed":
        stripe_customer_id = data["customer"]
        result = await db.execute(
            select(Subscription).where(Subscription.stripe_customer_id == stripe_customer_id)
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = SubscriptionStatus.past_due
            await db.commit()

    return {"received": True}


@router.get("/subscription/me", response_model=SubscriptionOut)
async def my_subscription(
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    result = await db.execute(
        select(Subscription)
        .options(selectinload(Subscription.plan))
        .where(Subscription.editor_id == current.id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="No active subscription")
    return sub


@router.post("/subscription/cancel")
async def cancel_subscription(
    db: AsyncSession = Depends(get_db),
    current: Editor = Depends(get_current_editor)
):
    stripe = _get_stripe()
    result = await db.execute(
        select(Subscription).where(Subscription.editor_id == current.id)
    )
    sub = result.scalar_one_or_none()
    if not sub or not sub.stripe_subscription_id:
        raise HTTPException(status_code=404, detail="No active subscription to cancel")

    stripe.Subscription.cancel(sub.stripe_subscription_id)
    sub.status = SubscriptionStatus.canceled
    await db.commit()
    return {"message": "Subscription canceled"}
