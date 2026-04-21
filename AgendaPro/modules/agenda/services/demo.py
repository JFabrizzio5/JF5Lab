"""Seed demo para AgendaPro — 4 verticales."""
from __future__ import annotations
import random
from datetime import datetime, timedelta, time, date as DateType
from decimal import Decimal
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from modules.agenda.models import (
    Tenant, Plan, TenantPlan, Staff, Service, AvailabilityRule,
    Customer, Appointment,
)


DEMOS = {
    "barber": {
        "name": "Barbería El Corte · Roma",
        "slug": "barberia-el-corte",
        "industry": "barber",
        "city": "CDMX",
        "brand_color": "#0f172a",
        "tagline": "Clásicos, precisos, puntuales.",
        "about": "Barbería de barrio desde 2014. Corte, barba y estilo sin prisas.",
        "instagram": "@barberiaelcorte",
        "staff": [
            ("Marco Aguilar", "marco", "#0f172a", "Maestro barbero. 10 años. Fade specialist."),
            ("Juan Páez", "juan", "#b45309", "Barbas y diseños. Fundador."),
            ("Ernesto Vidal", "ernesto", "#0e7490", "Corte clásico y afeitado con navaja."),
        ],
        "services": [
            ("Corte de cabello", "clasico", 30, 250, 0, False, "#0f172a"),
            ("Barba", "clasico", 20, 150, 0, False, "#b45309"),
            ("Corte + Barba", "combo", 50, 350, 100, True, "#0e7490"),
            ("Color / Tinte", "color", 60, 600, 200, True, "#7c3aed"),
            ("Corte chamacos", "ninos", 25, 180, 0, False, "#10b981"),
            ("Diseño + Línea", "diseno", 40, 400, 100, True, "#ef4444"),
        ],
        "schedule": [(d, time(10, 0), time(20, 0)) for d in range(0, 6)],  # Lun-Sáb
    },
    "dentist": {
        "name": "Clínica Dental Sonrisa",
        "slug": "clinica-sonrisa",
        "industry": "clinic",
        "city": "CDMX",
        "brand_color": "#0891b2",
        "tagline": "Sonrisas que cuidan cada detalle.",
        "about": "Clínica dental con tecnología 3D y doctores certificados.",
        "instagram": "@clinicasonrisa",
        "staff": [
            ("Dra. Fernanda Ruiz", "fer", "#0891b2", "Ortodoncia y estética dental. 12 años."),
            ("Dr. Arturo Gómez", "arturo", "#7c3aed", "Odontología general y endodoncia."),
        ],
        "services": [
            ("Limpieza dental", "general", 45, 800, 200, True, "#0891b2"),
            ("Extracción simple", "cirugia", 30, 1500, 500, True, "#ef4444"),
            ("Consulta Ortodoncia", "ortodoncia", 30, 500, 250, True, "#7c3aed"),
            ("Blanqueamiento", "estetica", 60, 4500, 1000, True, "#f59e0b"),
        ],
        "schedule": [(d, time(9, 0), time(19, 0)) for d in range(0, 5)] + [(5, time(10, 0), time(14, 0))],
    },
    "vet": {
        "name": "Vet Amigo · Del Valle",
        "slug": "vet-amigo",
        "industry": "vet",
        "city": "CDMX",
        "brand_color": "#059669",
        "tagline": "Cuidado que tu mejor amigo merece.",
        "about": "Clínica veterinaria especialista en pequeñas especies.",
        "instagram": "@vetamigomx",
        "staff": [
            ("MVZ Laura Torres", "laura", "#059669", "Medicina general y preventiva."),
            ("MVZ Pablo Sánchez", "pablo", "#0ea5e9", "Cirugía y odontología."),
        ],
        "services": [
            ("Consulta general", "consulta", 30, 400, 0, False, "#059669"),
            ("Vacuna", "prevencion", 15, 300, 0, False, "#0ea5e9"),
            ("Baño medicado", "estetica", 45, 280, 0, False, "#7c3aed"),
            ("Estética pet", "estetica", 60, 350, 100, True, "#f59e0b"),
        ],
        "schedule": [(d, time(10, 0), time(19, 0)) for d in range(0, 6)],
    },
    "coach": {
        "name": "Coach Flow · Aurora",
        "slug": "coach-flow",
        "industry": "coach",
        "city": "CDMX",
        "brand_color": "#7c3aed",
        "tagline": "Claridad, foco, resultados.",
        "about": "Coaching ejecutivo uno-a-uno. Sesiones 100% online o presenciales.",
        "instagram": "@coachflow",
        "staff": [
            ("Aurora Méndez", "aurora", "#7c3aed", "Life & executive coach. ICF PCC."),
        ],
        "services": [
            ("Sesión 1 hora", "sesion", 60, 1200, 300, True, "#7c3aed"),
            ("Paquete 4 sesiones", "paquete", 60, 4000, 1000, True, "#0891b2"),
            ("Sesión intro 30 min", "intro", 30, 0, 0, False, "#10b981"),
        ],
        "schedule": [(d, time(9, 0), time(18, 0)) for d in range(0, 5)],
    },
}


