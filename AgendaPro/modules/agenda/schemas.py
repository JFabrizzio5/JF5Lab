from __future__ import annotations
from datetime import datetime, date, time
from decimal import Decimal
from typing import Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# ─── Plans ───
class PlanOut(BaseModel):
    id: str
    name: str
    price_mxn: Decimal
    currency: str
    max_appointments_mo: int
    max_staff: int
    has_prepay: bool
    has_whatsapp: bool
    has_custom_brand: bool
    has_google_review: bool
    description: str | None = None
    featured: bool
    class Config: from_attributes = True


# ─── Tenant ───
class TenantCreate(BaseModel):
    name: str
    industry: str = "barber"
    slug: str | None = None
    city: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    plan_id: str | None = "free"
    brand_color: str = "#1e3a8a"
    tagline: str | None = None


class TenantOut(BaseModel):
    id: UUID
    name: str
    slug: str
    industry: str
    brand_color: str
    timezone: str
    logo_url: str | None = None
    instagram: str | None = None
    tagline: str | None = None
    about: str | None = None
    active: bool
    class Config: from_attributes = True


# ─── Staff ───
class StaffCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    role: str = "professional"
    photo_url: str | None = None
    color: str = "#1e3a8a"
    bio: str | None = None


class StaffOut(StaffCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


# ─── Services ───
class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    duration_minutes: int = 30
    buffer_minutes: int = 0
    price_mxn: Decimal = Decimal("0")
    deposit_mxn: Decimal = Decimal("0")
    requires_prepay: bool = False
    color: str = "#1e3a8a"
    staff_ids: list[UUID] = Field(default_factory=list)


class ServiceOut(ServiceCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


# ─── Availability ───
class AvailabilityRuleCreate(BaseModel):
    staff_id: UUID
    weekday: int  # 0=Mon
    start_time: time
    end_time: time


class AvailabilityRuleOut(AvailabilityRuleCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


class AvailabilityExceptionCreate(BaseModel):
    staff_id: UUID
    date: date
    kind: str = "blocked"  # blocked | extra
    start_time: time | None = None
    end_time: time | None = None
    note: str | None = None


class AvailabilityExceptionOut(AvailabilityExceptionCreate):
    id: UUID
    class Config: from_attributes = True


class Slot(BaseModel):
    starts_at: datetime
    ends_at: datetime
    staff_id: UUID
    staff_name: str


# ─── Customers ───
class CustomerCreate(BaseModel):
    name: str
    phone: str | None = None
    email: EmailStr | None = None
    whatsapp_optin: bool = True
    notes: str | None = None


class CustomerOut(BaseModel):
    id: UUID
    name: str
    phone: str | None = None
    email: str | None = None
    whatsapp_optin: bool
    total_visits: int
    no_show_count: int
    created_at: datetime
    class Config: from_attributes = True


# ─── Appointments ───
class AppointmentCreate(BaseModel):
    customer_id: UUID
    staff_id: UUID
    service_id: UUID
    starts_at: datetime
    notes: str | None = None


class AppointmentOut(BaseModel):
    id: UUID
    customer_id: UUID | None = None
    staff_id: UUID | None = None
    service_id: UUID | None = None
    starts_at: datetime
    ends_at: datetime
    status: str
    deposit_paid: bool
    total: Decimal
    deposit: Decimal
    source: str
    notes: str | None = None
    class Config: from_attributes = True


# ─── Public booking ───
class PublicCustomer(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None


class PublicBookRequest(BaseModel):
    service_id: UUID
    staff_id: UUID
    starts_at: datetime
    customer: PublicCustomer
    notes: str | None = None


class PublicBookResponse(BaseModel):
    appointment_id: UUID
    status: str
    requires_payment: bool
    checkout_url: str | None = None
    total: Decimal
    deposit: Decimal


# ─── Checkout ───
class CheckoutResponse(BaseModel):
    provider: str
    checkout_url: str
    session_id: str | None = None
    demo: bool = False


# ─── Payments ───
class PaymentOut(BaseModel):
    id: UUID
    appointment_id: UUID | None = None
    amount_mxn: Decimal
    currency: str
    provider: str | None = None
    status: str
    method: str | None = None
    description: str | None = None
    paid_at: datetime | None = None
    created_at: datetime
    class Config: from_attributes = True


# ─── Dashboard ───
class DashboardKPIs(BaseModel):
    appts_today: int
    appts_week: int
    revenue_mtd_mxn: Decimal
    no_show_rate: float
    confirmed_rate: float
    top_staff: list[dict[str, Any]]
    top_services: list[dict[str, Any]]
    upcoming: list[dict[str, Any]]


# ─── Public tenant view ───
class PublicTenantView(BaseModel):
    id: UUID
    name: str
    slug: str
    industry: str
    brand_color: str
    logo_url: str | None = None
    tagline: str | None = None
    about: str | None = None
    city: str | None = None
    instagram: str | None = None
    timezone: str
    services: list[ServiceOut]
    staff: list[StaffOut]
