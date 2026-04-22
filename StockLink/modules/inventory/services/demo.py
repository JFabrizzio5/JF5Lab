"""Demo seed — crea tenants con datos realistas por vertical.

Verticales soportados:
 - store        (tiendita abarrotes MX)
 - shipping     (paquetería / hub logística)
 - restaurant   (fonda / restaurante)
 - construction (obra civil / ferretería)
"""
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from modules.inventory.models import (
    Tenant, Plan, TenantPlan, Warehouse, Location, Category, Supplier,
    Item, StockLevel, Movement, Label, Employee,
)


DEMOS = {
    "store": {
        "name": "Tiendita Don Memo",
        "rfc": "DMM010101AB1",
        "warehouse": ("TDA-01", "Tienda principal", "Av. Insurgentes 250, CDMX", "shelf"),
        "locations": [
            ("MOSTRADOR", "Mostrador", "aisle"),
            ("BOD", "Bodega trasera", "zone"),
            ("VITRINA", "Vitrina refrigerada", "shelf"),
        ],
        "categories": [("ABT", "Abarrotes"), ("BEB", "Bebidas"), ("BOT", "Botanas"), ("LIM", "Limpieza")],
        "items": [
            ("7501055363057", "Coca-Cola 600ml", "BEB", "pieza", 24, 100, 16.50, 23.00),
            ("7501000112395", "Sabritas Original 45g", "BOT", "pieza", 20, 80, 10.00, 16.00),
            ("7501030459873", "Maruchan res 64g", "ABT", "pieza", 15, 60, 12.00, 19.00),
            ("7501008000011", "Bimbo pan blanco gde", "ABT", "pieza", 6, 30, 42.00, 59.00),
            ("7501055360055", "Agua Ciel 1L", "BEB", "pieza", 12, 60, 8.50, 14.00),
            ("7501030403012", "Jabón Zote 400g", "LIM", "pieza", 10, 40, 21.00, 29.00),
            ("7501000674008", "Pan Tía Rosa Gansito", "BOT", "pieza", 12, 60, 14.00, 20.00),
        ],
    },
    "shipping": {
        "name": "PaqueExpress Norte",
        "rfc": "PEN120315ZZ1",
        "warehouse": ("HUB-MTY", "Hub Monterrey", "Carretera Nacional KM 12", "hub"),
        "locations": [
            ("RECEPCION", "Recepción paquetes", "zone"),
            ("SORT-A", "Clasificación ruta A", "aisle"),
            ("SORT-B", "Clasificación ruta B", "aisle"),
            ("SALIDA", "Andén de salida", "zone"),
            ("TRUCK-01", "Camioneta 01", "truck"),
        ],
        "categories": [("PAQ", "Paquetes"), ("SOBRE", "Sobres"), ("FRAG", "Frágil")],
        "items": [
            ("PKG-SM", "Paquete Chico hasta 2kg", "PAQ", "pieza", 100, 2000, 0, 99),
            ("PKG-MD", "Paquete Mediano 2-5kg", "PAQ", "pieza", 50, 1000, 0, 189),
            ("PKG-LG", "Paquete Grande 5-15kg", "PAQ", "pieza", 30, 500, 0, 349),
            ("ENV-DOC", "Sobre Documento", "SOBRE", "pieza", 200, 3000, 0, 55),
            ("FRAG-ELEC", "Frágil Electrónica", "FRAG", "pieza", 20, 300, 0, 249),
        ],
    },
    "restaurant": {
        "name": "Fonda La Esquina",
        "rfc": "FLE150820XY7",
        "warehouse": ("REST-01", "Restaurante Centro", "5 de Mayo 88", "kitchen"),
        "locations": [
            ("COCINA", "Cocina caliente", "zone"),
            ("FRIA", "Cámara fría", "zone"),
            ("SECOS", "Almacén secos", "shelf"),
            ("BARRA", "Barra de bebidas", "shelf"),
        ],
        "categories": [("CAR", "Carnes"), ("VEG", "Verduras"), ("SEC", "Secos"), ("BEB", "Bebidas")],
        "items": [
            ("RES-ARR", "Arrachera res kg", "CAR", "kg", 5, 50, 220.00, 0),
            ("POLL-PEC", "Pechuga pollo kg", "CAR", "kg", 8, 60, 110.00, 0),
            ("TOR-HAR", "Tortilla harina paq", "SEC", "pieza", 20, 200, 26.00, 0),
            ("JIT-R", "Jitomate roma kg", "VEG", "kg", 10, 50, 18.00, 0),
            ("CEB-B", "Cebolla blanca kg", "VEG", "kg", 5, 30, 22.00, 0),
            ("AGU-H", "Aguacate hass kg", "VEG", "kg", 6, 40, 65.00, 0),
            ("LIM-P", "Limón persa kg", "VEG", "kg", 4, 25, 28.00, 0),
            ("CHIL-J", "Chile jalapeño kg", "VEG", "kg", 2, 15, 32.00, 0),
            ("COC-600", "Coca-Cola 600ml", "BEB", "pieza", 24, 120, 16.50, 28.00),
            ("VASO-DES", "Vaso desechable 16oz", "SEC", "pieza", 100, 1000, 1.20, 0),
        ],
    },
    "construction": {
        "name": "Constructora Norte SA",
        "rfc": "CNO110505TT4",
        "warehouse": ("OBRA-A", "Obra Torre A", "Av. Revolución 1500", "site"),
        "locations": [
            ("BOD-HERR", "Bodega herramienta", "zone"),
            ("PATIO", "Patio materiales", "zone"),
            ("PISO-1", "Piso 1 en curso", "zone"),
            ("PISO-2", "Piso 2 en curso", "zone"),
        ],
        "categories": [("HER", "Herramienta"), ("MAT", "Material"), ("EPP", "Seguridad")],
        "items": [
            ("CEM-50", "Cemento gris 50kg", "MAT", "bulto", 50, 500, 285.00, 0),
            ("VAR-38", "Varilla 3/8\" 12m", "MAT", "pieza", 100, 2000, 165.00, 0),
            ("ARE-M3", "Arena m3", "MAT", "m3", 20, 200, 520.00, 0),
            ("GRV-M3", "Grava m3", "MAT", "m3", 20, 200, 480.00, 0),
            ("TAL-INAL", "Taladro inalámbrico", "HER", "pieza", 2, 20, 2800.00, 0),
            ("MAR-DEM", "Marro demolición", "HER", "pieza", 2, 10, 580.00, 0),
            ("CASC-BLA", "Casco blanco", "EPP", "pieza", 20, 200, 180.00, 0),
            ("GUA-CAR", "Guantes carnaza par", "EPP", "par", 50, 500, 85.00, 0),
            ("BOT-SEG", "Botas seguridad par", "EPP", "par", 10, 60, 650.00, 0),
        ],
    },
}


