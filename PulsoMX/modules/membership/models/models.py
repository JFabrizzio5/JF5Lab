"""PulsoMX — Dominio membresías + clases + cobros.

Multi-tenant por `tenant_id` + RLS Postgres (policies en migración 0001).
Verticales: gym, yoga, coworking, dojo, dance, spa.
"""
from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Integer, Numeric, ForeignKey, Text,
    UniqueConstraint, Index, Date, Time,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from config.database import Base


def uuid_pk():
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def tenant_fk():
    return Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)


# ─────────────────────────────────────────────
# Plans catálogo SaaS (global)
# ─────────────────────────────────────────────
class Plan(Base):
    __tablename__ = "plans"
    id = Column(String(32), primary_key=True)
    name = Column(String(80), nullable=False)
    price_mxn = Column(Numeric(10, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="MXN")
    max_members = Column(Integer, nullable=False, default=50)
    max_venues = Column(Integer, nullable=False, default=1)
    max_staff = Column(Integer, nullable=False, default=3)
    has_bookings = Column(Boolean, default=True)
    has_payments = Column(Boolean, default=False)
    has_whatsapp = Column(Boolean, default=False)
    has_custom_brand = Column(Boolean, default=False)
    description = Column(Text)
    featured = Column(Boolean, default=False)
    stripe_price_id = Column(String(120))  # opcional si usas Stripe real
    conekta_plan_id = Column(String(120))  # opcional si usas Conekta real


# ─────────────────────────────────────────────
# Tenant (un club/gym/estudio)
# ─────────────────────────────────────────────
class Tenant(Base):
    __tablename__ = "tenants"
    id = uuid_pk()
    name = Column(String(160), nullable=False)
    slug = Column(String(80), unique=True, index=True)
    industry = Column(String(40), nullable=False, default="gym")  # gym|yoga|coworking|dojo|dance|spa|other
    country = Column(String(2), default="MX")
    rfc = Column(String(13))
    contact_email = Column(String(160))
    contact_phone = Column(String(40))
    logo_url = Column(String(512))
    brand_color = Column(String(20), default="#7c3aed")
    locale = Column(String(10), default="es-MX")
    timezone = Column(String(40), default="America/Mexico_City")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TenantPlan(Base):
    __tablename__ = "tenant_plans"
    id = uuid_pk()
    tenant_id = tenant_fk()
    plan_id = Column(String(32), ForeignKey("plans.id"), nullable=False)
    status = Column(String(20), default="trialing")  # trialing|active|past_due|canceled
    started_at = Column(DateTime, default=datetime.utcnow)
    trial_end = Column(DateTime)
    current_period_end = Column(DateTime)
    stripe_subscription_id = Column(String(120))
    conekta_subscription_id = Column(String(120))
    provider = Column(String(20))  # stripe | conekta | manual


# ─────────────────────────────────────────────
# Venues / Rooms
# ─────────────────────────────────────────────
class Venue(Base):
    __tablename__ = "venues"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(160), nullable=False)
    address = Column(String(320))
    city = Column(String(80))
    capacity = Column(Integer, default=0)
    active = Column(Boolean, default=True)


class Room(Base):
    __tablename__ = "rooms"
    id = uuid_pk()
    tenant_id = tenant_fk()
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(120), nullable=False)
    capacity = Column(Integer, default=0)
    kind = Column(String(40), default="general")  # floor, mat, cycling, reformer, open_space


# ─────────────────────────────────────────────
# Members + Memberships
# ─────────────────────────────────────────────
class Member(Base):
    __tablename__ = "members"
    id = uuid_pk()
    tenant_id = tenant_fk()
    code = Column(String(40), nullable=False)  # QR code payload
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80))
    email = Column(String(160), index=True)
    phone = Column(String(40))
    birthdate = Column(Date)
    gender = Column(String(10))
    emergency_contact = Column(String(160))
    photo_url = Column(String(512))
    joined_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    notes = Column(Text)
    metadata_json = Column("metadata", JSONB, default=dict)
    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_member_tenant_code"),
        Index("ix_member_tenant_email", "tenant_id", "email"),
    )


class MembershipPlan(Base):
    """Plan que el tenant ofrece a sus miembros (distinto del SaaS plan)."""
    __tablename__ = "membership_plans"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(120), nullable=False)
    price_mxn = Column(Numeric(10, 2), nullable=False)
    billing_interval = Column(String(20), default="month")  # month|year|one_time|visits
    visits_included = Column(Integer)  # para paquetes de N visitas
    duration_days = Column(Integer)  # vigencia tipo "30 días"
    description = Column(Text)
    active = Column(Boolean, default=True)
    color = Column(String(20), default="#7c3aed")
    perks = Column(JSONB, default=list)  # lista de strings "beneficios"


