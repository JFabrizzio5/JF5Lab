"""Demo seed con 4 verticales: servicios, manufactura, comercio, legal."""
from __future__ import annotations
import random
import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from modules.cobranza.models.models import (
    Tenant, TenantPlan, Debtor, Invoice, DunningFlow, DunningTemplate,
)


INDUSTRY_CONFIG = {
    "servicios": {
        "name": "Agencia Creativa Ejemplo",
        "razon_social": "AGENCIA CREATIVA EJEMPLO SA DE CV",
        "brand_color": "#10b981",
        "debtors": 15,
        "inv_per": (2, 5),
        "amount": (35000, 180000),
        "due_days": 30,
        "tenant_rfc": "ACE240101AB1",
    },
    "manufactura": {
        "name": "Metalurgica Norte SA",
        "razon_social": "METALURGICA DEL NORTE SA DE CV",
        "brand_color": "#f59e0b",
        "debtors": 10,
        "inv_per": (3, 6),
        "amount": (50000, 2000000),
        "due_days": 60,
        "tenant_rfc": "MEN230101XY2",
    },
    "comercio": {
        "name": "Distribuidora Ejemplo",
        "razon_social": "DISTRIBUIDORA EJEMPLO SA DE CV",
        "brand_color": "#3b82f6",
        "debtors": 20,
        "inv_per": (5, 12),
        "amount": (5000, 50000),
        "due_days": 30,
        "tenant_rfc": "DIE220101ZZ3",
    },
    "legal": {
        "name": "Despacho Juridico Ejemplo",
        "razon_social": "DESPACHO JURIDICO EJEMPLO SC",
        "brand_color": "#6366f1",
        "debtors": 12,
        "inv_per": (2, 4),
        "amount": (20000, 500000),
        "due_days": 15,
        "tenant_rfc": "DJE210101LL4",
    },
}

FIRST_NAMES = ["Constructora", "Grupo", "Corporativo", "Servicios", "Industrias", "Promotora", "Inmobiliaria", "Soluciones"]
LAST_NAMES  = ["Aguila", "Monterrey", "Valle", "Pacifico", "Atlante", "Cedral", "Cumbres", "Veracruz"]


def _random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)} SA de CV"


def _random_rfc():
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    return f"{''.join(random.choices(letters,k=3))}{random.randint(10,25):02d}{random.randint(1,12):02d}{random.randint(1,28):02d}{''.join(random.choices(letters+'0123456789',k=3))}"


