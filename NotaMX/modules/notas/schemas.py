from __future__ import annotations
from datetime import datetime, date
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
    max_notes_month: int
    max_customers: int
    has_whatsapp: bool
    has_cfdi: bool
    has_branding: bool
    has_api: bool
    description: str | None = None
    featured: bool
    class Config: from_attributes = True


# ─── Tenants ───
class TenantCreate(BaseModel):
    name: str
    industry: str = "freelance"
    slug: str | None = None
    rfc: str | None = None
    razon_social: str | None = None
    regimen_fiscal: str | None = None
    codigo_postal: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    whatsapp_number: str | None = None
    plan_id: str | None = "free"


class TenantOut(BaseModel):
    id: UUID
    name: str
    slug: str | None = None
    industry: str
    rfc: str | None = None
    razon_social: str | None = None
    brand_color: str
    locale: str
    timezone: str
    active: bool
    class Config: from_attributes = True


# ─── Customers ───
class CustomerCreate(BaseModel):
    name: str
    rfc: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    whatsapp: str | None = None
    uso_cfdi: str = "G03"
    regimen_fiscal: str | None = None
    codigo_postal: str | None = None
    razon_social: str | None = None
    address: str | None = None
    notes: str | None = None


class CustomerOut(BaseModel):
    id: UUID
    name: str
    rfc: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    uso_cfdi: str | None = None
    regimen_fiscal: str | None = None
    codigo_postal: str | None = None
    razon_social: str | None = None
    address: str | None = None
    notes: str | None = None
    active: bool
    created_at: datetime
    class Config: from_attributes = True


# ─── Products ───
class ProductCreate(BaseModel):
    sku: str | None = None
    name: str
    description: str | None = None
    price_mxn: Decimal
    unit: str = "servicio"
    tax_rate: Decimal = Decimal("0.16")
    sat_product_key: str | None = None
    sat_unit_key: str | None = None


class ProductOut(BaseModel):
    id: UUID
    sku: str | None = None
    name: str
    description: str | None = None
    price_mxn: Decimal
    unit: str
    tax_rate: Decimal
    sat_product_key: str | None = None
    sat_unit_key: str | None = None
    active: bool
    class Config: from_attributes = True


# ─── Notes ───
class NoteItemIn(BaseModel):
    product_id: UUID | None = None
    description: str
    qty: Decimal = Decimal("1")
    unit_price: Decimal
    discount: Decimal = Decimal("0")
    tax_rate: Decimal = Decimal("0.16")


class NoteItemOut(BaseModel):
    id: UUID
    product_id: UUID | None = None
    description: str
    qty: Decimal
    unit_price: Decimal
    discount: Decimal
    tax_rate: Decimal
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    class Config: from_attributes = True


class NoteCreate(BaseModel):
    customer_id: UUID
    items: list[NoteItemIn] = Field(default_factory=list)
    notes: str | None = None
    valid_until: date | None = None
    number: str | None = None
    discount: Decimal = Decimal("0")


class NoteOut(BaseModel):
    id: UUID
    number: str | None = None
    customer_id: UUID | None = None
    status: str
    channel: str
    public_token: str
    currency: str
    subtotal: Decimal
    tax_total: Decimal
    discount: Decimal
    total: Decimal
    valid_until: date | None = None
    notes: str | None = None
    viewed_at: datetime | None = None
    sent_at: datetime | None = None
    paid_at: datetime | None = None
    created_at: datetime
    class Config: from_attributes = True


class NoteDetailOut(NoteOut):
    items: list[NoteItemOut] = []
    customer: CustomerOut | None = None


class NoteSendRequest(BaseModel):
    channel: str = "whatsapp"  # whatsapp | email | link
    message: str | None = None


class NoteSendResponse(BaseModel):
    note_id: UUID
    public_url: str
    channel: str
    whatsapp_sent: bool = False
    whatsapp_status: str | None = None


class PublicNoteOut(BaseModel):
    id: UUID
    number: str | None = None
    status: str
    subtotal: Decimal
    tax_total: Decimal
    discount: Decimal
    total: Decimal
    currency: str
    valid_until: date | None = None
    notes: str | None = None
    items: list[NoteItemOut] = []
    customer_name: str | None = None
    tenant_name: str
    tenant_brand_color: str
    tenant_rfc: str | None = None
    paid_at: datetime | None = None


# ─── Checkout ───
class CheckoutRequest(BaseModel):
    provider: str = "stripe"  # stripe | conekta
    success_url: str | None = None
    cancel_url: str | None = None


class CheckoutResponse(BaseModel):
    provider: str
    checkout_url: str
    session_id: str | None = None
    demo: bool = False


class PaymentOut(BaseModel):
    id: UUID
    note_id: UUID | None = None
    customer_id: UUID | None = None
    amount_mxn: Decimal
    currency: str
    provider: str | None = None
    status: str
    method: str | None = None
    description: str | None = None
    paid_at: datetime | None = None
    created_at: datetime
    class Config: from_attributes = True


# ─── CFDI ───
class CfdiIssueRequest(BaseModel):
    uso_cfdi: str | None = None
    metodo_pago: str = "PUE"
    forma_pago: str = "03"
    serie: str = "A"


class CfdiOut(BaseModel):
    id: UUID
    related_note_id: UUID | None = None
    payment_id: UUID | None = None
    customer_id: UUID | None = None
    uuid_sat: str | None = None
    serie: str
    folio: str | None = None
    xml_url: str | None = None
    pdf_url: str | None = None
    status: str
    total: Decimal | None = None
    uso_cfdi: str | None = None
    metodo_pago: str | None = None
    forma_pago: str | None = None
    issued_at: datetime | None = None
    created_at: datetime
    class Config: from_attributes = True


# ─── Dashboard ───
class DashboardKPIs(BaseModel):
    notes_mtd: int
    notes_paid_mtd: int
    notes_pending: int
    revenue_mtd_mxn: Decimal
    avg_note_mxn: Decimal
    conversion_rate: float
    cfdi_issued_mtd: int
    top_customers: list[dict[str, Any]]
    recent_notes: list[dict[str, Any]]
    monthly_series: list[dict[str, Any]]