class Membership(Base):
    """Suscripción o paquete activo de un miembro."""
    __tablename__ = "memberships"
    id = uuid_pk()
    tenant_id = tenant_fk()
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    membership_plan_id = Column(UUID(as_uuid=True), ForeignKey("membership_plans.id", ondelete="SET NULL"))
    status = Column(String(20), default="active")  # active|paused|expired|canceled
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    visits_remaining = Column(Integer)
    auto_renew = Column(Boolean, default=False)
    stripe_subscription_id = Column(String(120))
    conekta_subscription_id = Column(String(120))


# ─────────────────────────────────────────────
# Instructors + Classes
# ─────────────────────────────────────────────
class Instructor(Base):
    __tablename__ = "instructors"
    id = uuid_pk()
    tenant_id = tenant_fk()
    code = Column(String(40), nullable=False)
    name = Column(String(160), nullable=False)
    email = Column(String(160))
    bio = Column(Text)
    photo_url = Column(String(512))
    specialty = Column(String(120))
    active = Column(Boolean, default=True)
    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_instr_tenant_code"),)


class ClassTemplate(Base):
    __tablename__ = "class_templates"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(160), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, default=60)
    capacity = Column(Integer, default=20)
    color = Column(String(20), default="#7c3aed")
    kind = Column(String(60))  # yoga_flow, hiit, cycling, crossfit, jiu_jitsu, pilates


class ClassSession(Base):
    __tablename__ = "class_sessions"
    id = uuid_pk()
    tenant_id = tenant_fk()
    template_id = Column(UUID(as_uuid=True), ForeignKey("class_templates.id", ondelete="SET NULL"))
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("instructors.id", ondelete="SET NULL"))
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="SET NULL"))
    name = Column(String(160))
    starts_at = Column(DateTime, nullable=False, index=True)
    ends_at = Column(DateTime, nullable=False)
    capacity = Column(Integer, default=20)
    booked_count = Column(Integer, default=0)
    status = Column(String(20), default="scheduled")  # scheduled|in_progress|completed|canceled


class Booking(Base):
    __tablename__ = "bookings"
    id = uuid_pk()
    tenant_id = tenant_fk()
    session_id = Column(UUID(as_uuid=True), ForeignKey("class_sessions.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default="booked")  # booked|attended|no_show|canceled
    booked_at = Column(DateTime, default=datetime.utcnow)
    attended_at = Column(DateTime)
    __table_args__ = (UniqueConstraint("tenant_id", "session_id", "member_id", name="uq_book_tenant_sess_mem"),)


# ─────────────────────────────────────────────
# Check-ins (asistencia al venue o clase)
# ─────────────────────────────────────────────
class CheckIn(Base):
    __tablename__ = "check_ins"
    id = uuid_pk()
    tenant_id = tenant_fk()
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id", ondelete="SET NULL"))
    session_id = Column(UUID(as_uuid=True), ForeignKey("class_sessions.id", ondelete="SET NULL"))
    at = Column(DateTime, default=datetime.utcnow, index=True)
    kind = Column(String(20), default="IN")  # IN|OUT
    method = Column(String(20), default="QR")  # QR|NFC|MANUAL|KIOSK
    metadata_json = Column("metadata", JSONB, default=dict)
    __table_args__ = (Index("ix_ci_tenant_mem_date", "tenant_id", "member_id", "at"),)


# ─────────────────────────────────────────────
# Pagos (Stripe / Conekta)
# ─────────────────────────────────────────────
class Payment(Base):
    __tablename__ = "payments"
    id = uuid_pk()
    tenant_id = tenant_fk()
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id", ondelete="SET NULL"))
    membership_id = Column(UUID(as_uuid=True), ForeignKey("memberships.id", ondelete="SET NULL"))
    amount_mxn = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="MXN")
    provider = Column(String(20))  # stripe|conekta|cash|transfer
    provider_id = Column(String(160), index=True)  # payment_intent | order_id
    status = Column(String(20), default="pending")  # pending|succeeded|failed|refunded
    method = Column(String(40))  # card|oxxo|spei|cash
    receipt_url = Column(String(512))
    description = Column(String(240))
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column("metadata", JSONB, default=dict)


class Invoice(Base):
    __tablename__ = "invoices"
    id = uuid_pk()
    tenant_id = tenant_fk()
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="SET NULL"))
    number = Column(String(40))
    cfdi_uuid = Column(String(80))
    total_mxn = Column(Numeric(10, 2))
    issued_at = Column(DateTime, default=datetime.utcnow)
    pdf_url = Column(String(512))
    xml_url = Column(String(512))


# ─────────────────────────────────────────────
# Loyalty (opcional, bonitos puntos)
# ─────────────────────────────────────────────
class LoyaltyPoint(Base):
    __tablename__ = "loyalty_points"
    id = uuid_pk()
    tenant_id = tenant_fk()
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    points = Column(Integer, default=0)
    reason = Column(String(120))
    earned_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"
    id = uuid_pk()
    tenant_id = tenant_fk()
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"))
    channel = Column(String(20))  # whatsapp|email|sms|push
    template = Column(String(80))
    payload = Column(JSONB)
    status = Column(String(20), default="queued")
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
