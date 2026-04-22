from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr


class TenantCreate(BaseModel):
    name: str
    industry: str = "other"
    rfc: str | None = None
    contact_email: EmailStr | None = None
    plan_id: str | None = "free"


class TenantOut(BaseModel):
    id: UUID
    name: str
    industry: str
    rfc: str | None = None
    contact_email: str | None = None
    locale: str
    timezone: str
    active: bool
    class Config: from_attributes = True


class PlanOut(BaseModel):
    id: str
    name: str
    price_mxn: Decimal
    currency: str
    max_warehouses: int
    max_items: int
    max_users: int
    nfc_enabled: bool
    webhooks_enabled: bool
    attendance_enabled: bool
    excel_export: bool
    description: str | None = None
    featured: bool
    class Config: from_attributes = True


class WarehouseCreate(BaseModel):
    code: str
    name: str
    address: str | None = None
    kind: str = "general"


class WarehouseOut(WarehouseCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


class LocationCreate(BaseModel):
    warehouse_id: UUID
    code: str
    name: str
    kind: str = "bin"
    parent_id: UUID | None = None


class LocationOut(LocationCreate):
    id: UUID
    path: str | None = None
    active: bool
    class Config: from_attributes = True


class CategoryCreate(BaseModel):
    code: str
    name: str
    parent_id: UUID | None = None


class CategoryOut(CategoryCreate):
    id: UUID
    class Config: from_attributes = True


class SupplierCreate(BaseModel):
    code: str
    name: str
    contact: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    rfc: str | None = None


class SupplierOut(SupplierCreate):
    id: UUID
    class Config: from_attributes = True


class ItemCreate(BaseModel):
    sku: str
    name: str
    description: str | None = None
    category_id: UUID | None = None
    unit: str = "pieza"
    barcode: str | None = None
    min_stock: Decimal = Decimal("0")
    max_stock: Decimal = Decimal("0")
    cost: Decimal = Decimal("0")
    price: Decimal = Decimal("0")
    is_serialized: bool = False
    perishable: bool = False
    shelf_life_days: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    initial_qty: Decimal = Decimal("0")
    initial_location_id: UUID | None = None


class ItemOut(BaseModel):
    id: UUID
    sku: str
    name: str
    description: str | None = None
    category_id: UUID | None = None
    unit: str
    barcode: str | None = None
    min_stock: Decimal
    max_stock: Decimal
    cost: Decimal
    price: Decimal
    is_serialized: bool
    perishable: bool
    shelf_life_days: int | None = None
    active: bool
    class Config: from_attributes = True


class StockLevelOut(BaseModel):
    item_id: UUID
    location_id: UUID
    qty: Decimal
    reserved: Decimal
    updated_at: datetime
    class Config: from_attributes = True


class MovementCreate(BaseModel):
    item_id: UUID
    kind: str  # IN | OUT | TRANSFER | ADJUST | CONSUME | RETURN | RESERVE | RELEASE
    qty: Decimal
    from_location_id: UUID | None = None
    to_location_id: UUID | None = None
    reason: str | None = None
    ref_type: str | None = None
    ref_id: str | None = None
    user_id: str | None = None


class MovementOut(BaseModel):
    id: UUID
    item_id: UUID
    kind: str
    qty: Decimal
    from_location_id: UUID | None = None
    to_location_id: UUID | None = None
    reason: str | None = None
    ref_type: str | None = None
    ref_id: str | None = None
    occurred_at: datetime
    class Config: from_attributes = True


class LabelCreate(BaseModel):
    kind: str  # BARCODE | QR | NFC
    code: str | None = None  # Si es None, se genera automáticamente
    item_id: UUID | None = None
    location_id: UUID | None = None
    employee_id: UUID | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class LabelOut(BaseModel):
    id: UUID
    kind: str
    code: str
    item_id: UUID | None = None
    location_id: UUID | None = None
    employee_id: UUID | None = None
    printed_at: datetime | None = None
    created_at: datetime
    class Config: from_attributes = True


class ScanResult(BaseModel):
    kind: str
    code: str
    resolved_type: str  # item | location | employee | unknown
    resolved: dict[str, Any] | None = None
    stock: list[StockLevelOut] = []


class EmployeeCreate(BaseModel):
    code: str
    name: str
    email: EmailStr | None = None
    role: str = "operador"


class EmployeeOut(EmployeeCreate):
    id: UUID
    active: bool
    class Config: from_attributes = True


class ShiftCreate(BaseModel):
    employee_id: UUID
    warehouse_id: UUID | None = None
    start_at: datetime
    end_at: datetime
    notes: str | None = None


class ShiftOut(ShiftCreate):
    id: UUID
    status: str
    class Config: from_attributes = True


class AttendancePunch(BaseModel):
    code: str  # código QR/NFC del empleado
    kind: str  # IN | OUT | BREAK_START | BREAK_END
    method: str = "QR"
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class AttendanceOut(BaseModel):
    id: UUID
    employee_id: UUID
    kind: str
    at: datetime
    method: str
    class Config: from_attributes = True


class WebhookEventIn(BaseModel):
    source: str
    event_type: str
    payload: dict[str, Any]


class ViabilityReport(BaseModel):
    tenant_id: UUID
    total_items: int
    total_warehouses: int
    items_under_min: int
    items_above_max: int
    movements_last_30d: int
    top_consumers_last_30d: list[dict[str, Any]]
    stock_value_mxn: Decimal
    health_score: int  # 0..100
    verdict: str
    recommendations: list[str]
