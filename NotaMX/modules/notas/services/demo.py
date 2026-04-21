"""Seed demo NotaMX - 4 verticales: freelance, consultorio, abogados, agencia."""
from __future__ import annotations
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from modules.notas.models import (
    Tenant, Plan, TenantPlan, Customer, Product, Note, NoteItem, Payment, CfdiDocument,
    WhatsappTemplate,
)

DEMOS = {
    "freelance": {
        "name": "Estudio Mora - Diseño Web",
        "slug": "estudio-mora",
        "brand_color": "#10b981",
        "industry": "freelance",
        "rfc": "MOGM900101AB1",
        "razon_social": "MARTINEZ MORA GUSTAVO",
        "regimen_fiscal": "612",
        "codigo_postal": "06140",
        "contact_email": "hola@estudiomora.mx",
        "contact_phone": "+525544221188",
        "whatsapp_number": "+525544221188",
        "customers": [
            ("Café Oaxaca Roma", "OXR210310HM4", "hola@cafeoaxaca.mx", "+525566110011"),
            ("Fernanda Torres", "TOFE890512MDF", "fer@torres.com", "+525511223344"),
            ("Mezcalería La Nueve", "LNU180901AB9", "admin@lanueve.mx", "+525512345678"),
            ("Studio B Fotografía", "SBF190102CD3", "hi@studiob.mx", "+525598765432"),
            ("Luis Arana Consultor", "AALU800201XYZ", "luis@arana.com", "+525511119999"),
            ("Arquitectura Polanco", "APO200710EF1", "contacto@arquipolanco.mx", "+525533445566"),
            ("Moda Condesa", "MCO220801GH5", "ventas@modacondesa.mx", "+525577889900"),
            ("Pastelería Dulce Luna", "DLN210403KL9", "hola@dulceluna.mx", "+525522334455"),
        ],
        "products": [
            ("WEB-LOGO", "Diseño de logotipo", "Identidad visual completa (3 propuestas + manual)", 4500, "servicio"),
            ("WEB-LAND", "Landing page", "Landing de 1 seccion con formulario", 8500, "servicio"),
            ("WEB-SITE", "Sitio web corporativo", "Hasta 6 secciones, CMS y hosting 1 año", 22000, "servicio"),
            ("WEB-ECOM", "Tienda en línea", "Shopify o WooCommerce hasta 50 productos", 38000, "servicio"),
            ("WEB-MNT", "Mantenimiento mensual", "Actualizaciones, backup y soporte (20h)", 1800, "mes"),
            ("DEV-HR",  "Hora de desarrollo", "Desarrollo frontend o backend", 650, "hora"),
            ("DES-POST", "Post redes sociales", "Diseño de post para IG/FB", 350, "pieza"),
            ("DES-BRAND", "Paquete branding", "Logo + paleta + tipografías + 10 plantillas", 12000, "paquete"),
            ("SEO-AUD",  "Auditoría SEO", "Informe técnico + plan de acción 3 meses", 5500, "servicio"),
            ("CONS-HR",  "Consultoría digital", "Sesión estratégica 60min", 1200, "hora"),
        ],
    },
    "consultorio": {
        "name": "Dental Studio Condesa",
        "slug": "dental-condesa",
        "brand_color": "#0ea5e9",
        "industry": "consultorio",
        "rfc": "DSC190505XYZ",
        "razon_social": "DENTAL STUDIO CONDESA S.C.",
        "regimen_fiscal": "601",
        "codigo_postal": "06140",
        "contact_email": "citas@dentalcondesa.mx",
        "contact_phone": "+525578902345",
        "whatsapp_number": "+525578902345",
        "customers": [
            ("Mariana Vega", "VEGM920511MDF", "mariana@gmail.com", "+525522229999"),
            ("Roberto Díaz", "DIRO850211HDF", "roberto@outlook.com", "+525533330011"),
            ("Carla Nuñez", "NUCA790820MDF", "carla@yahoo.com", "+525544557788"),
            ("Familia Herrera", "HERC700401XYZ", "herrera.fam@gmail.com", "+525566778899"),
            ("Andrés Cruz", "CRAN951122HDF", "andres@hotmail.com", "+525500112233"),
            ("Isabel Moreno", "MOIS880303MDF", "isabel@mail.com", "+525512340987"),
        ],
        "products": [
            ("ODO-LIM", "Limpieza dental", "Profilaxis + ultrasonido", 800, "servicio"),
            ("ODO-EXT", "Extracción simple", "Pieza dental sin complicaciones", 1500, "servicio"),
            ("ODO-EXQ", "Extracción quirúrgica", "Incluye sutura", 3500, "servicio"),
            ("ODO-RES", "Resina estética", "Por diente", 1200, "servicio"),
            ("ODO-END", "Endodoncia unirradicular", "Tratamiento de conductos 1 raíz", 4500, "servicio"),
            ("ODO-BLQ", "Blanqueamiento láser", "Sesión completa en consultorio", 4200, "servicio"),
            ("ODO-ORT", "Ortodoncia paquete", "Brackets metálicos, 18 meses", 15000, "paquete"),
            ("ODO-ORQ", "Ortodoncia estética", "Brackets cerámicos, 18 meses", 22000, "paquete"),
            ("ODO-CON", "Consulta inicial", "Revisión + radiografía panorámica", 450, "servicio"),
        ],
    },
    "abogados": {
        "name": "Despacho Legal Hernández & Asociados",
        "slug": "hernandez-legal",
        "brand_color": "#7c3aed",
        "industry": "abogados",
        "rfc": "HAL150615QQ8",
        "razon_social": "HERNANDEZ Y ASOCIADOS S.C.",
        "regimen_fiscal": "601",
        "codigo_postal": "11000",
        "contact_email": "contacto@hernandezlegal.mx",
        "contact_phone": "+525588776644",
        "whatsapp_number": "+525588776644",
        "customers": [
            ("Transportes Valle SA", "TVA050303AB1", "finanzas@tvalle.mx", "+525533221100"),
            ("Constructora RAM", "CRM120214CD2", "admin@ramconstructora.mx", "+525522110099"),
            ("Patricia Zúñiga", "ZUPA800716MDF", "patricia@gmail.com", "+525511220033"),
            ("Innovatec SA", "INN190101EF5", "cobros@innovatec.mx", "+525544332211"),
            ("Raúl Sánchez", "SARA851212HDF", "raul@outlook.com", "+525566778811"),
            ("Distribuidora Norte", "DNO170503GH2", "admin@distnorte.mx", "+525599887766"),
        ],
        "products": [
            ("LEG-CON", "Consulta legal", "Orientación 60min", 1500, "hora"),
            ("LEG-HON", "Honorarios fijos", "Caso civil con monto fijo pactado", 35000, "paquete"),
            ("LEG-MEN", "Iguala mensual", "Asesoría fiscal y corporativa (hasta 10h)", 8500, "mes"),
            ("LEG-JUI", "Representación en juicio", "Tramite primera instancia", 55000, "paquete"),
            ("LEG-DOC", "Revisión contractual", "Contrato hasta 20 págs", 3800, "servicio"),
            ("LEG-AMP", "Juicio de amparo", "Elaboración y seguimiento", 22000, "servicio"),
            ("LEG-NOT", "Escrituración fedataria", "Compraventa inmueble (sin costos fedatario)", 18000, "servicio"),
        ],
    },
    "agencia": {
        "name": "Cometa Creativa Agencia",
        "slug": "cometa-creativa",
        "brand_color": "#ec4899",
        "industry": "agencia",
        "rfc": "CCA200801RR7",
        "razon_social": "COMETA CREATIVA AGENCIA S.A.S.",
        "regimen_fiscal": "601",
        "codigo_postal": "03103",
        "contact_email": "hola@cometacreativa.mx",
        "contact_phone": "+525544994499",
        "whatsapp_number": "+525544994499",
        "customers": [
            ("Pan de Muerto SA", "PMU180912AB0", "marketing@pandemuerto.mx", "+525533445566"),
            ("Tequila Sol Bravo", "TSB150210CD1", "brand@solbravo.mx", "+525511223344"),
            ("Zapatería Andaluz", "ZAN090505EF3", "ceo@andaluz.mx", "+525599001122"),
            ("Startup Bloom", "SBL220101GH7", "growth@bloom.mx", "+525588990033"),
            ("Clínica Vitalis", "CVI170613KL9", "mercadotecnia@vitalis.mx", "+525544330022"),
        ],
        "products": [
            ("AGC-RET", "Retainer mensual premium", "Gestión IG/FB/TT + 12 posts + 4 reels", 28000, "mes"),
            ("AGC-ADS", "Fee gestión ADS", "Administración de pauta (10% de inversión)", 6500, "mes"),
            ("AGC-CAM", "Campaña de lanzamiento", "Estrategia + creatividades + pauta 30 días", 48000, "paquete"),
            ("AGC-VID", "Producción video comercial", "Hasta 90 seg, 1 día de grabación", 35000, "servicio"),
            ("AGC-FOT", "Sesión fotográfica producto", "Hasta 20 tomas editadas", 8500, "servicio"),
            ("AGC-EST", "Estrategia de marca", "Workshop + documento de posicionamiento", 22000, "paquete"),
            ("AGC-LAN", "Landing alta conversión", "Landing + copy + integración CRM", 18000, "servicio"),
        ],
    },
}


