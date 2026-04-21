"""PorCobrar — Dominio cobranza B2B.

Multi-tenant por `tenant_id` + RLS Postgres (policies en migracion 0001).
"""
from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Integer, Numeric, ForeignKey, Text,
    Index, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from config.database import Base


def uuid_pk():
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def tenant_fk():
    return Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)


# ─────────────────────────────────────────────
# Plans SaaS globales
# ─────────────────────────────────────────────
class Plan(Base):
    __tablename__ = "plans"
    id = Column(String(32), primary_key=True)
    name = Column(String(80), nullable=False)
    price_mxn = Column(Numeric(10, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="MXN")
    max_invoices_month = Column(Integer, nullable=False, default=20)
    has_whatsapp = Column(Boolean, default=False)
    has_ai_scoring = Column(Boolean, default=False)
    has_cfdi_parser = Column(Boolean, default=True)
    has_custom_brand = Column(Boolean, default=False)
    description = Column(Text)
    featured = Column(Boolean, default=False)
    stripe_price_id = Column(String(120))
    conekta_plan_id = Column(String(120))


class Tenant(Base):
    __tablename__ = "tenants"
    id = uuid_pk()
    name = Column(String(160), nullable=False)
    slug = Column(String(80), unique=True, index=True)
    rfc = Column(String(13))
    razon_social = Column(String(240))
    industry = Column(String(40), default="servicios")  # servicios|manufactura|comercio|legal|other
    country = Column(String(2), default="MX")
    contact_email = Column(String(160))
    contact_phone = Column(String(40))
    logo_url = Column(String(512))
    brand_color = Column(String(20), default="#10b981")
    locale = Column(String(10), default="es-MX")
    timezone = Column(String(40), default="America/Mexico_City")
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


# ─────────────────────────────────────────────
# Deudores
# ─────────────────────────────────────────────
class Debtor(Base):
    __tablename__ = "debtors"
    id = uuid_pk()
    tenant_id = tenant_fk()
    rfc = Column(String(13), index=True)
    name = Column(String(240), nullable=False)
    email = Column(String(160))
    phone = Column(String(40))
    whatsapp = Column(String(40))
    total_owed = Column(Numeric(12, 2), default=0)
    overdue_days_avg = Column(Integer, default=0)
    payment_score = Column(Integer, default=50)  # 0-100
    last_payment_at = Column(DateTime)
    notes = Column(Text)
    metadata_json = Column("metadata", JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index("ix_debtor_tenant_name", "tenant_id", "name"),
    )


class Invoice(Base):
    __tablename__ = "invoices"
    id = uuid_pk()
    tenant_id = tenant_fk()
    debtor_id = Column(UUID(as_uuid=True), ForeignKey("debtors.id", ondelete="CASCADE"), nullable=False, index=True)
    cfdi_uuid = Column(String(80), index=True)
    serie = Column(String(20))
    folio = Column(String(40))
    issued_at = Column(DateTime, default=datetime.utcnow)
    due_at = Column(DateTime, nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="MXN")
    paid_amount = Column(Numeric(12, 2), default=0)
    status = Column(String(20), default="pending")  # pending|partial|paid|overdue|written_off|disputed
    xml_url = Column(String(512))
    pdf_url = Column(String(512))
    source = Column(String(20), default="manual")  # cfdi_upload|manual|api
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_invoice_tenant_status", "tenant_id", "status"),
        Index("ix_invoice_tenant_due", "tenant_id", "due_at"),
    )


# ─────────────────────────────────────────────
# Dunning (cobranza escalada)
# ─────────────────────────────────────────────
class DunningFlow(Base):
    __tablename__ = "dunning_flows"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(120), nullable=False)
    description = Column(Text)
    steps = Column(JSONB, default=list)  # [{day:0, channel:"email", template_id:"..."}]
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DunningTemplate(Base):
    __tablename__ = "dunning_templates"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(120), nullable=False)
    channel = Column(String(20), nullable=False)  # email|whatsapp|sms
    subject = Column(String(240))
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DunningRun(Base):
    __tablename__ = "dunning_runs"
    id = uuid_pk()
    tenant_id = tenant_fk()
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    flow_id = Column(UUID(as_uuid=True), ForeignKey("dunning_flows.id", ondelete="SET NULL"))
    step_index = Column(Integer, default=0)
    scheduled_at = Column(DateTime, nullable=False, index=True)
    executed_at = Column(DateTime)
    status = Column(String(20), default="queued")  # queued|sent|failed|skipped
    channel = Column(String(20))
    message_id = Column(String(160))
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────────
# Pagos + Payment links
# ─────────────────────────────────────────────
class Payment(Base):
    __tablename__ = "payments"
    id = uuid_pk()
    tenant_id = tenant_fk()
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="SET NULL"))
    debtor_id = Column(UUID(as_uuid=True), ForeignKey("debtors.id", ondelete="SET NULL"))
    amount_mxn = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="MXN")
    provider = Column(String(20))  # stripe|conekta|spei|cash|transfer
    provider_id = Column(String(160), index=True)
    status = Column(String(20), default="pending")  # pending|succeeded|failed|refunded
    method = Column(String(40))
    receipt_url = Column(String(512))
    description = Column(String(240))
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column("metadata", JSONB, default=dict)


class PaymentLink(Base):
    __tablename__ = "payment_links"
    id = uuid_pk()
    tenant_id = tenant_fk()
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(80), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime)
    stripe_session_id = Column(String(160))
    conekta_order_id = Column(String(160))
    created_at = Column(DateTime, default=datetime.utcnow)


class PaymentScoreEvent(Base):
    __tablename__ = "payment_score_events"
    id = uuid_pk()
    tenant_id = tenant_fk()
    debtor_id = Column(UUID(as_uuid=True), ForeignKey("debtors.id", ondelete="CASCADE"), nullable=False, index=True)
    event = Column(String(40), nullable=False)  # paid_on_time|paid_late|dispute|contact_responded|ignored
    delta = Column(Integer, default=0)
    at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)


class NoteLog(Base):
    __tablename__ = "notes_log"
    id = uuid_pk()
    tenant_id = tenant_fk()
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))
    debtor_id = Column(UUID(as_uuid=True), ForeignKey("debtors.id", ondelete="CASCADE"))
    user = Column(String(120))
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
