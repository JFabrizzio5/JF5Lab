"""NotaMX - WhatsApp + Cobros Stripe/Conekta + CFDI 4.0.

Multi-tenant por tenant_id + RLS Postgres (policies en migration 0001).
Verticales demo: freelance, consultorio, abogados, agencia.
"""
from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Integer, Numeric, ForeignKey, Text,
    UniqueConstraint, Index, Date,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from config.database import Base


def uuid_pk():
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def tenant_fk():
    return Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)


# ───────────── SaaS Plans (catalog, global) ─────────────
class Plan(Base):
    __tablename__ = "plans"
    id = Column(String(32), primary_key=True)
    name = Column(String(80), nullable=False)
    price_mxn = Column(Numeric(10, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="MXN")
    max_notes_month = Column(Integer, nullable=False, default=5)
    max_customers = Column(Integer, nullable=False, default=50)
    has_whatsapp = Column(Boolean, default=False)
    has_cfdi = Column(Boolean, default=False)
    has_branding = Column(Boolean, default=False)
    has_api = Column(Boolean, default=False)
    description = Column(Text)
    featured = Column(Boolean, default=False)
    stripe_price_id = Column(String(120))
    conekta_plan_id = Column(String(120))


# ───────────── Tenant ─────────────
class Tenant(Base):
    __tablename__ = "tenants"
    id = uuid_pk()
    name = Column(String(160), nullable=False)
    slug = Column(String(80), unique=True, index=True)
    industry = Column(String(40), nullable=False, default="freelance")
    country = Column(String(2), default="MX")
    rfc = Column(String(13))
    razon_social = Column(String(240))
    regimen_fiscal = Column(String(10))  # codigo SAT (601, 612, 621, 626, etc)
    codigo_postal = Column(String(5))
    contact_email = Column(String(160))
    contact_phone = Column(String(40))
    whatsapp_number = Column(String(40))
    logo_url = Column(String(512))
    brand_color = Column(String(20), default="#10b981")
    locale = Column(String(10), default="es-MX")
    timezone = Column(String(40), default="America/Mexico_City")
    stripe_account = Column(String(120))
    conekta_account = Column(String(120))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TenantPlan(Base):
    __tablename__ = "tenant_plans"
    id = uuid_pk()
    tenant_id = tenant_fk()
    plan_id = Column(String(32), ForeignKey("plans.id"), nullable=False)
    status = Column(String(20), default="trialing")
    started_at = Column(DateTime, default=datetime.utcnow)
    trial_end = Column(DateTime)
    current_period_end = Column(DateTime)
    stripe_subscription_id = Column(String(120))
    conekta_subscription_id = Column(String(120))
    provider = Column(String(20))


# ───────────── Customers ─────────────
class Customer(Base):
    __tablename__ = "customers"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(200), nullable=False)
    rfc = Column(String(13))
    email = Column(String(160), index=True)
    phone = Column(String(40))
    whatsapp = Column(String(40))
    uso_cfdi = Column(String(10), default="G03")  # G01 G03 P01 etc
    regimen_fiscal = Column(String(10))
    codigo_postal = Column(String(5))
    razon_social = Column(String(240))
    address = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    metadata_json = Column("metadata", JSONB, default=dict)
    __table_args__ = (
        Index("ix_customer_tenant_name", "tenant_id", "name"),
    )


# ───────────── Products / Services ─────────────
class Product(Base):
    __tablename__ = "products"
    id = uuid_pk()
    tenant_id = tenant_fk()
    sku = Column(String(60))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price_mxn = Column(Numeric(10, 2), nullable=False, default=0)
    unit = Column(String(20), default="servicio")  # servicio | hora | pieza | paquete | mes
    tax_rate = Column(Numeric(5, 4), default=0.16)  # 0.16 IVA MX
    sat_product_key = Column(String(20))  # c_ClaveProdServ
    sat_unit_key = Column(String(10))     # c_ClaveUnidad
    active = Column(Boolean, default=True)
    __table_args__ = (
        Index("ix_product_tenant_name", "tenant_id", "name"),
    )