async def _ensure_plans(db: AsyncSession):
    exists = (await db.execute(select(Plan))).first()
    if exists:
        return
    plans = [
        Plan(id="free", name="Gratis", price_mxn=0, max_appointments_mo=30, max_staff=1,
             has_prepay=False, has_whatsapp=False, has_custom_brand=False, has_google_review=False,
             description="Empieza gratis: 30 citas/mes, agenda pública, recordatorios email."),
        Plan(id="pro", name="Pro", price_mxn=399, max_appointments_mo=500, max_staff=3,
             has_prepay=True, has_whatsapp=True, has_custom_brand=False, has_google_review=False,
             description="Cobros Stripe/Conekta, WhatsApp reminders, 3 profesionales.", featured=True),
        Plan(id="premium", name="Premium", price_mxn=999, max_appointments_mo=3000, max_staff=10,
             has_prepay=True, has_whatsapp=True, has_custom_brand=True, has_google_review=True,
             description="Todo Pro + branding propio, 10 pros, pedidos Google Review automáticos."),
        Plan(id="business", name="Business", price_mxn=2499, max_appointments_mo=999999, max_staff=999,
             has_prepay=True, has_whatsapp=True, has_custom_brand=True, has_google_review=True,
             description="Cadenas: multi-sucursal, CFDI 4.0, API, SLA."),
    ]
    for p in plans:
        db.add(p)
    await db.commit()


CUSTOMER_NAMES = [
    "Ana Ramírez", "Carlos González", "María López", "Juan Pérez",
    "Sofía Hernández", "Diego Torres", "Valentina Flores", "Luis Sánchez",
    "Camila Rodríguez", "Santiago Martínez", "Isabella García", "Mateo Díaz",
    "Emilia Castro", "Bruno Jiménez", "Renata Vargas", "Tomás Morales",
    "Alejandra Silva", "Gabriel Ruiz", "Daniela Ortega", "Nicolás Romero",
]


async def seed_for_industry(db: AsyncSession, industry: str):
    await _ensure_plans(db)
    if industry not in DEMOS:
        return {"error": f"industry desconocido. Usa: {list(DEMOS)}"}

    d = DEMOS[industry]

    # tenant
    t = Tenant(
        name=d["name"], slug=d["slug"], industry=d["industry"],
        city=d["city"], brand_color=d["brand_color"],
        tagline=d["tagline"], about=d["about"],
        instagram=d["instagram"],
        contact_email=f"hola@{d['slug']}.mx",
        contact_phone="+525555000111",
    )
    db.add(t); await db.flush()
    db.add(TenantPlan(tenant_id=t.id, plan_id="pro", status="trialing",
                     trial_end=datetime.utcnow() + timedelta(days=14),
                     current_period_end=datetime.utcnow() + timedelta(days=30)))

    # set tenant para RLS
    await db.execute(text("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=str(t.id)))

    # staff
    staff_objs: list[Staff] = []
    for name, slug, color, bio in d["staff"]:
        s = Staff(tenant_id=t.id, name=name, email=f"{slug}@{d['slug']}.mx",
                 phone="+525555001122", role="professional", color=color, bio=bio)
        db.add(s); await db.flush()
        staff_objs.append(s)
    staff_ids = [s.id for s in staff_objs]

    # services
    svc_objs: list[Service] = []
    for sname, cat, dur, price, deposit, requires_prepay, color in d["services"]:
        sv = Service(
            tenant_id=t.id, name=sname, category=cat,
            duration_minutes=dur, buffer_minutes=5,
            price_mxn=Decimal(str(price)), deposit_mxn=Decimal(str(deposit)),
            requires_prepay=requires_prepay, color=color,
            staff_ids=staff_ids,
        )
        db.add(sv); await db.flush()
        svc_objs.append(sv)

    # availability rules
    for s in staff_objs:
        for wday, start, end in d["schedule"]:
            db.add(AvailabilityRule(
                tenant_id=t.id, staff_id=s.id,
                weekday=wday, start_time=start, end_time=end, active=True,
            ))

    # customers + appointments próximos 7 días
    rng = random.Random(42)
    customer_objs: list[Customer] = []
    for i, full in enumerate(CUSTOMER_NAMES):
        c = Customer(
            tenant_id=t.id, name=full,
            phone=f"+52555{2000000 + i}",
            email=f"{full.lower().replace(' ', '.')}@demo.mx",
            whatsapp_optin=True,
            total_visits=rng.randint(0, 8),
            no_show_count=rng.choice([0, 0, 0, 0, 1]),
        )
        db.add(c); await db.flush()
        customer_objs.append(c)

    # 20 citas próximos 7 días
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    appts_created = 0
    for i in range(22):
        day_off = rng.randint(0, 6)
        day = now + timedelta(days=day_off)
        wd = day.weekday()
        # schedule elegible
        day_rules = [sch for sch in d["schedule"] if sch[0] == wd]
        if not day_rules:
            continue
        _, hs, he = day_rules[0]
        hour = rng.randint(hs.hour, max(hs.hour, he.hour - 1))
        minute = rng.choice([0, 15, 30, 45])
        starts = day.replace(hour=hour, minute=minute)
        svc = rng.choice(svc_objs)
        staff = rng.choice(staff_objs)
        cust = rng.choice(customer_objs)
        status = rng.choice(["confirmed", "confirmed", "confirmed", "pending_payment", "completed"])
        db.add(Appointment(
            tenant_id=t.id, customer_id=cust.id, staff_id=staff.id, service_id=svc.id,
            starts_at=starts, ends_at=starts + timedelta(minutes=svc.duration_minutes),
            status=status,
            deposit_paid=(status == "confirmed" and svc.requires_prepay),
            total=svc.price_mxn, deposit=svc.deposit_mxn,
            source="public" if i % 2 == 0 else "manual",
        ))
        appts_created += 1

    await db.commit()

    return {
        "tenant_id": str(t.id), "industry": industry, "name": d["name"],
        "slug": d["slug"], "brand_color": d["brand_color"],
        "public_url": f"http://62.72.3.139:3055/{d['slug']}",
        "staff": len(staff_objs), "services": len(svc_objs),
        "customers": len(customer_objs), "appointments": appts_created,
        "hint": "Usa X-Tenant-Id en headers O abre la URL pública (sin auth).",
    }