async def _ensure_plans(db: AsyncSession):
    exists = (await db.execute(select(Plan))).first()
    if exists:
        return
    plans = [
        Plan(id="free", name="Gratis", price_mxn=0, max_warehouses=1, max_items=100, max_users=2,
             nfc_enabled=False, webhooks_enabled=False, attendance_enabled=False,
             description="Para probar: 1 almacén, 100 SKUs, 2 usuarios. Barcode/QR básicos."),
        Plan(id="starter", name="Starter", price_mxn=499, max_warehouses=3, max_items=2000, max_users=5,
             nfc_enabled=False, webhooks_enabled=True, attendance_enabled=True, featured=False,
             description="Ideal tiendita o fonda: 3 almacenes, 2 mil SKUs, QR ilimitado, asistencias, Excel."),
        Plan(id="pro", name="Pro", price_mxn=1499, max_warehouses=10, max_items=20000, max_users=15,
             nfc_enabled=True, webhooks_enabled=True, attendance_enabled=True, featured=True,
             description="Para cadena, taller, paquetería: NFC, webhooks (POS/ERP), 10 almacenes, 20k SKUs."),
        Plan(id="enterprise", name="Enterprise", price_mxn=4999, max_warehouses=999, max_items=999999, max_users=999,
             nfc_enabled=True, webhooks_enabled=True, attendance_enabled=True,
             description="Constructoras, franquicias, hubs logísticos. CFDI, SSO, multi-región, SLA 99.9%."),
    ]
    for p in plans:
        db.add(p)
    await db.commit()


