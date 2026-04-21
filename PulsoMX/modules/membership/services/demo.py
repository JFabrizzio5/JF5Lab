"""Seed demo para PulsoMX — 4 verticales."""
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from modules.membership.models import (
    Tenant, Plan, TenantPlan, Venue, Room, Member, MembershipPlan, Membership,
    Instructor, ClassTemplate, ClassSession, CheckIn,
)


DEMOS = {
    "gym": {
        "name": "Pulso Fit · Roma Norte",
        "slug": "pulso-fit-roma",
        "brand_color": "#7c3aed",
        "venue": ("Pulso Fit Roma", "Av. Álvaro Obregón 120, Roma Norte, CDMX", "CDMX", 120),
        "rooms": [("Piso principal", 120, "floor"), ("Sala cycling", 24, "cycling"), ("Zona crossfit", 20, "open_space")],
        "plans": [
            ("Mensual Estándar", 899, "month", None, 30, "#7c3aed", ["Acceso ilimitado", "Clases grupales", "Casilleros"]),
            ("Mensual Plus",    1299, "month", None, 30, "#ec4899", ["Todo lo del Estándar", "Entrenador 1-a-1 (2x mes)", "Toallas"]),
            ("Paquete 10 visitas", 899, "visits", 10, 60, "#f59e0b", ["10 entradas flexibles", "Sin compromiso"]),
            ("Anual Premium",  9490, "year", None, 365, "#10b981", ["Todo incluido", "Invitados 2x mes", "Smoothie bar gratis"]),
        ],
        "instructors": [("IN-01", "Carla Rodríguez", "HIIT, Crossfit"), ("IN-02", "Mario Díaz", "Cycling, Cardio")],
        "templates": [("Crossfit Lunes", "crossfit", 60, 20, "#ef4444"), ("Cycling Power", "cycling", 45, 24, "#f59e0b"), ("HIIT Express", "hiit", 30, 25, "#7c3aed")],
    },
    "yoga": {
        "name": "Soma Yoga Studio",
        "slug": "soma-yoga",
        "brand_color": "#10b981",
        "venue": ("Soma Studio Condesa", "Amsterdam 88, Condesa, CDMX", "CDMX", 40),
        "rooms": [("Sala Om", 22, "mat"), ("Sala Shanti", 18, "mat")],
        "plans": [
            ("Mensual Ilimitado", 1499, "month", None, 30, "#10b981", ["Clases ilimitadas", "Mat incluido", "Tés de bienvenida"]),
            ("Paquete 8 clases",  1099, "visits", 8, 45, "#0891b2", ["8 clases", "Válido 45 días"]),
            ("Drop-in",            180, "one_time", 1, 1, "#64748b", ["Una sola clase"]),
        ],
        "instructors": [("IN-01", "Laura Méndez", "Vinyasa, Yin"), ("IN-02", "Diego Castro", "Ashtanga, Power")],
        "templates": [("Vinyasa Flow", "yoga_flow", 60, 22, "#10b981"), ("Yin Yoga", "yoga_flow", 75, 18, "#7c3aed"), ("Power Yoga", "yoga_flow", 60, 22, "#ef4444")],
    },
    "coworking": {
        "name": "Nodo Coworking",
        "slug": "nodo-coworking",
        "brand_color": "#0ea5e9",
        "venue": ("Nodo Polanco", "Presidente Masaryk 40, Polanco, CDMX", "CDMX", 80),
        "rooms": [("Open Space", 60, "open_space"), ("Sala Aurora (8)", 8, "meeting"), ("Sala Boreal (4)", 4, "meeting")],
        "plans": [
            ("Hot Desk mensual", 3999, "month", None, 30, "#0ea5e9", ["Escritorio flex", "Internet 500Mb", "Café ilimitado", "Impresiones 200/mes"]),
            ("Dedicated Desk",   6999, "month", None, 30, "#7c3aed", ["Escritorio fijo", "Locker", "Dirección fiscal"]),
            ("Day Pass",          399, "one_time", 1, 1, "#f59e0b", ["Un día completo", "Sin compromiso"]),
        ],
        "instructors": [("HOST-01", "Roberto Silva", "Community Manager")],
        "templates": [("Networking Breakfast", "event", 60, 30, "#f59e0b"), ("Founder Roundtable", "event", 90, 12, "#7c3aed")],
    },
    "dojo": {
        "name": "Dojo Kihon · Bushido",
        "slug": "dojo-kihon",
        "brand_color": "#ef4444",
        "venue": ("Dojo Kihon Del Valle", "Insurgentes Sur 1800, Del Valle", "CDMX", 50),
        "rooms": [("Tatami Principal", 40, "mat"), ("Área de impacto", 12, "open_space")],
        "plans": [
            ("Mensual Adultos",  1200, "month", None, 30, "#ef4444", ["4 clases/semana", "Uniforme gi incluido primer mes"]),
            ("Mensual Niños",     990, "month", None, 30, "#f59e0b", ["3 clases/semana", "Grupo 6-12 años"]),
            ("Anual Adulto",   12900, "year",  None, 365, "#7c3aed", ["Todo incluido", "Exámenes de grado sin costo"]),
        ],
        "instructors": [("SENSEI-01", "Sensei Akira Tanaka", "Karate Shotokan 5° dan"), ("SENSEI-02", "Sensei Ana Ruiz", "Brazilian Jiu-Jitsu")],
        "templates": [("Karate Adultos", "karate", 75, 22, "#ef4444"), ("BJJ Fundamentals", "jiu_jitsu", 90, 18, "#7c3aed"), ("Niños Shotokan", "karate", 60, 20, "#f59e0b")],
    },
}


