"""Payment score simple (0-100). Recalcula desde payment_score_events + hábito de pago."""
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from modules.cobranza.models.models import Debtor, Invoice, Payment, PaymentScoreEvent


EVENT_WEIGHTS = {
    "paid_on_time": +10,
    "paid_late": -5,
    "paid_very_late": -15,
    "dispute": -20,
    "contact_responded": +3,
    "ignored": -4,
    "partial_payment": -2,
}


async def recalculate_debtor_score(db: AsyncSession, debtor_id) -> dict:
    # base 50 neutro
    score = 50
    # aplica eventos pasados 90 días
    since = datetime.utcnow() - timedelta(days=180)
    res = await db.execute(
        select(PaymentScoreEvent).where(PaymentScoreEvent.debtor_id == debtor_id, PaymentScoreEvent.at >= since)
    )
    events = res.scalars().all()
    for ev in events:
        score += ev.delta or EVENT_WEIGHTS.get(ev.event, 0)

    # Ajuste por facturas vencidas
    res = await db.execute(
        select(Invoice).where(Invoice.debtor_id == debtor_id, Invoice.status.in_(("pending", "partial", "overdue")))
    )
    pending = res.scalars().all()
    now = datetime.utcnow()
    total_owed = Decimal("0")
    overdue_days = []
    for inv in pending:
        total_owed += (inv.total or 0) - (inv.paid_amount or 0)
        if inv.due_at and inv.due_at < now:
            days = (now - inv.due_at).days
            overdue_days.append(days)
            if days > 90: score -= 30
            elif days > 60: score -= 18
            elif days > 30: score -= 10
            elif days > 0: score -= 3

    score = max(0, min(100, score))

    # Actualiza el debtor
    deb = await db.get(Debtor, debtor_id)
    if deb:
        deb.payment_score = score
        deb.total_owed = total_owed
        deb.overdue_days_avg = int(sum(overdue_days) / len(overdue_days)) if overdue_days else 0
        await db.flush()
    return {"debtor_id": str(debtor_id), "score": score, "total_owed": float(total_owed), "overdue_days_avg": deb.overdue_days_avg if deb else 0}
