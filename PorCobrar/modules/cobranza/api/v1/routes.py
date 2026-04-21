"""PorCobrar API /cobrar/v1."""
from __future__ import annotations
import os
import secrets
import csv
import io
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Body, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, RedirectResponse
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from config.database import get_sql_db
from core.tenant import tenant_db, get_tenant_id, raw_db
from modules.cobranza.models.models import (
    Tenant, TenantPlan, Plan, Debtor, Invoice, DunningFlow, DunningTemplate,
    DunningRun, Payment, PaymentLink, PaymentScoreEvent, NoteLog,
)
from modules.cobranza.schemas import (
    TenantCreate, TenantOut, DebtorCreate, DebtorOut, InvoiceCreate, InvoiceOut,
    DunningTemplateCreate, DunningTemplateOut, DunningFlowCreate, DunningFlowOut, AssignFlow,
)
from modules.cobranza.services.cfdi_parser import parse_cfdi_xml
from modules.cobranza.services.scoring import recalculate_debtor_score
from modules.cobranza.services.dunning import schedule_flow, execute_run_stub, render_template
from modules.cobranza.services.seed import seed_industry, seed_plans
from modules.cobranza.services.exports import invoices_to_xlsx, debtors_to_xlsx, aging_to_xlsx
from services.billing import create_stripe_checkout, create_conekta_checkout


router = APIRouter()


# ═══════════════════════════════════════════════
# PLANES (global, no RLS necesita)
# ═══════════════════════════════════════════════
@router.get("/plans")
async def list_plans(db: AsyncSession = Depends(raw_db)):
    await seed_plans(db)
    await db.commit()
    res = await db.execute(select(Plan))
    return [{
        "id": p.id, "name": p.name, "price_mxn": float(p.price_mxn or 0),
        "max_invoices_month": p.max_invoices_month, "has_whatsapp": p.has_whatsapp,
        "has_ai_scoring": p.has_ai_scoring, "has_custom_brand": p.has_custom_brand,
        "description": p.description, "featured": p.featured,
    } for p in res.scalars().all()]


# ═══════════════════════════════════════════════
# TENANTS
# ═══════════════════════════════════════════════
@router.post("/tenants", response_model=TenantOut)
async def create_tenant(body: TenantCreate, db: AsyncSession = Depends(raw_db)):
    slug = body.name.lower().replace(" ", "-")[:60] + "-" + secrets.token_hex(3)
    t = Tenant(
        name=body.name, slug=slug, rfc=body.rfc, razon_social=body.razon_social,
        industry=body.industry, contact_email=body.contact_email,
        contact_phone=body.contact_phone, brand_color=body.brand_color,
    )
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return t


@router.get("/tenants/{tenant_id}", response_model=TenantOut)
async def get_tenant(tenant_id: UUID, db: AsyncSession = Depends(raw_db)):
    t = await db.get(Tenant, tenant_id)
    if not t:
        raise HTTPException(404, "tenant no existe")
    return t