MEMBER_NAMES = [
    ("Ana", "Ramírez"), ("Carlos", "González"), ("María", "López"), ("Juan", "Pérez"),
    ("Sofía", "Hernández"), ("Diego", "Torres"), ("Valentina", "Flores"), ("Luis", "Sánchez"),
    ("Camila", "Rodríguez"), ("Santiago", "Martínez"), ("Isabella", "García"), ("Mateo", "Díaz"),
]


async def _ensure_plans(db: AsyncSession):
    exists = (await db.execute(select(Plan))).first()
    if exists:
        return
    plans = [
        Plan(id="free", name="Gratis", price_mxn=0, max_members=30, max_venues=1, max_staff=2,
             has_bookings=True, has_payments=False, has_whatsapp=False, has_custom_brand=False,
             description="Para empezar: 30 miembros, QR check-in, agenda de clases."),
        Plan(id="starter", name="Starter", price_mxn=699, max_members=200, max_venues=1, max_staff=5,
             has_bookings=True, has_payments=True, has_whatsapp=False, has_custom_brand=False, featured=False,
             description="Perfecto para estudios pequeños. Cobros con Stripe/Conekta incluidos."),
        Plan(id="pro", name="Pro", price_mxn=1499, max_members=1000, max_venues=3, max_staff=15,
             has_bookings=True, has_payments=True, has_whatsapp=True, has_custom_brand=True, featured=True,
             description="Cadena con varias sucursales. WhatsApp + branding propio + API."),
        Plan(id="enterprise", name="Enterprise", price_mxn=4999, max_members=999999, max_venues=999, max_staff=999,
             has_bookings=True, has_payments=True, has_whatsapp=True, has_custom_brand=True,
             description="Franquicias. CFDI 4.0, SSO, multi-región, integración a medida."),
    ]
    for p in plans:
        db.add(p)
    await db.commit()