# ───────────── Notes (cotizacion/recibo) ─────────────
class Note(Base):
    __tablename__ = "notes"
    id = uuid_pk()
    tenant_id = tenant_fk()
    number = Column(String(40))  # folio visible (NT-0001)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"))
    status = Column(String(20), default="draft")  # draft|sent|paid|canceled|expired
    channel = Column(String(20), default="link")  # whatsapp|email|link
    public_token = Column(String(64), unique=True, index=True, default=lambda: uuid.uuid4().hex)
    currency = Column(String(3), default="MXN")
    subtotal = Column(Numeric(12, 2), default=0)
    tax_total = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), default=0)
    discount = Column(Numeric(12, 2), default=0)
    valid_until = Column(Date)
    notes = Column(Text)
    viewed_at = Column(DateTime)
    sent_at = Column(DateTime)
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column("metadata", JSONB, default=dict)


class NoteItem(Base):
    __tablename__ = "note_items"
    id = uuid_pk()
    tenant_id = tenant_fk()
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"))
    description = Column(String(240), nullable=False)
    qty = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(10, 2), default=0)
    discount = Column(Numeric(10, 2), default=0)
    tax_rate = Column(Numeric(5, 4), default=0.16)
    subtotal = Column(Numeric(12, 2), default=0)
    tax = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), default=0)
    sort_order = Column(Integer, default=0)


# ───────────── Payments ─────────────
class Payment(Base):
    __tablename__ = "payments"
    id = uuid_pk()
    tenant_id = tenant_fk()
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.id", ondelete="SET NULL"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"))
    amount_mxn = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="MXN")
    provider = Column(String(20))  # stripe|conekta|manual|cash|transfer
    provider_id = Column(String(160), index=True)
    status = Column(String(20), default="pending")  # pending|succeeded|failed|refunded
    method = Column(String(40))  # card|oxxo|spei|cash
    receipt_url = Column(String(512))
    description = Column(String(240))
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column("metadata", JSONB, default=dict)


# ───────────── CFDI 4.0 (SAT) ─────────────
class CfdiDocument(Base):
    __tablename__ = "cfdi_documents"
    id = uuid_pk()
    tenant_id = tenant_fk()
    related_note_id = Column(UUID(as_uuid=True), ForeignKey("notes.id", ondelete="SET NULL"))
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="SET NULL"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"))
    uuid_sat = Column(String(40))  # UUID SAT (folio fiscal)
    serie = Column(String(10), default="A")
    folio = Column(String(20))
    xml_url = Column(String(512))
    pdf_url = Column(String(512))
    status = Column(String(20), default="pending")  # pending|issued|canceled|error
    total = Column(Numeric(12, 2))
    uso_cfdi = Column(String(10))
    metodo_pago = Column(String(10), default="PUE")  # PUE | PPD
    forma_pago = Column(String(10), default="03")    # 01 efectivo, 03 transferencia, 04 tarjeta, etc
    error_message = Column(Text)
    issued_at = Column(DateTime)
    canceled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


# ───────────── WhatsApp ─────────────
class WhatsappTemplate(Base):
    __tablename__ = "whatsapp_templates"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(80), nullable=False)
    body = Column(Text, nullable=False)
    variables = Column(JSONB, default=list)
    category = Column(String(40), default="nota")  # nota|cobro|recordatorio
    active = Column(Boolean, default=True)


class WhatsappMessage(Base):
    __tablename__ = "whatsapp_messages"
    id = uuid_pk()
    tenant_id = tenant_fk()
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.id", ondelete="SET NULL"))
    to_phone = Column(String(40), nullable=False)
    template = Column(String(80))
    body = Column(Text)
    status = Column(String(20), default="queued")  # queued|sent|delivered|read|failed
    provider_message_id = Column(String(120))
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