# ═══════════════════════════════════════════════
# DEBTORS
# ═══════════════════════════════════════════════
@router.post("/debtors", response_model=DebtorOut)
async def create_debtor(body: DebtorCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    d = Debtor(tenant_id=tenant_id, **body.model_dump())
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return d


@router.get("/debtors", response_model=list[DebtorOut])
async def list_debtors(q: str | None = None, db: AsyncSession = Depends(tenant_db)):
    stmt = select(Debtor)
    if q:
        stmt = stmt.where(Debtor.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Debtor.total_owed.desc())
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/debtors/{debtor_id}", response_model=DebtorOut)
async def get_debtor(debtor_id: UUID, db: AsyncSession = Depends(tenant_db)):
    d = await db.get(Debtor, debtor_id)
    if not d:
        raise HTTPException(404, "deudor no existe")
    return d


@router.post("/debtors/{debtor_id}/recalculate-score")
async def recalc_score(debtor_id: UUID, db: AsyncSession = Depends(tenant_db)):
    result = await recalculate_debtor_score(db, debtor_id)
    await db.commit()
    return result


# ═══════════════════════════════════════════════
# INVOICES
# ═══════════════════════════════════════════════
@router.post("/invoices", response_model=InvoiceOut)
async def create_invoice(body: InvoiceCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    # Validar que el deudor pertenezca al tenant (RLS lo filtra automaticamente)
    d = await db.get(Debtor, body.debtor_id)
    if not d:
        raise HTTPException(404, "deudor no existe")
    inv = Invoice(tenant_id=tenant_id, **body.model_dump())
    if not inv.issued_at:
        inv.issued_at = datetime.utcnow()
    db.add(inv)
    await db.commit()
    await db.refresh(inv)
    return inv


@router.get("/invoices", response_model=list[InvoiceOut])
async def list_invoices(
    status: str | None = None, debtor_id: UUID | None = None,
    overdue: bool = False, limit: int = 200,
    db: AsyncSession = Depends(tenant_db),
):
    stmt = select(Invoice)
    if status:
        stmt = stmt.where(Invoice.status == status)
    if debtor_id:
        stmt = stmt.where(Invoice.debtor_id == debtor_id)
    if overdue:
        stmt = stmt.where(Invoice.due_at < datetime.utcnow(), Invoice.status != "paid")
    stmt = stmt.order_by(Invoice.due_at.asc()).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/invoices/{invoice_id}", response_model=InvoiceOut)
async def get_invoice(invoice_id: UUID, db: AsyncSession = Depends(tenant_db)):
    inv = await db.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(404, "factura no existe")
    return inv


@router.post("/invoices/import")
async def import_invoices(
    file: UploadFile = File(...),
    default_debtor_id: UUID | None = Form(default=None),
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(tenant_db),
):
    """Acepta un XML CFDI (1 factura) o CSV (rfc,name,email,phone,cfdi_uuid,folio,total,due_at)."""
    data = await file.read()
    filename = (file.filename or "").lower()
    created = 0
    errors = []

    if filename.endswith(".xml"):
        try:
            parsed = parse_cfdi_xml(data)
        except Exception as e:
            raise HTTPException(400, f"XML invalido: {e}")
        rfc = parsed.get("receptor_rfc") or "XAXX010101000"
        nombre = parsed.get("receptor_nombre") or rfc
        res = await db.execute(select(Debtor).where(Debtor.rfc == rfc))
        deb = res.scalars().first()
        if not deb:
            deb = Debtor(tenant_id=tenant_id, rfc=rfc, name=nombre)
            db.add(deb)
            await db.flush()
        inv = Invoice(
            tenant_id=tenant_id,
            debtor_id=deb.id,
            cfdi_uuid=parsed.get("uuid"),
            serie=parsed.get("serie"),
            folio=parsed.get("folio"),
            issued_at=parsed.get("fecha") or datetime.utcnow(),
            due_at=(parsed.get("fecha") or datetime.utcnow()) + timedelta(days=30),
            total=parsed.get("total") or Decimal("0"),
            source="cfdi_upload",
        )
        db.add(inv)
        created = 1
        await db.commit()
        return {"created": created, "invoice_id": str(inv.id), "debtor_id": str(deb.id), "uuid": inv.cfdi_uuid}

    elif filename.endswith(".csv"):
        text = data.decode("utf-8", errors="ignore")
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            try:
                rfc = (row.get("rfc") or "XAXX010101000").strip()
                name = (row.get("name") or rfc).strip()
                res = await db.execute(select(Debtor).where(Debtor.rfc == rfc))
                deb = res.scalars().first()
                if not deb:
                    deb = Debtor(tenant_id=tenant_id, rfc=rfc, name=name,
                                 email=row.get("email"), phone=row.get("phone"))
                    db.add(deb)
                    await db.flush()
                due_raw = row.get("due_at")
                due = datetime.fromisoformat(due_raw) if due_raw else datetime.utcnow() + timedelta(days=30)
                inv = Invoice(
                    tenant_id=tenant_id,
                    debtor_id=deb.id,
                    cfdi_uuid=row.get("cfdi_uuid"),
                    folio=row.get("folio"),
                    total=Decimal(row.get("total") or "0"),
                    due_at=due,
                    issued_at=datetime.utcnow(),
                    source="manual",
                )
                db.add(inv)
                created += 1
            except Exception as e:
                errors.append({"row": row, "error": str(e)})
        await db.commit()
        return {"created": created, "errors": errors}

    else:
        raise HTTPException(400, "Solo se acepta .xml (CFDI) o .csv")


# ═══════════════════════════════════════════════
# PAYMENT LINKS + CHECKOUT
# ═══════════════════════════════════════════════
@router.post("/invoices/{invoice_id}/payment-link")
async def create_payment_link(invoice_id: UUID, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    inv = await db.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(404, "factura no existe")
    token = secrets.token_urlsafe(24)
    link = PaymentLink(tenant_id=tenant_id, invoice_id=inv.id, token=token,
                       expires_at=datetime.utcnow() + timedelta(days=60))
    db.add(link)
    await db.commit()
    await db.refresh(link)
    public_url = os.getenv("APP_PUBLIC_URL", "http://62.72.3.139:3060")
    return {
        "token": token,
        "link": f"{public_url}/pay/{token}",
        "expires_at": link.expires_at.isoformat(),
    }


@router.post("/invoices/{invoice_id}/checkout")
async def create_checkout(invoice_id: UUID, provider: str = Query("stripe"),
                          tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    inv = await db.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(404, "factura no existe")
    debtor = await db.get(Debtor, inv.debtor_id)
    amount = (inv.total or Decimal("0")) - (inv.paid_amount or Decimal("0"))
    ref = f"inv-{inv.id.hex[:12]}"
    desc = f"Pago factura {inv.serie or ''}{inv.folio or ''}"
    if provider == "stripe":
        url, sid = create_stripe_checkout(amount_mxn=amount, description=desc, reference=ref,
                                          customer_email=debtor.email if debtor else None)
        return {"url": url, "session_id": sid, "provider": "stripe"}
    elif provider == "conekta":
        url, oid = create_conekta_checkout(amount_mxn=amount, description=desc, reference=ref,
                                            customer_name=debtor.name if debtor else None,
                                            customer_email=debtor.email if debtor else None,
                                            customer_phone=debtor.phone if debtor else None)
        return {"url": url, "order_id": oid, "provider": "conekta"}
    raise HTTPException(400, "provider debe ser stripe|conekta")


# ═══════════════════════════════════════════════
# DUNNING FLOWS + TEMPLATES
# ═══════════════════════════════════════════════
@router.post("/dunning-templates", response_model=DunningTemplateOut)
async def create_template(body: DunningTemplateCreate, tenant_id: str = Depends(get_tenant_id),
                          db: AsyncSession = Depends(tenant_db)):
    t = DunningTemplate(tenant_id=tenant_id, **body.model_dump())
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return t


@router.get("/dunning-templates", response_model=list[DunningTemplateOut])
async def list_templates(db: AsyncSession = Depends(tenant_db)):
    res = await db.execute(select(DunningTemplate))
    return res.scalars().all()


@router.post("/dunning-flows", response_model=DunningFlowOut)
async def create_flow(body: DunningFlowCreate, tenant_id: str = Depends(get_tenant_id),
                      db: AsyncSession = Depends(tenant_db)):
    f = DunningFlow(tenant_id=tenant_id, **body.model_dump())
    db.add(f)
    await db.commit()
    await db.refresh(f)
    return f


@router.get("/dunning-flows", response_model=list[DunningFlowOut])
async def list_flows(db: AsyncSession = Depends(tenant_db)):
    res = await db.execute(select(DunningFlow))
    return res.scalars().all()


@router.post("/invoices/{invoice_id}/assign-flow")
async def assign_flow_to_invoice(invoice_id: UUID, body: AssignFlow,
                                  tenant_id: str = Depends(get_tenant_id),
                                  db: AsyncSession = Depends(tenant_db)):
    runs = await schedule_flow(db, invoice_id, body.flow_id, tenant_id)
    await db.commit()
    return {"scheduled_runs": [
        {"id": str(r.id), "scheduled_at": r.scheduled_at.isoformat(), "channel": r.channel, "step_index": r.step_index}
        for r in runs
    ]}


@router.get("/dunning/upcoming")
async def upcoming_runs(days: int = 7, db: AsyncSession = Depends(tenant_db)):
    horizon = datetime.utcnow() + timedelta(days=days)
    res = await db.execute(
        select(DunningRun).where(DunningRun.status == "queued",
                                  DunningRun.scheduled_at <= horizon).order_by(DunningRun.scheduled_at.asc())
    )
    runs = res.scalars().all()
    return [{
        "id": str(r.id), "invoice_id": str(r.invoice_id), "channel": r.channel,
        "scheduled_at": r.scheduled_at.isoformat(), "step_index": r.step_index,
    } for r in runs]


@router.post("/dunning/{run_id}/execute")
async def execute_dunning_run(run_id: UUID, db: AsyncSession = Depends(tenant_db)):
    result = await execute_run_stub(db, run_id)
    await db.commit()
    return result


# ═══════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════
@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(tenant_db)):
    now = datetime.utcnow()
    # total por cobrar (saldo pendiente)
    res = await db.execute(select(
        func.coalesce(func.sum(Invoice.total - Invoice.paid_amount), 0)
    ).where(Invoice.status.in_(("pending", "partial", "overdue"))))
    total_owed = float(res.scalar() or 0)

    # cobrado MTD
    month_start = datetime(now.year, now.month, 1)
    res = await db.execute(select(
        func.coalesce(func.sum(Payment.amount_mxn), 0)
    ).where(Payment.status == "succeeded", Payment.paid_at >= month_start))
    paid_mtd = float(res.scalar() or 0)

    # DSO simplificado: promedio de dias entre emision y pago
    res = await db.execute(select(
        func.coalesce(func.avg(func.extract("epoch", Payment.paid_at - Invoice.issued_at) / 86400), 0)
    ).join(Invoice, Invoice.id == Payment.invoice_id).where(Payment.status == "succeeded"))
    dso = float(res.scalar() or 0)

    # Cartera por edad
    buckets = {"0-30": {"count": 0, "amount": 0}, "31-60": {"count": 0, "amount": 0},
               "61-90": {"count": 0, "amount": 0}, "+90": {"count": 0, "amount": 0}}
    res = await db.execute(select(Invoice).where(Invoice.status.in_(("pending", "partial", "overdue"))))
    for inv in res.scalars().all():
        days = (now - inv.due_at).days if inv.due_at else 0
        saldo = float((inv.total or 0) - (inv.paid_amount or 0))
        if days <= 30: key = "0-30"
        elif days <= 60: key = "31-60"
        elif days <= 90: key = "61-90"
        else: key = "+90"
        buckets[key]["count"] += 1
        buckets[key]["amount"] += saldo

    # Top 5 deudores
    res = await db.execute(select(Debtor).order_by(Debtor.total_owed.desc()).limit(5))
    top = [{"id": str(d.id), "name": d.name, "total_owed": float(d.total_owed or 0),
            "payment_score": d.payment_score} for d in res.scalars().all()]

    # Tasa recuperacion mes: cobrado / (cobrado + vencido mes)
    recovery_rate = round(paid_mtd / (paid_mtd + total_owed) * 100, 2) if (paid_mtd + total_owed) else 0

    return {
        "total_owed": round(total_owed, 2),
        "paid_mtd": round(paid_mtd, 2),
        "dso_days": round(dso, 1),
        "aging": buckets,
        "top_debtors": top,
        "recovery_rate_pct": recovery_rate,
        "as_of": now.isoformat(),
    }


# ═══════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════
@router.get("/exports/invoices.xlsx")
async def export_invoices(db: AsyncSession = Depends(tenant_db)):
    res = await db.execute(select(Invoice, Debtor).join(Debtor, Debtor.id == Invoice.debtor_id))
    rows = []
    for inv, deb in res.all():
        rows.append({
            "folio": inv.folio, "serie": inv.serie, "cfdi_uuid": inv.cfdi_uuid,
            "debtor_name": deb.name, "debtor_rfc": deb.rfc,
            "issued_at": inv.issued_at, "due_at": inv.due_at,
            "total": inv.total, "paid_amount": inv.paid_amount, "status": inv.status,
        })
    data = invoices_to_xlsx(rows)
    return StreamingResponse(io.BytesIO(data),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=porcobrar-invoices.xlsx"})


@router.get("/exports/debtors.xlsx")
async def export_debtors(db: AsyncSession = Depends(tenant_db)):
    res = await db.execute(select(Debtor))
    rows = [{
        "name": d.name, "rfc": d.rfc, "email": d.email, "phone": d.phone,
        "total_owed": d.total_owed, "overdue_days_avg": d.overdue_days_avg,
        "payment_score": d.payment_score, "last_payment_at": d.last_payment_at,
    } for d in res.scalars().all()]
    data = debtors_to_xlsx(rows)
    return StreamingResponse(io.BytesIO(data),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=porcobrar-debtors.xlsx"})


@router.get("/exports/cartera-antiguedad.xlsx")
async def export_aging(db: AsyncSession = Depends(tenant_db)):
    data_dash = await dashboard(db)  # type: ignore
    data = aging_to_xlsx(data_dash["aging"])
    return StreamingResponse(io.BytesIO(data),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=porcobrar-cartera.xlsx"})


# ═══════════════════════════════════════════════
# DEMO SEED
# ═══════════════════════════════════════════════
@router.post("/demo/seed")
async def demo_seed(industry: str = Query("servicios"), db: AsyncSession = Depends(raw_db)):
    await seed_plans(db)
    await db.commit()
    try:
        result = await seed_industry(db, industry)
    except ValueError as e:
        raise HTTPException(400, str(e))
    await db.commit()
    return {"ok": True, **result}


# ═══════════════════════════════════════════════
# PUBLIC PAY PAGE (sin tenant header, resuelve por token)
# ═══════════════════════════════════════════════
@router.get("/public/pay/{token}")
async def public_pay_info(token: str, db: AsyncSession = Depends(raw_db)):
    res = await db.execute(select(PaymentLink).where(PaymentLink.token == token))
    link = res.scalars().first()
    if not link:
        raise HTTPException(404, "link no existe")
    if link.expires_at and link.expires_at < datetime.utcnow():
        raise HTTPException(410, "link expirado")
    # set tenant context para esta sesion
    from sqlalchemy import text as sqltext
    await db.execute(sqltext("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=str(link.tenant_id)))
    inv = await db.get(Invoice, link.invoice_id)
    tenant = await db.get(Tenant, link.tenant_id)
    debtor = await db.get(Debtor, inv.debtor_id) if inv else None
    saldo = float((inv.total or 0) - (inv.paid_amount or 0)) if inv else 0
    return {
        "token": token,
        "tenant": {
            "name": tenant.name if tenant else "",
            "rfc": tenant.rfc if tenant else "",
            "razon_social": tenant.razon_social if tenant else "",
            "brand_color": tenant.brand_color if tenant else "#10b981",
            "logo_url": tenant.logo_url if tenant else None,
        },
        "invoice": {
            "id": str(inv.id) if inv else None,
            "serie": inv.serie if inv else None,
            "folio": inv.folio if inv else None,
            "cfdi_uuid": inv.cfdi_uuid if inv else None,
            "issued_at": inv.issued_at.isoformat() if inv and inv.issued_at else None,
            "due_at": inv.due_at.isoformat() if inv and inv.due_at else None,
            "total": float(inv.total or 0) if inv else 0,
            "paid_amount": float(inv.paid_amount or 0) if inv else 0,
            "balance": saldo,
            "currency": inv.currency if inv else "MXN",
            "status": inv.status if inv else None,
        },
        "debtor": {
            "name": debtor.name if debtor else "",
            "rfc": debtor.rfc if debtor else "",
        },
    }


@router.post("/public/pay/{token}/checkout")
async def public_pay_checkout(token: str, provider: str = Query("stripe"), db: AsyncSession = Depends(raw_db)):
    res = await db.execute(select(PaymentLink).where(PaymentLink.token == token))
    link = res.scalars().first()
    if not link:
        raise HTTPException(404, "link no existe")
    from sqlalchemy import text as sqltext
    await db.execute(sqltext("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=str(link.tenant_id)))
    inv = await db.get(Invoice, link.invoice_id)
    debtor = await db.get(Debtor, inv.debtor_id) if inv else None
    amount = (inv.total or Decimal("0")) - (inv.paid_amount or Decimal("0"))
    ref = f"pl-{token[:8]}"
    desc = f"Pago factura {inv.serie or ''}{inv.folio or ''}"
    if provider == "stripe":
        url, sid = create_stripe_checkout(amount_mxn=amount, description=desc, reference=ref,
                                          customer_email=debtor.email if debtor else None)
        link.stripe_session_id = sid
        await db.commit()
        return {"url": url, "provider": "stripe"}
    url, oid = create_conekta_checkout(amount_mxn=amount, description=desc, reference=ref,
                                        customer_name=debtor.name if debtor else None,
                                        customer_email=debtor.email if debtor else None,
                                        customer_phone=debtor.phone if debtor else None)
    link.conekta_order_id = oid
    await db.commit()
    return {"url": url, "provider": "conekta"}


# ═══════════════════════════════════════════════
# DEMO CHECKOUT (fallback cuando no hay Stripe/Conekta keys)
# ═══════════════════════════════════════════════
@router.get("/billing/demo-checkout/{provider}", response_class=HTMLResponse)
async def demo_checkout(provider: str, ref: str = "", amount: str = "0"):
    html = f"""<!doctype html><html><head><meta charset='utf-8'>
    <title>Checkout demo {provider}</title>
    <style>
      body {{ font-family: -apple-system, system-ui, sans-serif; background:#0a0a0b; color:#fafafa;
             display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; }}
      .card {{ background:#111113; border:1px solid #2a2a2e; border-radius:16px; padding:40px; max-width:420px; width:90%; }}
      h1 {{ margin:0 0 8px 0; font-size:22px; color:#10b981; }}
      .amt {{ font-size:36px; font-weight:700; margin:16px 0; }}
      .prov {{ color:#a1a1aa; font-size:14px; text-transform:uppercase; letter-spacing:1px; }}
      button {{ background:#10b981; color:#0a0a0b; border:0; padding:14px 24px; border-radius:10px; font-weight:700;
               cursor:pointer; width:100%; font-size:16px; }}
    </style></head><body>
    <div class='card'>
      <div class='prov'>{provider} · modo demo</div>
      <h1>Checkout PorCobrar</h1>
      <div class='amt'>$ {amount} MXN</div>
      <p style='color:#a1a1aa'>Referencia: <b style='color:#fafafa'>{ref}</b></p>
      <button onclick="alert('Pago demo exitoso. En produccion redirige a {provider}.')">Simular pago</button>
    </div>
    </body></html>"""
    return HTMLResponse(html)