WA_TEMPLATES = [
    ("nota_nueva", "Hola {{customer_name}}, te compartimos la nota {{number}} por {{total}}. Puedes verla y pagarla aquí: {{link}}", ["customer_name", "number", "total", "link"], "nota"),
    ("recordatorio", "Hola {{customer_name}}, un recordatorio amistoso de la nota {{number}} por {{total}}. {{link}}", ["customer_name", "number", "total", "link"], "recordatorio"),
    ("gracias_pago", "Gracias {{customer_name}} por tu pago de {{total}}. Tu CFDI estará listo en breve.", ["customer_name", "total"], "cobro"),
]


async def _ensure_plans(db: AsyncSession):
    exists = (await db.execute(select(Plan))).first()
    if exists:
        return
    plans = [
        Plan(id="free", name="Gratis", price_mxn=0, max_notes_month=5, max_customers=20,
             has_whatsapp=False, has_cfdi=False, has_branding=False, has_api=False,
             description="Ideal para empezar: 5 notas por mes, link público de pago."),
        Plan(id="pro", name="Pro", price_mxn=299, max_notes_month=60, max_customers=200,
             has_whatsapp=True, has_cfdi=True, has_branding=False, has_api=False, featured=False,
             description="Notas ilimitadas dentro del plan, WhatsApp y CFDI 4.0 automático."),
        Plan(id="growth", name="Growth", price_mxn=999, max_notes_month=500, max_customers=2000,
             has_whatsapp=True, has_cfdi=True, has_branding=True, has_api=False, featured=True,
             description="PYMEs en crecimiento. Branding propio, recordatorios WhatsApp, reportes."),
        Plan(id="business", name="Business", price_mxn=2499, max_notes_month=999999, max_customers=999999,
             has_whatsapp=True, has_cfdi=True, has_branding=True, has_api=True,
             description="Negocios con volumen. API, multi-usuario, SLA prioritario."),
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
        name=d["name"], slug=f"{d['slug']}-{int(datetime.utcnow().timestamp())}",
        industry=d["industry"], brand_color=d["brand_color"],
        rfc=d["rfc"], razon_social=d["razon_social"],
        regimen_fiscal=d["regimen_fiscal"], codigo_postal=d["codigo_postal"],
        contact_email=d["contact_email"], contact_phone=d["contact_phone"],
        whatsapp_number=d["whatsapp_number"],
    )
    db.add(t); await db.flush()
    # Activar contexto RLS al tenant recien creado
    await db.execute(text("SELECT set_config('app.tenant_id', :tid, false)").bindparams(tid=str(t.id)))
    db.add(TenantPlan(
        tenant_id=t.id, plan_id="pro", status="trialing",
        trial_end=datetime.utcnow() + timedelta(days=14),
        current_period_end=datetime.utcnow() + timedelta(days=30),
    ))

    # Customers
    cust_objs: list[Customer] = []
    for name, rfc, email, phone in d["customers"]:
        c = Customer(
            tenant_id=t.id, name=name, rfc=rfc, email=email, phone=phone,
            whatsapp=phone, uso_cfdi="G03", regimen_fiscal="612",
            codigo_postal="06140", razon_social=name.upper(),
        )
        db.add(c); cust_objs.append(c)
    await db.flush()

    # Products
    prod_objs: list[Product] = []
    for sku, name, desc, price, unit in d["products"]:
        p = Product(
            tenant_id=t.id, sku=sku, name=name, description=desc,
            price_mxn=Decimal(str(price)), unit=unit, tax_rate=Decimal("0.16"),
            sat_product_key="80101500", sat_unit_key="E48" if unit == "servicio" else "H87",
        )
        db.add(p); prod_objs.append(p)
    await db.flush()

    # Notes - 15 mixed states
    statuses = ["draft"] * 3 + ["sent"] * 5 + ["paid"] * 6 + ["canceled"]
    random.shuffle(statuses)
    note_num = 1
    for i, status in enumerate(statuses):
        cust = random.choice(cust_objs)
        created = datetime.utcnow() - timedelta(days=random.randint(0, 45))
        n = Note(
            tenant_id=t.id,
            number=f"NT-{note_num:04d}",
            customer_id=cust.id,
            status=status,
            channel=random.choice(["whatsapp", "link", "email"]),
            valid_until=(created + timedelta(days=15)).date(),
            notes="Gracias por tu preferencia. Precios sujetos a IVA.",
            created_at=created,
            sent_at=created if status in ("sent", "paid") else None,
            paid_at=created + timedelta(days=random.randint(1, 10)) if status == "paid" else None,
        )
        db.add(n); await db.flush()
        note_num += 1

        # Items 1-3
        n_items = random.randint(1, 3)
        subtotal = Decimal("0"); tax_total = Decimal("0")
        for _ in range(n_items):
            p = random.choice(prod_objs)
            qty = Decimal(str(random.choice([1, 1, 1, 2, 3])))
            sub = qty * p.price_mxn
            tax = sub * p.tax_rate
            it = NoteItem(
                tenant_id=t.id, note_id=n.id, product_id=p.id,
                description=p.name, qty=qty, unit_price=p.price_mxn,
                tax_rate=p.tax_rate, subtotal=sub, tax=tax, total=sub + tax,
            )
            db.add(it)
            subtotal += sub; tax_total += tax
        n.subtotal = subtotal
        n.tax_total = tax_total
        n.total = subtotal + tax_total

        # Payment + CFDI if paid
        if status == "paid":
            pay = Payment(
                tenant_id=t.id, note_id=n.id, customer_id=cust.id,
                amount_mxn=n.total, provider=random.choice(["stripe", "conekta", "manual"]),
                status="succeeded", method=random.choice(["card", "oxxo", "spei"]),
                description=f"Pago {n.number}", paid_at=n.paid_at,
                created_at=n.paid_at,
            )
            db.add(pay); await db.flush()
            cfdi = CfdiDocument(
                tenant_id=t.id, related_note_id=n.id, payment_id=pay.id, customer_id=cust.id,
                serie="A", folio=str(100 + i), status="issued",
                total=n.total, uso_cfdi=cust.uso_cfdi, metodo_pago="PUE", forma_pago="03",
                uuid_sat=f"DEMO-{cust.id.hex[:8]}-{i:04d}",
                issued_at=n.paid_at, created_at=n.paid_at,
            )
            db.add(cfdi)

    # WhatsApp templates
    for name, body, vars_, cat in WA_TEMPLATES:
        db.add(WhatsappTemplate(
            tenant_id=t.id, name=name, body=body, variables=vars_, category=cat,
        ))

    await db.commit()
    await db.refresh(t)
    return {
        "tenant_id": str(t.id),
        "name": t.name,
        "slug": t.slug,
        "brand_color": t.brand_color,
        "industry": t.industry,
        "seeded": {
            "customers": len(cust_objs),
            "products": len(prod_objs),
            "notes": len(statuses),
        },
    }
