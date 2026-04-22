"""StockLink - Modelo de dominio generalista.

Multi-tenant por `tenant_id` en cada tabla. Aislamiento real vía Row Level
Security (Postgres) — ver migración inicial. RLS lee `current_setting('app.tenant_id')`.

Industrias soportadas (campo libre): warehouse, restaurant, construction, store,
shipping, pharmacy, workshop, clinic, other.
"""
from __future__ import annotations
import enum
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Integer, Numeric, ForeignKey, Text,
    UniqueConstraint, Index, Enum as SAEnum, JSON,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from config.database import Base


def uuid_pk():
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def tenant_fk():
    return Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)


class Industry(str, enum.Enum):
    warehouse = "warehouse"
    restaurant = "restaurant"
    construction = "construction"
    store = "store"
    shipping = "shipping"
    pharmacy = "pharmacy"
    workshop = "workshop"
    clinic = "clinic"
    other = "other"


class MovementKind(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"
    ADJUST = "ADJUST"
    CONSUME = "CONSUME"
    RETURN = "RETURN"
    RESERVE = "RESERVE"
    RELEASE = "RELEASE"


class LabelKind(str, enum.Enum):
    BARCODE = "BARCODE"
    QR = "QR"
    NFC = "NFC"


class AttendanceKind(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    BREAK_START = "BREAK_START"
    BREAK_END = "BREAK_END"


# ──────────────────────────────────────────────────────────────
# Plans (global, no tenant)
# ──────────────────────────────────────────────────────────────
class Plan(Base):
    __tablename__ = "plans"
    id = Column(String(32), primary_key=True)
    name = Column(String(80), nullable=False)
    price_mxn = Column(Numeric(10, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="MXN")
    max_warehouses = Column(Integer, nullable=False, default=1)
    max_items = Column(Integer, nullable=False, default=100)
    max_users = Column(Integer, nullable=False, default=2)
    nfc_enabled = Column(Boolean, default=False)
    webhooks_enabled = Column(Boolean, default=False)
    attendance_enabled = Column(Boolean, default=False)
    excel_export = Column(Boolean, default=True)
    description = Column(Text)
    featured = Column(Boolean, default=False)


# ──────────────────────────────────────────────────────────────
# Tenants
# ──────────────────────────────────────────────────────────────
class Tenant(Base):
    __tablename__ = "tenants"
    id = uuid_pk()
    name = Column(String(160), nullable=False)
    industry = Column(String(40), nullable=False, default="other")
    country = Column(String(2), nullable=False, default="MX")
    rfc = Column(String(13))
    contact_email = Column(String(160))
    logo_url = Column(String(512))
    locale = Column(String(10), default="es-MX")
    timezone = Column(String(40), default="America/Mexico_City")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TenantPlan(Base):
    __tablename__ = "tenant_plans"
    id = uuid_pk()
    tenant_id = tenant_fk()
    plan_id = Column(String(32), ForeignKey("plans.id"), nullable=False)
    status = Column(String(20), default="active")  # active | canceled | trialing
    started_at = Column(DateTime, default=datetime.utcnow)
    current_period_end = Column(DateTime)


class ApiKey(Base):
    __tablename__ = "api_keys"
    id = uuid_pk()
    tenant_id = tenant_fk()
    name = Column(String(80), nullable=False)
    key_hash = Column(String(128), nullable=False, unique=True, index=True)
    scopes = Column(JSONB, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime)
    revoked_at = Column(DateTime)


# ──────────────────────────────────────────────────────────────
# Warehouses / Locations
# ──────────────────────────────────────────────────────────────
class Warehouse(Base):
    __tablename__ = "warehouses"
    id = uuid_pk()
    tenant_id = tenant_fk()
    code = Column(String(40), nullable=False)
    name = Column(String(160), nullable=False)
    address = Column(String(320))
    kind = Column(String(40), default="general")  # kitchen, cellar, shelf, site, hub
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_wh_tenant_code"),)


class Location(Base):
    __tablename__ = "locations"
    id = uuid_pk()
    tenant_id = tenant_fk()
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="SET NULL"))
    code = Column(String(60), nullable=False)
    name = Column(String(160), nullable=False)
    kind = Column(String(40), default="bin")  # aisle, rack, shelf, bin, zone, truck
    path = Column(String(512))  # materialized path, e.g. WH1/A/01/B3
    active = Column(Boolean, default=True)
    __table_args__ = (
        UniqueConstraint("tenant_id", "warehouse_id", "code", name="uq_loc_tenant_wh_code"),
        Index("ix_loc_tenant_path", "tenant_id", "path"),
    )


# ──────────────────────────────────────────────────────────────
# Catalog
# ──────────────────────────────────────────────────────────────
class Category(Base):
    __tablename__ = "categories"
    id = uuid_pk()
    tenant_id = tenant_fk()
    code = Column(String(40), nullable=False)
    name = Column(String(160), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"))
    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_cat_tenant_code"),)


class Supplier(Base):
    __tablename__ = "suppliers"
    id = uuid_pk()
    tenant_id = tenant_fk()
    code = Column(String(40), nullable=False)
    name = Column(String(160), nullable=False)
    contact = Column(String(160))
    email = Column(String(160))
    phone = Column(String(40))
    rfc = Column(String(13))
    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_sup_tenant_code"),)


class Item(Base):
    __tablename__ = "items"
    id = uuid_pk()
    tenant_id = tenant_fk()
    sku = Column(String(80), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"))
    unit = Column(String(20), default="pieza")  # kg, l, pieza, caja, m, m2, m3
    barcode = Column(String(80), index=True)
    min_stock = Column(Numeric(14, 3), default=0)
    max_stock = Column(Numeric(14, 3), default=0)
    cost = Column(Numeric(12, 2), default=0)
    price = Column(Numeric(12, 2), default=0)
    is_serialized = Column(Boolean, default=False)
    perishable = Column(Boolean, default=False)
    shelf_life_days = Column(Integer)
    metadata_json = Column("metadata", JSONB, default=dict)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint("tenant_id", "sku", name="uq_item_tenant_sku"),
        Index("ix_item_tenant_name", "tenant_id", "name"),
    )


# ──────────────────────────────────────────────────────────────
# Stock
# ──────────────────────────────────────────────────────────────
class StockLevel(Base):
    __tablename__ = "stock_levels"
    id = uuid_pk()
    tenant_id = tenant_fk()
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    qty = Column(Numeric(14, 3), nullable=False, default=0)
    reserved = Column(Numeric(14, 3), nullable=False, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint("tenant_id", "item_id", "location_id", name="uq_stock_tenant_item_loc"),
        Index("ix_stock_tenant_item", "tenant_id", "item_id"),
    )


class Movement(Base):
    __tablename__ = "movements"
    id = uuid_pk()
    tenant_id = tenant_fk()
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    from_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="SET NULL"))
    to_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="SET NULL"))
    qty = Column(Numeric(14, 3), nullable=False)
    kind = Column(String(16), nullable=False)
    reason = Column(String(200))
    ref_type = Column(String(40))  # order, invoice, event, adjustment, audit
    ref_id = Column(String(80))
    user_id = Column(String(80))
    source_event = Column(JSONB)
    occurred_at = Column(DateTime, default=datetime.utcnow, index=True)
    __table_args__ = (Index("ix_mov_tenant_item_date", "tenant_id", "item_id", "occurred_at"),)