async def seed_for_industry(db: AsyncSession, industry: str):
    await _ensure_plans(db)
    if industry not in DEMOS:
        return {"error": f"industry desconocido: {list(DEMOS)}"}

    d = DEMOS[industry]
    # Crear tenant
    t = Tenant(name=d["name"], industry=industry, rfc=d["rfc"], contact_email=f"demo@{industry}.stocklink.mx")
    db.add(t)
    await db.flush()
    db.add(TenantPlan(tenant_id=t.id, plan_id="starter", current_period_end=datetime.utcnow() + timedelta(days=30)))

    # Activar RLS context para el tenant
    await db.execute(text("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=str(t.id)))

    # Warehouse + locations
    wh_code, wh_name, wh_addr, wh_kind = d["warehouse"]
    wh = Warehouse(tenant_id=t.id, code=wh_code, name=wh_name, address=wh_addr, kind=wh_kind)
    db.add(wh)
    await db.flush()

    loc_map = {}
    for code, name, kind in d["locations"]:
        l = Location(tenant_id=t.id, warehouse_id=wh.id, code=code, name=name, kind=kind, path=f"{wh_code}/{code}")
        db.add(l)
        await db.flush()
        loc_map[code] = l.id

    # Categorías
    cat_map = {}
    for code, name in d["categories"]:
        c = Category(tenant_id=t.id, code=code, name=name)
        db.add(c)
        await db.flush()
        cat_map[code] = c.id

    # Items + stock inicial
    primary_loc = list(loc_map.values())[0]
    first_item_id = None
    for row in d["items"]:
        barcode, name, cat_code, unit, min_s, max_s, cost, price = row
        it = Item(
            tenant_id=t.id, sku=barcode, name=name, category_id=cat_map.get(cat_code),
            unit=unit, barcode=barcode, min_stock=Decimal(str(min_s)), max_stock=Decimal(str(max_s)),
            cost=Decimal(str(cost)), price=Decimal(str(price)),
        )
        db.add(it)
        await db.flush()
        if first_item_id is None:
            first_item_id = it.id
        sl = StockLevel(tenant_id=t.id, item_id=it.id, location_id=primary_loc, qty=Decimal(str(min_s * 2)))
        db.add(sl)
        # Movement inicial de carga
        db.add(Movement(tenant_id=t.id, item_id=it.id, to_location_id=primary_loc, qty=sl.qty, kind="IN",
                        reason="Carga inicial demo", ref_type="seed"))
        # Label QR por item
        db.add(Label(tenant_id=t.id, kind="QR", code=f"SKU-{barcode}", item_id=it.id, metadata_json={"auto": True}))

    # Empleados + asistencia demo
    employees = [
        ("EMP-001", "Ana López", "supervisor"),
        ("EMP-002", "Luis Pérez", "operador"),
        ("EMP-003", "María Hernández", "operador"),
    ]
    for code, name, role in employees:
        e = Employee(tenant_id=t.id, code=code, name=name, role=role, email=f"{code.lower()}@{industry}.demo")
        db.add(e)
        await db.flush()
        db.add(Label(tenant_id=t.id, kind="QR", code=f"EMP-{code}", employee_id=e.id, metadata_json={"auto": True}))

    await db.commit()

    return {
        "tenant_id": str(t.id), "industry": industry, "name": d["name"],
        "warehouse": wh_code, "locations": list(loc_map.keys()),
        "items": len(d["items"]), "employees": len(employees),
        "hint": f"Guarda este tenant_id y úsalo como header X-Tenant-Id.",
    }
