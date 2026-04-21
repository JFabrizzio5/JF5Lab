"""Schemas Pydantic para PorCobrar."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class TenantCreate(BaseModel):
    name: str
    rfc: str | None = None
    razon_social: str | None = None
    industry: str = "servicios"
    contact_email: str | None = None
    contact_phone: str | None = None
    brand_color: str = "#10b981"


class TenantOut(BaseModel):
    id: UUID
    name: str
    slug: str | None = None
    rfc: str | None = None
    razon_social: str | None = None
    industry: str
    brand_color: str | None = None
    created_at: datetime
    class Config: from_attributes = True


class DebtorCreate(BaseModel):
    rfc: str | None = None
    name: str
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    notes: str | None = None


class DebtorOut(BaseModel):
    id: UUID
    rfc: str | None = None
    name: str
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    total_owed: Decimal = Decimal(0)
    overdue_days_avg: int = 0
    payment_score: int = 50
    last_payment_at: datetime | None = None
    class Config: from_attributes = True


class InvoiceCreate(BaseModel):
    debtor_id: UUID
    cfdi_uuid: str | None = None
    serie: str | None = None
    folio: str | None = None
    issued_at: datetime | None = None
    due_at: datetime
    total: Decimal
    currency: str = "MXN"
    notes: str | None = None


class InvoiceOut(BaseModel):
    id: UUID
    debtor_id: UUID
    cfdi_uuid: str | None = None
    serie: str | None = None
    folio: str | None = None
    issued_at: datetime | None = None
    due_at: datetime
    total: Decimal
    paid_amount: Decimal = Decimal(0)
    currency: str = "MXN"
    status: str
    source: str | None = None
    class Config: from_attributes = True


class DunningTemplateCreate(BaseModel):
    name: str
    channel: str
    subject: str | None = None
    body: str


class DunningTemplateOut(DunningTemplateCreate):
    id: UUID
    class Config: from_attributes = True


class DunningFlowCreate(BaseModel):
    name: str
    description: str | None = None
    steps: list[dict] = []


class DunningFlowOut(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    steps: list[dict] = []
    active: bool
    class Config: from_attributes = True


class AssignFlow(BaseModel):
    flow_id: UUID
