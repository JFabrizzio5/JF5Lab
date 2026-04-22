"""StockLink v1 — todas las rutas del microservicio bajo `/inventory/v1`."""
from __future__ import annotations
import io
import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_sql_db
from core.tenant import get_tenant_id, tenant_db
from modules.inventory.models import (
    Tenant, Plan, TenantPlan, Warehouse, Location, Category, Supplier,
    Item, StockLevel, Movement, Label, Employee, Shift, Attendance, WebhookEvent,
)
from modules.inventory import schemas as S
from modules.inventory.services.stock import apply_movement
from modules.inventory.services.labels import (
    generate_barcode_png, generate_qr_png, generate_nfc_code, render_label_pdf,
)
from modules.inventory.services.excel import rows_to_xlsx, fmt_dt

router = APIRouter()


# ─────────────────────────────────────────────────────
# PLANS (público) + TENANTS (admin)
# ─────────────────────────────────────────────────────
@router.get("/plans", response_model=list[S.PlanOut])
async def list_plans(db: AsyncSession = Depends(get_sql_db)):
    result = await db.execute(select(Plan).order_by(Plan.price_mxn))
    return result.scalars().all()


@router.post("/tenants", response_model=S.TenantOut, status_code=201)
async def create_tenant(payload: S.TenantCreate, db: AsyncSession = Depends(get_sql_db)):
    t = Tenant(
        name=payload.name, industry=payload.industry, rfc=payload.rfc,
        contact_email=payload.contact_email,
    )
    db.add(t)
    await db.flush()
    if payload.plan_id:
        plan = (await db.execute(select(Plan).where(Plan.id == payload.plan_id))).scalar_one_or_none()
        if plan:
            db.add(TenantPlan(tenant_id=t.id, plan_id=plan.id, current_period_end=datetime.utcnow() + timedelta(days=30)))
    await db.commit()
    await db.refresh(t)
    return t


@router.get("/tenants/{tid}", response_model=S.TenantOut)
async def get_tenant(tid: UUID, db: AsyncSession = Depends(get_sql_db)):
    t = (await db.execute(select(Tenant).where(Tenant.id == tid))).scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Tenant no encontrado")
    return t


# ─────────────────────────────────────────────────────
# WAREHOUSES / LOCATIONS
# ─────────────────────────────────────────────────────
@router.get("/warehouses", response_model=list[S.WarehouseOut])
async def list_warehouses(db: AsyncSession = Depends(tenant_db)):
    r = await db.execute(select(Warehouse).order_by(Warehouse.code))
    return r.scalars().all()


