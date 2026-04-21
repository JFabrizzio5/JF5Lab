"""Motor de dunning flows: programa runs al asignar un flow a una factura."""
from __future__ import annotations
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from modules.cobranza.models.models import DunningFlow, DunningRun, Invoice


async def schedule_flow(db: AsyncSession, invoice_id: UUID, flow_id: UUID, tenant_id: str) -> list[DunningRun]:
    inv = await db.get(Invoice, invoice_id)
    flow = await db.get(DunningFlow, flow_id)
    if not inv or not flow:
        raise ValueError("invoice o flow no existe")
    base = inv.due_at or datetime.utcnow()
    runs = []
    for idx, step in enumerate(flow.steps or []):
        day = int(step.get("day", 0))
        scheduled = base + timedelta(days=day)
        run = DunningRun(
            tenant_id=inv.tenant_id,
            invoice_id=inv.id,
            flow_id=flow.id,
            step_index=idx,
            scheduled_at=scheduled,
            channel=step.get("channel"),
            status="queued",
        )
        db.add(run)
        runs.append(run)
    await db.flush()
    return runs


def render_template(body: str, variables: dict) -> str:
    out = body or ""
    for k, v in variables.items():
        out = out.replace("{{" + k + "}}", str(v) if v is not None else "")
    return out


async def execute_run_stub(db: AsyncSession, run_id: UUID) -> dict:
    """Stub: marca el run como sent y registra message_id fake.
    Integracion real con WhatsApp/Twilio/SES = TODO.
    """
    run = await db.get(DunningRun, run_id)
    if not run:
        raise ValueError("run no existe")
    run.executed_at = datetime.utcnow()
    run.status = "sent"
    run.message_id = f"stub_{run.id.hex[:12]}"
    await db.flush()
    return {"run_id": str(run.id), "status": run.status, "message_id": run.message_id, "channel": run.channel}