async def seed_for_industry(db: AsyncSession, industry: str):
    await _ensure_plans(db)
    if industry not in DEMOS:
        return {"error": f"industry desconocido: {list(DEMOS)}"}

    d = DEMOS[industry]
    t = Tenant(
        name=d["name"], slug=d["slug"], industry=industry,
        brand_color=d["brand_color"], contact_email=f"demo@{d['slug']}.mx",
        contact_phone="+525555000000",
    )
    db.add(t)
    await db.flush()
    db.add(TenantPlan(tenant_id=t.id, plan_id="starter", status="trialing",
                     trial_end=datetime.utcnow() + timedelta(days=14),
                     current_period_end=datetime.utcnow() + timedelta(days=30)))
    await db.execute(text("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=str(t.id)))

    # Venue + rooms
    vname, vaddr, vcity, vcap = d["venue"]
    venue = Venue(tenant_id=t.id, name=vname, address=vaddr, city=vcity, capacity=vcap)
    db.add(venue)
    await db.flush()
    room_ids = []
    for rname, rcap, rkind in d["rooms"]:
        r = Room(tenant_id=t.id, venue_id=venue.id, name=rname, capacity=rcap, kind=rkind)
        db.add(r)
        await db.flush()
        room_ids.append(r.id)

    # Membership plans
    plan_ids = []
    for pname, price, interval, visits, duration, color, perks in d["plans"]:
        p = MembershipPlan(
            tenant_id=t.id, name=pname, price_mxn=Decimal(str(price)),
            billing_interval=interval, visits_included=visits,
            duration_days=duration, color=color, perks=perks,
            description=f"{pname} — " + ", ".join(perks[:2]),
        )
        db.add(p)
        await db.flush()
        plan_ids.append(p.id)

    # Instructors
    instr_ids = []
    for code, name, specialty in d["instructors"]:
        i = Instructor(tenant_id=t.id, code=code, name=name, specialty=specialty)
        db.add(i)
        await db.flush()
        instr_ids.append(i.id)

    # Class templates
    tmpl_ids = []
    for tname, tkind, tdur, tcap, tcolor in d["templates"]:
        tpl = ClassTemplate(tenant_id=t.id, name=tname, kind=tkind,
                           duration_minutes=tdur, capacity=tcap, color=tcolor)
        db.add(tpl)
        await db.flush()
        tmpl_ids.append(tpl.id)

    # Sessions próximos 7 días (3 clases al día)
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    for day in range(7):
        for hour_off, tmpl_id, instr_idx, room_idx in [(9, 0, 0, 0), (18, 1, 1 % len(instr_ids), 1 % len(room_ids)), (20, 2 % len(tmpl_ids), 0, 0)]:
            starts = now + timedelta(days=day, hours=hour_off - now.hour)
            db.add(ClassSession(
                tenant_id=t.id, template_id=tmpl_ids[tmpl_id],
                instructor_id=instr_ids[instr_idx], room_id=room_ids[room_idx],
                starts_at=starts, ends_at=starts + timedelta(minutes=60), capacity=20,
            ))

    # Members + memberships activas + algunos check-ins
    for idx, (fn, ln) in enumerate(MEMBER_NAMES):
        code = f"PM-{1000 + idx:04d}"
        m = Member(
            tenant_id=t.id, code=code,
            first_name=fn, last_name=ln,
            email=f"{fn.lower()}.{ln.lower()}@demo.mx",
            phone=f"+52555{1000000 + idx}",
            joined_at=datetime.utcnow() - timedelta(days=60 - idx * 3),
        )
        db.add(m)
        await db.flush()
        # Suscribir al primer plan
        if plan_ids:
            db.add(Membership(
                tenant_id=t.id, member_id=m.id, membership_plan_id=plan_ids[idx % len(plan_ids)],
                status="active", started_at=datetime.utcnow() - timedelta(days=30),
                expires_at=datetime.utcnow() + timedelta(days=30),
                visits_remaining=10 if idx % 4 == 2 else None,
            ))
        # Check-ins últimos días
        for days_ago in [0, 1, 2, 4]:
            if (idx + days_ago) % 3 == 0:
                db.add(CheckIn(
                    tenant_id=t.id, member_id=m.id, venue_id=venue.id,
                    at=datetime.utcnow() - timedelta(days=days_ago, hours=2),
                    method="QR",
                ))

    await db.commit()

    return {
        "tenant_id": str(t.id), "industry": industry, "name": d["name"],
        "slug": d["slug"], "brand_color": d["brand_color"],
        "venue": vname, "rooms": len(d["rooms"]),
        "membership_plans": len(d["plans"]), "members": len(MEMBER_NAMES),
        "hint": "Usa X-Tenant-Id en headers o ?tenant=<uuid> en URLs.",
    }