@router.post("/warehouses", response_model=S.WarehouseOut, status_code=201)
async def create_warehouse(payload: S.WarehouseCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    w = Warehouse(tenant_id=tenant_id, **payload.model_dump())
    db.add(w)
    await db.commit()
    await db.refresh(w)
    return w


@router.get("/locations", response_model=list[S.LocationOut])
async def list_locations(warehouse_id: UUID | None = None, db: AsyncSession = Depends(tenant_db)):
    q = select(Location)
    if warehouse_id:
        q = q.where(Location.warehouse_id == warehouse_id)
    r = await db.execute(q.order_by(Location.path))
    return r.scalars().all()


@router.post("/locations", response_model=S.LocationOut, status_code=201)
async def create_location(payload: S.LocationCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    wh = (await db.execute(select(Warehouse).where(Warehouse.id == payload.warehouse_id))).scalar_one_or_none()
    if not wh:
        raise HTTPException(status_code=404, detail="Warehouse no encontrado")
    path = f"{wh.code}/{payload.code}"
    if payload.parent_id:
        parent = (await db.execute(select(Location).where(Location.id == payload.parent_id))).scalar_one_or_none()
        if parent:
            path = f"{parent.path}/{payload.code}"
    l = Location(tenant_id=tenant_id, path=path, **payload.model_dump())
    db.add(l)
    await db.commit()
    await db.refresh(l)
    return l


# ─────────────────────────────────────────────────────
# CATEGORIES / SUPPLIERS
# ─────────────────────────────────────────────────────
@router.get("/categories", response_model=list[S.CategoryOut])
async def list_categories(db: AsyncSession = Depends(tenant_db)):
    r = await db.execute(select(Category).order_by(Category.name))
    return r.scalars().all()


@router.post("/categories", response_model=S.CategoryOut, status_code=201)
async def create_category(payload: S.CategoryCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    c = Category(tenant_id=tenant_id, **payload.model_dump())
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c


@router.get("/suppliers", response_model=list[S.SupplierOut])
async def list_suppliers(db: AsyncSession = Depends(tenant_db)):
    r = await db.execute(select(Supplier).order_by(Supplier.name))
    return r.scalars().all()


@router.post("/suppliers", response_model=S.SupplierOut, status_code=201)
async def create_supplier(payload: S.SupplierCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    s = Supplier(tenant_id=tenant_id, **payload.model_dump())
    db.add(s)
    await db.commit()
    await db.refresh(s)
    return s


# ─────────────────────────────────────────────────────
# ITEMS (catálogo)
# ─────────────────────────────────────────────────────
@router.get("/items", response_model=list[S.ItemOut])
async def list_items(q: str | None = None, category_id: UUID | None = None, db: AsyncSession = Depends(tenant_db)):
    query = select(Item).where(Item.active == True)  # noqa: E712
    if q:
        query = query.where(func.lower(Item.name).like(f"%{q.lower()}%") | Item.sku.ilike(f"%{q}%") | Item.barcode.ilike(f"%{q}%"))
    if category_id:
        query = query.where(Item.category_id == category_id)
    r = await db.execute(query.order_by(Item.name).limit(500))
    return r.scalars().all()


@router.post("/items", response_model=S.ItemOut, status_code=201)
async def create_item(payload: S.ItemCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    data = payload.model_dump()
    meta = data.pop("metadata", {})
    initial_qty = data.pop("initial_qty", Decimal("0"))
    initial_loc = data.pop("initial_location_id", None)
    item = Item(tenant_id=tenant_id, metadata_json=meta, **data)
    db.add(item)
    await db.flush()
    if initial_qty and initial_qty > 0 and initial_loc:
        await apply_movement(
            db, tenant_id,
            item_id=item.id, kind="IN", qty=Decimal(str(initial_qty)),
            from_location_id=None, to_location_id=initial_loc,
            reason="Carga inicial", ref_type="item_create",
        )
    else:
        await db.commit()
    await db.refresh(item)
    # Label QR automático para el nuevo item
    db.add(Label(tenant_id=tenant_id, kind="QR", code=f"SKU-{item.sku}", item_id=item.id, metadata_json={"auto": True}))
    await db.commit()
    return item


@router.get("/items/{item_id}", response_model=S.ItemOut)
async def get_item(item_id: UUID, db: AsyncSession = Depends(tenant_db)):
    i = (await db.execute(select(Item).where(Item.id == item_id))).scalar_one_or_none()
    if not i:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return i


@router.get("/items/{item_id}/stock", response_model=list[S.StockLevelOut])
async def get_item_stock(item_id: UUID, db: AsyncSession = Depends(tenant_db)):
    r = await db.execute(select(StockLevel).where(StockLevel.item_id == item_id))
    return r.scalars().all()


# ─────────────────────────────────────────────────────
# MOVEMENTS (entrada/salida/traslado/consumo)
# ─────────────────────────────────────────────────────
@router.post("/movements", response_model=S.MovementOut, status_code=201)
async def create_movement(payload: S.MovementCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    mv = await apply_movement(
        db, tenant_id,
        item_id=payload.item_id, kind=payload.kind, qty=payload.qty,
        from_location_id=payload.from_location_id, to_location_id=payload.to_location_id,
        reason=payload.reason, ref_type=payload.ref_type, ref_id=payload.ref_id, user_id=payload.user_id,
    )
    return mv


@router.get("/movements", response_model=list[S.MovementOut])
async def list_movements(item_id: UUID | None = None, since: datetime | None = None, limit: int = Query(200, le=2000), db: AsyncSession = Depends(tenant_db)):
    q = select(Movement)
    if item_id:
        q = q.where(Movement.item_id == item_id)
    if since:
        q = q.where(Movement.occurred_at >= since)
    r = await db.execute(q.order_by(Movement.occurred_at.desc()).limit(limit))
    return r.scalars().all()


# ─────────────────────────────────────────────────────
# LABELS (barcode, QR, NFC) + SCAN
# ─────────────────────────────────────────────────────
@router.post("/labels", response_model=S.LabelOut, status_code=201)
async def create_label(payload: S.LabelCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    kind = payload.kind.upper()
    if kind not in ("BARCODE", "QR", "NFC"):
        raise HTTPException(status_code=400, detail="kind debe ser BARCODE|QR|NFC")
    code = payload.code
    if not code:
        if kind == "NFC":
            code = generate_nfc_code()
        elif kind == "QR":
            code = f"STK-{uuid4().hex[:12].upper()}"
        else:
            code = f"{secrets.randbelow(10**11):011d}"  # Code128 numérico
    lbl = Label(
        tenant_id=tenant_id, kind=kind, code=code,
        item_id=payload.item_id, location_id=payload.location_id,
        employee_id=payload.employee_id, metadata_json=payload.metadata,
    )
    db.add(lbl)
    await db.commit()
    await db.refresh(lbl)
    return lbl


@router.get("/labels/{label_id}/image")
async def render_label_image(label_id: UUID, size: int = 320, db: AsyncSession = Depends(tenant_db)):
    lbl = (await db.execute(select(Label).where(Label.id == label_id))).scalar_one_or_none()
    if not lbl:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    if lbl.kind in ("QR", "NFC"):
        png = generate_qr_png(f"stocklink://{lbl.kind.lower()}/{lbl.code}", size=size)
    else:
        png = generate_barcode_png(lbl.code, kind="CODE128")
    return Response(content=png, media_type="image/png")


@router.post("/labels/pdf")
async def labels_bulk_pdf(ids: list[UUID], db: AsyncSession = Depends(tenant_db)):
    r = await db.execute(select(Label).where(Label.id.in_(ids)))
    labels = r.scalars().all()
    payload = []
    for lbl in labels:
        name = ""
        if lbl.item_id:
            it = (await db.execute(select(Item).where(Item.id == lbl.item_id))).scalar_one_or_none()
            if it:
                name = it.name
        elif lbl.location_id:
            loc = (await db.execute(select(Location).where(Location.id == lbl.location_id))).scalar_one_or_none()
            if loc:
                name = f"{loc.name} ({loc.path})"
        elif lbl.employee_id:
            emp = (await db.execute(select(Employee).where(Employee.id == lbl.employee_id))).scalar_one_or_none()
            if emp:
                name = emp.name
        payload.append({
            "code": lbl.code, "kind": lbl.kind, "name": name,
            "subtitle": lbl.kind, "payload": f"stocklink://{lbl.kind.lower()}/{lbl.code}",
        })
    pdf = render_label_pdf(payload)
    return Response(content=pdf, media_type="application/pdf")


@router.get("/scan/{code}", response_model=S.ScanResult)
async def scan_code(code: str, db: AsyncSession = Depends(tenant_db)):
    # Normalizar deep-link stocklink://kind/code
    if code.startswith("stocklink://"):
        code = code.split("/")[-1]
    lbl = (await db.execute(select(Label).where(Label.code == code))).scalar_one_or_none()
    # Fallback: barcode directo en item
    if not lbl:
        item = (await db.execute(select(Item).where(Item.barcode == code))).scalar_one_or_none()
        if item:
            stock = (await db.execute(select(StockLevel).where(StockLevel.item_id == item.id))).scalars().all()
            return S.ScanResult(
                kind="BARCODE", code=code, resolved_type="item",
                resolved={"id": str(item.id), "sku": item.sku, "name": item.name, "unit": item.unit},
                stock=[S.StockLevelOut.model_validate(s) for s in stock],
            )
        return S.ScanResult(kind="UNKNOWN", code=code, resolved_type="unknown")

    if lbl.item_id:
        item = (await db.execute(select(Item).where(Item.id == lbl.item_id))).scalar_one_or_none()
        stock = (await db.execute(select(StockLevel).where(StockLevel.item_id == lbl.item_id))).scalars().all()
        return S.ScanResult(
            kind=lbl.kind, code=code, resolved_type="item",
            resolved={"id": str(item.id), "sku": item.sku, "name": item.name, "unit": item.unit} if item else None,
            stock=[S.StockLevelOut.model_validate(s) for s in stock],
        )
    if lbl.location_id:
        loc = (await db.execute(select(Location).where(Location.id == lbl.location_id))).scalar_one_or_none()
        return S.ScanResult(
            kind=lbl.kind, code=code, resolved_type="location",
            resolved={"id": str(loc.id), "code": loc.code, "name": loc.name, "path": loc.path} if loc else None,
        )
    if lbl.employee_id:
        emp = (await db.execute(select(Employee).where(Employee.id == lbl.employee_id))).scalar_one_or_none()
        return S.ScanResult(
            kind=lbl.kind, code=code, resolved_type="employee",
            resolved={"id": str(emp.id), "code": emp.code, "name": emp.name} if emp else None,
        )
    return S.ScanResult(kind=lbl.kind, code=code, resolved_type="unknown")


# ─────────────────────────────────────────────────────
# EMPLOYEES / ATTENDANCE (asistencia por QR/NFC)
# ─────────────────────────────────────────────────────
@router.get("/employees", response_model=list[S.EmployeeOut])
async def list_employees(db: AsyncSession = Depends(tenant_db)):
    r = await db.execute(select(Employee).order_by(Employee.name))
    return r.scalars().all()


@router.post("/employees", response_model=S.EmployeeOut, status_code=201)
async def create_employee(payload: S.EmployeeCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    e = Employee(tenant_id=tenant_id, **payload.model_dump())
    db.add(e)
    await db.commit()
    await db.refresh(e)
    # Crear label QR automático para asistencia
    lbl = Label(
        tenant_id=tenant_id, kind="QR", code=f"EMP-{e.code}-{uuid4().hex[:6].upper()}",
        employee_id=e.id, metadata_json={"auto": True},
    )
    db.add(lbl)
    await db.commit()
    return e


@router.get("/shifts", response_model=list[S.ShiftOut])
async def list_shifts(date_from: datetime | None = None, date_to: datetime | None = None, db: AsyncSession = Depends(tenant_db)):
    q = select(Shift)
    if date_from:
        q = q.where(Shift.start_at >= date_from)
    if date_to:
        q = q.where(Shift.end_at <= date_to)
    r = await db.execute(q.order_by(Shift.start_at.desc()))
    return r.scalars().all()


@router.post("/shifts", response_model=S.ShiftOut, status_code=201)
async def create_shift(payload: S.ShiftCreate, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    sh = Shift(tenant_id=tenant_id, **payload.model_dump())
    db.add(sh)
    await db.commit()
    await db.refresh(sh)
    return sh


@router.post("/attendance/punch", response_model=S.AttendanceOut)
async def punch_attendance(payload: S.AttendancePunch, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    code = payload.code
    if code.startswith("stocklink://"):
        code = code.split("/")[-1]
    lbl = (await db.execute(select(Label).where(Label.code == code))).scalar_one_or_none()
    emp_id = None
    if lbl and lbl.employee_id:
        emp_id = lbl.employee_id
    else:
        emp = (await db.execute(select(Employee).where(Employee.code == code))).scalar_one_or_none()
        if emp:
            emp_id = emp.id
    if not emp_id:
        raise HTTPException(status_code=404, detail="Empleado no encontrado para ese código")
    att = Attendance(
        tenant_id=tenant_id, employee_id=emp_id, kind=payload.kind, method=payload.method,
        latitude=payload.latitude, longitude=payload.longitude,
    )
    db.add(att)
    await db.commit()
    await db.refresh(att)
    return att


@router.get("/attendance", response_model=list[S.AttendanceOut])
async def list_attendance(date_from: datetime | None = None, date_to: datetime | None = None, employee_id: UUID | None = None, db: AsyncSession = Depends(tenant_db)):
    q = select(Attendance)
    if date_from:
        q = q.where(Attendance.at >= date_from)
    if date_to:
        q = q.where(Attendance.at <= date_to)
    if employee_id:
        q = q.where(Attendance.employee_id == employee_id)
    r = await db.execute(q.order_by(Attendance.at.desc()).limit(1000))
    return r.scalars().all()


# ─────────────────────────────────────────────────────
# EVENT-DRIVEN DECREMENT (webhooks externos)
# ─────────────────────────────────────────────────────
@router.post("/events/webhook", status_code=202)
async def receive_webhook(payload: S.WebhookEventIn, tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    """Recibe eventos externos (POS restaurante, tienda, ERP construcción) y
    aplica movimientos.

    Formato esperado en `payload.payload`:
    {
      "items": [{"sku": "...", "qty": 2, "from_location_code": "KITCHEN"}],
      "ref_id": "ORDER-123",
      "ref_type": "order"
    }
    """
    ev = WebhookEvent(
        tenant_id=tenant_id, source=payload.source, event_type=payload.event_type,
        payload=payload.payload,
    )
    db.add(ev)
    await db.commit()
    await db.refresh(ev)

    applied = []
    try:
        items_in = payload.payload.get("items", [])
        ref_type = payload.payload.get("ref_type", payload.event_type)
        ref_id = payload.payload.get("ref_id")
        for entry in items_in:
            sku = entry.get("sku")
            qty = Decimal(str(entry.get("qty", 0)))
            from_code = entry.get("from_location_code")
            to_code = entry.get("to_location_code")
            kind = entry.get("kind", "CONSUME")
            item = (await db.execute(select(Item).where(Item.sku == sku))).scalar_one_or_none()
            if not item:
                raise ValueError(f"SKU no encontrado: {sku}")
            from_loc = None
            to_loc = None
            if from_code:
                from_loc = (await db.execute(select(Location).where(Location.code == from_code))).scalar_one_or_none()
            if to_code:
                to_loc = (await db.execute(select(Location).where(Location.code == to_code))).scalar_one_or_none()
            # Si no mandan location pero hay una sola posible, usarla
            if not from_loc and kind in ("OUT", "CONSUME", "TRANSFER"):
                lv = (await db.execute(select(StockLevel).where(StockLevel.item_id == item.id).limit(1))).scalar_one_or_none()
                if lv:
                    from_loc_id = lv.location_id
                else:
                    raise ValueError("Sin location de origen")
            else:
                from_loc_id = from_loc.id if from_loc else None
            to_loc_id = to_loc.id if to_loc else None
            mv = await apply_movement(
                db, tenant_id, item_id=item.id, kind=kind, qty=qty,
                from_location_id=from_loc_id, to_location_id=to_loc_id,
                reason=f"{payload.source}:{payload.event_type}",
                ref_type=ref_type, ref_id=ref_id, source_event=payload.payload,
            )
            applied.append(str(mv.id))
        ev.processed_at = datetime.utcnow()
        ev.status = "processed"
        await db.commit()
    except Exception as e:
        ev.status = "failed"
        ev.error = str(e)
        await db.commit()
        raise HTTPException(status_code=400, detail=f"Evento fallido: {e}")
    return {"event_id": str(ev.id), "movements": applied, "status": "processed"}


# ─────────────────────────────────────────────────────
# EXCEL EXPORTS
# ─────────────────────────────────────────────────────
@router.get("/exports/inventory.xlsx")
async def export_inventory(db: AsyncSession = Depends(tenant_db)):
    r = await db.execute(
        select(Item, StockLevel, Location, Warehouse)
        .join(StockLevel, StockLevel.item_id == Item.id, isouter=True)
        .join(Location, Location.id == StockLevel.location_id, isouter=True)
        .join(Warehouse, Warehouse.id == Location.warehouse_id, isouter=True)
        .order_by(Item.sku)
    )
    rows = []
    for item, lvl, loc, wh in r.all():
        rows.append([
            item.sku, item.name, item.unit,
            wh.code if wh else "", loc.code if loc else "", loc.path if loc else "",
            float(lvl.qty) if lvl else 0,
            float(lvl.reserved) if lvl else 0,
            float(item.min_stock or 0), float(item.max_stock or 0),
            float(item.cost or 0), float(item.price or 0),
        ])
    xlsx = rows_to_xlsx(
        "Inventario",
        ["SKU", "Nombre", "Unidad", "Almacén", "Ubicación", "Ruta", "Qty", "Reservado", "Mín", "Máx", "Costo", "Precio"],
        rows,
    )
    return StreamingResponse(
        io.BytesIO(xlsx),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename=inventario-{datetime.utcnow():%Y%m%d}.xlsx'},
    )


@router.get("/exports/movements.xlsx")
async def export_movements(date_from: datetime | None = None, date_to: datetime | None = None, db: AsyncSession = Depends(tenant_db)):
    q = select(Movement, Item).join(Item, Item.id == Movement.item_id)
    if date_from:
        q = q.where(Movement.occurred_at >= date_from)
    if date_to:
        q = q.where(Movement.occurred_at <= date_to)
    r = await db.execute(q.order_by(Movement.occurred_at.desc()))
    rows = []
    for mv, it in r.all():
        rows.append([
            fmt_dt(mv.occurred_at), mv.kind, it.sku, it.name, float(mv.qty),
            str(mv.from_location_id or ""), str(mv.to_location_id or ""),
            mv.ref_type or "", mv.ref_id or "", mv.reason or "",
        ])
    xlsx = rows_to_xlsx(
        "Movimientos",
        ["Fecha", "Tipo", "SKU", "Artículo", "Cantidad", "Origen", "Destino", "Ref. Tipo", "Ref. ID", "Motivo"],
        rows,
    )
    return StreamingResponse(
        io.BytesIO(xlsx),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename=movimientos-{datetime.utcnow():%Y%m%d}.xlsx'},
    )


@router.get("/exports/attendance.xlsx")
async def export_attendance(date_from: datetime | None = None, date_to: datetime | None = None, db: AsyncSession = Depends(tenant_db)):
    q = select(Attendance, Employee).join(Employee, Employee.id == Attendance.employee_id)
    if date_from:
        q = q.where(Attendance.at >= date_from)
    if date_to:
        q = q.where(Attendance.at <= date_to)
    r = await db.execute(q.order_by(Attendance.at.desc()))
    rows = []
    for at, emp in r.all():
        rows.append([fmt_dt(at.at), at.kind, emp.code, emp.name, at.method, float(at.latitude or 0), float(at.longitude or 0)])
    xlsx = rows_to_xlsx(
        "Asistencias",
        ["Fecha/Hora", "Tipo", "Código", "Empleado", "Método", "Lat", "Lng"],
        rows,
    )
    return StreamingResponse(
        io.BytesIO(xlsx),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename=asistencias-{datetime.utcnow():%Y%m%d}.xlsx'},
    )


# ─────────────────────────────────────────────────────
# REPORTES (viabilidad, KPIs)
# ─────────────────────────────────────────────────────
@router.get("/reports/dashboard")
async def dashboard_kpis(tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    total_items = (await db.execute(select(func.count(Item.id)))).scalar() or 0
    total_wh = (await db.execute(select(func.count(Warehouse.id)))).scalar() or 0
    total_locs = (await db.execute(select(func.count(Location.id)))).scalar() or 0
    total_moves = (await db.execute(select(func.count(Movement.id)))).scalar() or 0
    under_min = (await db.execute(
        select(func.count(Item.id))
        .join(StockLevel, StockLevel.item_id == Item.id)
        .where(StockLevel.qty < Item.min_stock)
        .where(Item.min_stock > 0)
    )).scalar() or 0
    total_employees = (await db.execute(select(func.count(Employee.id)))).scalar() or 0
    last_moves_r = await db.execute(
        select(Movement, Item).join(Item, Item.id == Movement.item_id)
        .order_by(Movement.occurred_at.desc()).limit(10)
    )
    recent = [
        {"id": str(mv.id), "kind": mv.kind, "qty": float(mv.qty), "item": it.name, "at": fmt_dt(mv.occurred_at)}
        for mv, it in last_moves_r.all()
    ]
    return {
        "tenant_id": tenant_id, "total_items": total_items, "total_warehouses": total_wh,
        "total_locations": total_locs, "total_movements": total_moves,
        "items_under_min": under_min, "total_employees": total_employees,
        "recent_movements": recent,
    }


@router.get("/reports/viability", response_model=S.ViabilityReport)
async def viability_report(tenant_id: str = Depends(get_tenant_id), db: AsyncSession = Depends(tenant_db)):
    total_items = (await db.execute(select(func.count(Item.id)))).scalar() or 0
    total_wh = (await db.execute(select(func.count(Warehouse.id)))).scalar() or 0
    under = (await db.execute(
        select(func.count(Item.id)).join(StockLevel, StockLevel.item_id == Item.id)
        .where(StockLevel.qty < Item.min_stock).where(Item.min_stock > 0)
    )).scalar() or 0
    above = (await db.execute(
        select(func.count(Item.id)).join(StockLevel, StockLevel.item_id == Item.id)
        .where(StockLevel.qty > Item.max_stock).where(Item.max_stock > 0)
    )).scalar() or 0
    cutoff = datetime.utcnow() - timedelta(days=30)
    moves_30 = (await db.execute(select(func.count(Movement.id)).where(Movement.occurred_at >= cutoff))).scalar() or 0

    top_r = await db.execute(
        select(Item.name, func.sum(Movement.qty).label("total"))
        .join(Movement, Movement.item_id == Item.id)
        .where(Movement.kind.in_(["OUT", "CONSUME"])).where(Movement.occurred_at >= cutoff)
        .group_by(Item.name).order_by(func.sum(Movement.qty).desc()).limit(5)
    )
    top = [{"name": n, "qty": float(t)} for n, t in top_r.all()]

    value_r = await db.execute(
        select(func.coalesce(func.sum(StockLevel.qty * Item.cost), 0))
        .join(Item, Item.id == StockLevel.item_id)
    )
    stock_value = Decimal(str(value_r.scalar() or 0))

    # Health score simple
    score = 100
    if total_items == 0:
        score = 0
    else:
        pct_under = under / max(1, total_items)
        pct_above = above / max(1, total_items)
        score -= int(pct_under * 60)
        score -= int(pct_above * 30)
        if moves_30 == 0 and total_items > 10:
            score -= 10
        score = max(0, min(100, score))

    recs = []
    if under:
        recs.append(f"{under} artículos por debajo del mínimo — revisar reabastecimiento.")
    if above:
        recs.append(f"{above} artículos sobre el máximo — sobrestock, riesgo de merma.")
    if moves_30 == 0 and total_items > 0:
        recs.append("Sin movimientos en 30 días — validar que los POS/ERP estén emitiendo eventos.")
    if total_wh == 0:
        recs.append("No hay almacenes registrados — crea el primero.")
    verdict = "Excelente" if score >= 85 else "Bueno" if score >= 70 else "Atención" if score >= 50 else "Crítico"

    return S.ViabilityReport(
        tenant_id=UUID(tenant_id), total_items=total_items, total_warehouses=total_wh,
        items_under_min=under, items_above_max=above, movements_last_30d=moves_30,
        top_consumers_last_30d=top, stock_value_mxn=stock_value,
        health_score=score, verdict=verdict, recommendations=recs,
    )


# ─────────────────────────────────────────────────────
# DEMO SEED (tiendita, paquetería, restaurante, constructora)
# ─────────────────────────────────────────────────────
@router.post("/demo/seed")
async def seed_demo(industry: str = "store", db: AsyncSession = Depends(get_sql_db)):
    """Crea un tenant demo con datos reales del vertical elegido."""
    from modules.inventory.services.demo import seed_for_industry
    return await seed_for_industry(db, industry)