async def seed_industry(db: AsyncSession, industry: str) -> dict:
    from sqlalchemy import text as sqltext
    cfg = INDUSTRY_CONFIG.get(industry)
    if not cfg:
        raise ValueError(f"industry invalida: {industry}. Usa servicios|manufactura|comercio|legal.")

    # Tenant (tabla sin RLS)
    slug = f"demo-{industry}-{secrets.token_hex(3)}"
    tenant = Tenant(
        name=cfg["name"],
        slug=slug,
        rfc=cfg["tenant_rfc"],
        razon_social=cfg["razon_social"],
        industry=industry,
        contact_email=f"contacto@{slug}.mx",
        brand_color=cfg["brand_color"],
    )
    db.add(tenant)
    await db.flush()

    # Activa contexto RLS para esta sesion y todo lo que viene.
    await db.execute(sqltext("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=str(tenant.id)))

    tp = TenantPlan(tenant_id=tenant.id, plan_id="basic", status="active")
    db.add(tp)

    # Templates + Flow estandar 3 toques
    tmpl_email_0 = DunningTemplate(
        tenant_id=tenant.id, name="Recordatorio dia 0", channel="email",
        subject="Recordatorio: factura {{invoice.folio}}",
        body="Estimado {{debtor.name}}, su factura {{invoice.folio}} por ${{invoice.total}} vence hoy. Pague aqui: {{invoice.pay_link}}",
    )
    tmpl_wa_7 = DunningTemplate(
        tenant_id=tenant.id, name="Seguimiento WhatsApp 7d", channel="whatsapp",
        subject=None,
        body="Hola {{debtor.name}}, la factura {{invoice.folio}} lleva 7 dias vencida. Liquide en: {{invoice.pay_link}}",
    )
    tmpl_sms_15 = DunningTemplate(
        tenant_id=tenant.id, name="Alerta SMS 15d", channel="sms",
        subject=None,
        body="URGENTE: factura {{invoice.folio}} 15 dias vencida. Pague {{invoice.pay_link}} o conteste para acuerdo.",
    )
    db.add_all([tmpl_email_0, tmpl_wa_7, tmpl_sms_15])
    await db.flush()

    flow = DunningFlow(
        tenant_id=tenant.id,
        name="Estandar 3 toques",
        description="Email al vencer, WhatsApp a 7d, SMS a 15d",
        steps=[
            {"day": 0, "channel": "email", "template_id": str(tmpl_email_0.id)},
            {"day": 7, "channel": "whatsapp", "template_id": str(tmpl_wa_7.id)},
            {"day": 15, "channel": "sms", "template_id": str(tmpl_sms_15.id)},
        ],
    )
    db.add(flow)
    await db.flush()

    # Deudores + Facturas
    now = datetime.utcnow()
    stat_mix = ["pending", "pending", "partial", "overdue", "overdue", "paid"]

    debtors_created = 0
    invoices_created = 0
    for _ in range(cfg["debtors"]):
        d_name = _random_name()
        d_rfc = _random_rfc()
        deb = Debtor(
            tenant_id=tenant.id,
            rfc=d_rfc,
            name=d_name,
            email=f"pagos@{d_name.split()[1].lower()}.mx",
            phone=f"+52{random.randint(5500000000, 5599999999)}",
            whatsapp=f"+52{random.randint(5500000000, 5599999999)}",
            total_owed=0,
            payment_score=random.randint(25, 85),
        )
        db.add(deb)
        await db.flush()
        debtors_created += 1

        n_inv = random.randint(*cfg["inv_per"])
        for _ in range(n_inv):
            amount = Decimal(str(random.randint(cfg["amount"][0], cfg["amount"][1])))
            issued = now - timedelta(days=random.randint(0, 120))
            due = issued + timedelta(days=cfg["due_days"])
            status = random.choice(stat_mix)
            paid = Decimal("0")
            if status == "paid":
                paid = amount
            elif status == "partial":
                paid = amount / 2
            if status != "paid" and due < now and (now - due).days > 0:
                status = "overdue"
            inv = Invoice(
                tenant_id=tenant.id,
                debtor_id=deb.id,
                cfdi_uuid=f"DEMO-{secrets.token_hex(12).upper()}",
                serie="A",
                folio=str(random.randint(1000, 9999)),
                issued_at=issued,
                due_at=due,
                total=amount,
                paid_amount=paid,
                status=status,
                source="manual",
            )
            db.add(inv)
            invoices_created += 1

    await db.flush()
    return {
        "tenant_id": str(tenant.id),
        "tenant_slug": slug,
        "industry": industry,
        "debtors": debtors_created,
        "invoices": invoices_created,
        "default_flow_id": str(flow.id),
    }


async def seed_plans(db: AsyncSession):
    """Semilla catalogo SaaS global de planes."""
    from sqlalchemy import select
    from modules.cobranza.models.models import Plan
    existing = (await db.execute(select(Plan))).scalars().all()
    if existing:
        return [p.id for p in existing]
    plans = [
        Plan(id="gratis",   name="Gratis",   price_mxn=0,    max_invoices_month=20,     description="Hasta 20 facturas/mes. Email solo."),
        Plan(id="basic",    name="Basic",    price_mxn=999,  max_invoices_month=100,    has_whatsapp=True, description="100 facturas/mes + WhatsApp.", featured=True),
        Plan(id="pro",      name="Pro",      price_mxn=2499, max_invoices_month=1000,   has_whatsapp=True, has_ai_scoring=True, has_custom_brand=True, description="1,000 facturas/mes + IA scoring + marca propia."),
        Plan(id="business", name="Business", price_mxn=6999, max_invoices_month=999999, has_whatsapp=True, has_ai_scoring=True, has_custom_brand=True, description="Facturas ilimitadas + integracion API + soporte."),
    ]
    db.add_all(plans)
    await db.flush()
    return [p.id for p in plans]