# ──────────────────────────────────────────────────────────────
# Labels: Barcode / QR / NFC
# ──────────────────────────────────────────────────────────────
class Label(Base):
    __tablename__ = "labels"
    id = uuid_pk()
    tenant_id = tenant_fk()
    kind = Column(String(10), nullable=False)  # BARCODE | QR | NFC
    code = Column(String(200), nullable=False)  # EAN13/Code128/UUID/NFC UID
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"))
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"))
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"))
    metadata_json = Column("metadata", JSONB, default=dict)
    printed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint("tenant_id", "kind", "code", name="uq_label_tenant_kind_code"),
        Index("ix_label_tenant_code", "tenant_id", "code"),
    )


# ──────────────────────────────────────────────────────────────
# Attendance / Shifts
# ──────────────────────────────────────────────────────────────
class Employee(Base):
    __tablename__ = "employees"
    id = uuid_pk()
    tenant_id = tenant_fk()
    code = Column(String(40), nullable=False)
    name = Column(String(160), nullable=False)
    email = Column(String(160))
    role = Column(String(60), default="operador")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_emp_tenant_code"),)


class Shift(Base):
    __tablename__ = "shifts"
    id = uuid_pk()
    tenant_id = tenant_fk()
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="SET NULL"))
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    status = Column(String(20), default="scheduled")  # scheduled, active, completed, missed
    notes = Column(Text)


class Attendance(Base):
    __tablename__ = "attendance"
    id = uuid_pk()
    tenant_id = tenant_fk()
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id", ondelete="SET NULL"))
    kind = Column(String(16), nullable=False)  # IN | OUT | BREAK_START | BREAK_END
    at = Column(DateTime, default=datetime.utcnow, index=True)
    method = Column(String(16), default="QR")  # QR | NFC | MANUAL
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    metadata_json = Column("metadata", JSONB, default=dict)
    __table_args__ = (Index("ix_att_tenant_emp_date", "tenant_id", "employee_id", "at"),)


# ──────────────────────────────────────────────────────────────
# External events (webhooks)
# ──────────────────────────────────────────────────────────────
class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = uuid_pk()
    tenant_id = tenant_fk()
    source = Column(String(60), nullable=False)  # pos_restaurant, pos_store, wms, erp, custom
    event_type = Column(String(60), nullable=False)  # order.placed, order.fulfilled, shipment.out
    payload = Column(JSONB, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime)
    status = Column(String(20), default="pending")  # pending | processed | failed
    error = Column(Text)
