"""AgendaPro — dominio reservas B2C con pago anticipado.

Multi-tenant RLS (policies en 0001). Verticales: barber | clinic | vet | coach | beauty | pet | tattoo.
"""
from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Integer, Numeric, ForeignKey, Text,
    UniqueConstraint, Index, Date, Time,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from config.database import Base


def uuid_pk():
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def tenant_fk():
    return Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"),
                  nullable=False, index=True)


# ─────────────────────────────────────────────
# SaaS Plans (global)
# ─────────────────────────────────────────────
class Plan(Base):
    __tablename__ = "plans"
    id = Column(String(32), primary_key=True)
    name = Column(String(80), nullable=False)
    price_mxn = Column(Numeric(10, 2), nullable=False, default=0)
    currency = Column(String(3), default="MXN")
    max_appointments_mo = Column(Integer, default=30)
    max_staff = Column(Integer, default=1)
    has_prepay = Column(Boolean, default=False)
    has_whatsapp = Column(Boolean, default=False)
    has_custom_brand = Column(Boolean, default=False)
    has_google_review = Column(Boolean, default=False)
    description = Column(Text)
    featured = Column(Boolean, default=False)
    stripe_price_id = Column(String(120))
    conekta_plan_id = Column(String(120))


# ─────────────────────────────────────────────
# Tenant (negocio)
# ─────────────────────────────────────────────
class Tenant(Base):
    __tablename__ = "tenants"
    id = uuid_pk()
    name = Column(String(160), nullable=False)
    slug = Column(String(80), unique=True, index=True, nullable=False)
    industry = Column(String(40), default="barber")
    country = Column(String(2), default="MX")
    city = Column(String(80))
    timezone = Column(String(40), default="America/Mexico_City")
    brand_color = Column(String(20), default="#1e3a8a")
    logo_url = Column(String(512))
    instagram = Column(String(80))
    google_place_id = Column(String(120))
    rfc = Column(String(13))
    contact_email = Column(String(160))
    contact_phone = Column(String(40))
    tagline = Column(String(240))
    about = Column(Text)
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
# Staff (empleados que dan servicio)
# ─────────────────────────────────────────────
class Staff(Base):
    __tablename__ = "staff"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(160), nullable=False)
    email = Column(String(160))
    phone = Column(String(40))
    role = Column(String(40), default="professional")  # owner | manager | professional | assistant
    photo_url = Column(String(512))
    color = Column(String(20), default="#1e3a8a")
    bio = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────────
# Services (catálogo)
# ─────────────────────────────────────────────
class Service(Base):
    __tablename__ = "services"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(160), nullable=False)
    description = Column(Text)
    category = Column(String(60))
    duration_minutes = Column(Integer, default=30)
    buffer_minutes = Column(Integer, default=0)
    price_mxn = Column(Numeric(10, 2), nullable=False, default=0)
    deposit_mxn = Column(Numeric(10, 2), default=0)
    requires_prepay = Column(Boolean, default=False)
    color = Column(String(20), default="#1e3a8a")
    staff_ids = Column(ARRAY(UUID(as_uuid=True)), default=list)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────────
# Availability
# ─────────────────────────────────────────────
class AvailabilityRule(Base):
    """Horario recurrente por staff + día de la semana."""
    __tablename__ = "availability_rules"
    id = uuid_pk()
    tenant_id = tenant_fk()
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True)
    weekday = Column(Integer, nullable=False)  # 0=Mon … 6=Sun
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    active = Column(Boolean, default=True)


class AvailabilityException(Base):
    """Excepción puntual (bloqueo o horario extra)."""
    __tablename__ = "availability_exceptions"
    id = uuid_pk()
    tenant_id = tenant_fk()
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    kind = Column(String(20), default="blocked")  # blocked | extra
    start_time = Column(Time)
    end_time = Column(Time)
    note = Column(String(240))


# ─────────────────────────────────────────────
# Customers
# ─────────────────────────────────────────────
class Customer(Base):
    __tablename__ = "customers"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(160), nullable=False)
    phone = Column(String(40), index=True)
    email = Column(String(160), index=True)
    whatsapp_optin = Column(Boolean, default=True)
    notes = Column(Text)
    total_visits = Column(Integer, default=0)
    no_show_count = Column(Integer, default=0)
    tags = Column(ARRAY(String), default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index("ix_customer_tenant_phone", "tenant_id", "phone"),
    )


# ─────────────────────────────────────────────
# Appointments
# ─────────────────────────────────────────────
class Appointment(Base):
    __tablename__ = "appointments"
    id = uuid_pk()
    tenant_id = tenant_fk()
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"))
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="SET NULL"), index=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id", ondelete="SET NULL"))
    starts_at = Column(DateTime, nullable=False, index=True)
    ends_at = Column(DateTime, nullable=False)
    status = Column(String(30), default="pending_payment")
    # pending_payment | confirmed | completed | no_show | canceled | rescheduled
    notes = Column(Text)
    deposit_paid = Column(Boolean, default=False)
    total = Column(Numeric(10, 2), default=0)
    deposit = Column(Numeric(10, 2), default=0)
    source = Column(String(20), default="public")  # public | manual | imported
    google_event_id = Column(String(120))
    cancel_reason = Column(String(240))
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index("ix_appt_tenant_staff_starts", "tenant_id", "staff_id", "starts_at"),
    )


# ─────────────────────────────────────────────
# Payments
# ─────────────────────────────────────────────
class Payment(Base):
    __tablename__ = "payments"
    id = uuid_pk()
    tenant_id = tenant_fk()
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id", ondelete="SET NULL"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"))
    amount_mxn = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="MXN")
    provider = Column(String(20))  # stripe | conekta | cash | transfer
    provider_id = Column(String(160), index=True)
    status = Column(String(20), default="pending")  # pending | succeeded | failed | refunded
    method = Column(String(40))  # card | oxxo | spei | cash
    receipt_url = Column(String(512))
    description = Column(String(240))
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column("metadata", JSONB, default=dict)


# ─────────────────────────────────────────────
# Reminders
# ─────────────────────────────────────────────
class Reminder(Base):
    __tablename__ = "reminders"
    id = uuid_pk()
    tenant_id = tenant_fk()
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String(20), default="whatsapp")  # whatsapp | email | sms
    send_at = Column(DateTime, nullable=False)
    sent_at = Column(DateTime)
    status = Column(String(20), default="scheduled")  # scheduled | sent | failed
    payload = Column(JSONB, default=dict)


# ─────────────────────────────────────────────
# Reviews
# ─────────────────────────────────────────────
class Review(Base):
    __tablename__ = "reviews"
    id = uuid_pk()
    tenant_id = tenant_fk()
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"))
    rating = Column(Integer, default=5)
    comment = Column(Text)
    public = Column(Boolean, default=True)
    google_review_requested = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
