from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal
from typing import Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class PlanOut(BaseModel):
    id: str
    name: str
    price_mxn: Decimal
    currency: str
    max_members: int
    max_venues: int
    max_staff: int
    has_bookings: bool
    has_payments: bool
    has_whatsapp: bool
    has_custom_brand: bool
    description: str | None = None
    featured: bool
    class Config: from_attributes = True


class TenantCreate(BaseModel):
    name: str
    industry: str = "gym"
    slug: str | None = None
    rfc: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    plan_id: str | None = "free"


class TenantOut(BaseModel):
    id: UUID
    name: str
    slug: str | None = None
    industry: str
    brand_color: str
    locale: str
    timezone: str
    active: bool
    class Config: from_attributes = True


class VenueCreate(BaseModel):
    name: str
    address: str | None = None
    city: str | None = None
    capacity: int = 0


class VenueOut(VenueCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


class MemberCreate(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthdate: date | None = None
    gender: str | None = None
    code: str | None = None
    notes: str | None = None


class MemberOut(BaseModel):
    id: UUID
    code: str
    first_name: str
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    photo_url: str | None = None
    joined_at: datetime
    active: bool
    class Config: from_attributes = True


class MembershipPlanCreate(BaseModel):
    name: str
    price_mxn: Decimal
    billing_interval: str = "month"
    visits_included: int | None = None
    duration_days: int | None = None
    description: str | None = None
    color: str = "#7c3aed"
    perks: list[str] = Field(default_factory=list)


class MembershipPlanOut(MembershipPlanCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


class MembershipCreate(BaseModel):
    member_id: UUID
    membership_plan_id: UUID
    auto_renew: bool = False


class MembershipOut(BaseModel):
    id: UUID
    member_id: UUID
    membership_plan_id: UUID | None = None
    status: str
    started_at: datetime
    expires_at: datetime | None = None
    visits_remaining: int | None = None
    auto_renew: bool
    class Config: from_attributes = True


class InstructorCreate(BaseModel):
    code: str
    name: str
    email: EmailStr | None = None
    specialty: str | None = None
    bio: str | None = None


class InstructorOut(InstructorCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


class ClassTemplateCreate(BaseModel):
    name: str
    description: str | None = None
    duration_minutes: int = 60
    capacity: int = 20
    color: str = "#7c3aed"
    kind: str | None = None


class ClassTemplateOut(ClassTemplateCreate):
    id: UUID
    class Config: from_attributes = True


class ClassSessionCreate(BaseModel):
    template_id: UUID | None = None
    instructor_id: UUID | None = None
    room_id: UUID | None = None
    name: str | None = None
    starts_at: datetime
    ends_at: datetime
    capacity: int = 20


class ClassSessionOut(BaseModel):
    id: UUID
    template_id: UUID | None = None
    instructor_id: UUID | None = None
    room_id: UUID | None = None
    name: str | None = None
    starts_at: datetime
    ends_at: datetime
    capacity: int
    booked_count: int
    status: str
    class Config: from_attributes = True


class BookingCreate(BaseModel):
    session_id: UUID
    member_id: UUID


class BookingOut(BaseModel):
    id: UUID
    session_id: UUID
    member_id: UUID
    status: str
    booked_at: datetime
    class Config: from_attributes = True


class CheckInPunch(BaseModel):
    code: str  # QR code del miembro
    session_id: UUID | None = None
    venue_id: UUID | None = None
    method: str = "QR"


class CheckInOut(BaseModel):
    id: UUID
    member_id: UUID
    at: datetime
    kind: str
    method: str
    class Config: from_attributes = True


class CheckoutRequest(BaseModel):
    """Inicia checkout Stripe o Conekta para un plan SaaS o una membresía."""
    plan_id: str | None = None          # plan SaaS (billing/checkout)
    membership_plan_id: UUID | None = None  # plan interno (cobro miembro)
    member_id: UUID | None = None
    provider: str = "stripe"            # stripe | conekta
    success_url: str | None = None
    cancel_url: str | None = None


class CheckoutResponse(BaseModel):
    provider: str
    checkout_url: str
    session_id: str | None = None
    demo: bool = False


class PaymentOut(BaseModel):
    id: UUID
    member_id: UUID | None = None
    amount_mxn: Decimal
    currency: str
    provider: str | None = None
    status: str
    method: str | None = None
    description: str | None = None
    paid_at: datetime | None = None
    created_at: datetime
    class Config: from_attributes = True


class DashboardKPIs(BaseModel):
    total_members: int
    active_memberships: int
    check_ins_today: int
    bookings_today: int
    revenue_mtd_mxn: Decimal
    churn_last_30d: int
    new_members_last_7d: int
    upcoming_classes: list[dict[str, Any]]
    recent_check_ins: list[dict[str, Any]]
