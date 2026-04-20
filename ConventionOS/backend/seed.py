"""Idempotent seed script for ConventionOS demo data."""
import sys
import os
sys.path.insert(0, '/app')

from database import SessionLocal, engine, Base
import models
from auth import hash_password
from datetime import datetime
import json
import secrets

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def get_or_create_user(email, name, password, role):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            email=email,
            name=name,
            password_hash=hash_password(password),
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user: {email}")
    return user


def seed():
    # Users
    admin = get_or_create_user("admin@convention.mx", "Super Admin", "demo123", "superadmin")
    org = get_or_create_user("org@comiccon.mx", "Organizador MexiCon", "demo123", "organizer")
    fan = get_or_create_user("fan@test.mx", "Fan Attendee", "demo123", "attendee")

    # Convention
    conv = db.query(models.Convention).filter(models.Convention.slug == "mexican-2025").first()
    if not conv:
        conv = models.Convention(
            organizer_id=org.id,
            name="MexiCon 2025",
            slug="mexican-2025",
            edition="2025 Edition",
            tagline="La convención de entretenimiento más grande de México",
            description="MexiCon 2025 es el evento definitivo de gaming, anime, cómics y cultura pop en México. Tres días de paneles, torneos, exhibidores y mucho más.",
            logo_url="https://api.dicebear.com/7.x/initials/svg?seed=MexiCon",
            cover_url="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=80",
            banner_url="https://images.unsplash.com/photo-1560523159-4a9692d222ef?w=1920&q=80",
            theme_color="#7c3aed",
            accent_color="#f59e0b",
            bg_color="#0a0a0f",
            font_style="gaming",
            venue_name="Centro Banamex",
            address="Av. del Conscripto 311, Lomas de Sotelo",
            city="Ciudad de México",
            lat=19.4326,
            lng=-99.1332,
            start_date=datetime(2025, 8, 15, 10, 0),
            end_date=datetime(2025, 8, 17, 20, 0),
            status="published",
            max_attendees=5000,
            website="https://mexican2025.mx",
            social_json=json.dumps({
                "twitter": "@MexiCon2025",
                "instagram": "@mexican2025",
                "facebook": "MexiCon2025"
            }),
            rules_text="1. Respeto a todos los asistentes.\n2. No se permiten armas reales.\n3. Cosplay friendly — los disfraces deben ser apropiados para todas las edades.",
            platform_fee_percent=5.0,
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        print(f"Created convention: {conv.name}")

    # Stages
    stages_data = [
        {"name": "Main Stage", "description": "El escenario principal con los paneles más esperados", "capacity": 1000, "color": "#7c3aed", "location_in_venue": "Hall Principal, Nivel 1"},
        {"name": "Panel Room A", "description": "Sala de paneles y charlas especializadas", "capacity": 200, "color": "#3b82f6", "location_in_venue": "Sala A, Nivel 2"},
        {"name": "Gaming Arena", "description": "Arena de torneos y competencias de videojuegos", "capacity": 300, "color": "#10b981", "location_in_venue": "Hall B, Nivel 1"},
    ]
    stages = []
    for sd in stages_data:
        stage = db.query(models.Stage).filter(
            models.Stage.convention_id == conv.id,
            models.Stage.name == sd["name"]
        ).first()
        if not stage:
            stage = models.Stage(convention_id=conv.id, **sd)
            db.add(stage)
            db.commit()
            db.refresh(stage)
            print(f"Created stage: {sd['name']}")
        stages.append(stage)

    # Speakers
    speakers_data = [
        {"name": "Akira Yamamoto", "title": "Director de Arte", "company": "Pixel Studios Japan", "bio": "Veterano del anime con 20 años de experiencia en producción de series icónicas.", "photo_url": "https://api.dicebear.com/7.x/personas/svg?seed=Akira", "twitter": "@akira_art", "is_keynote": True},
        {"name": "María González", "title": "Campeona Nacional FGC", "company": "Team México", "bio": "Tres veces campeona nacional de Street Fighter. Representante de México en EVO.", "photo_url": "https://api.dicebear.com/7.x/personas/svg?seed=Maria", "twitter": "@mariafgc", "is_keynote": True},
        {"name": "Carlos Ríos", "title": "Escritor & Editor", "company": "Cómics del Norte", "bio": "Autor de la exitosa serie 'Lucha Heroes' con ventas de más de 200,000 ejemplares.", "photo_url": "https://api.dicebear.com/7.x/personas/svg?seed=Carlos", "twitter": "@carloscomics", "is_keynote": False},
        {"name": "Sofia Mendez", "title": "Content Creator", "company": "YouTube / Twitch", "bio": "Streamers con 2M de seguidores especializada en retrogaming y cultura pop mexicana.", "photo_url": "https://api.dicebear.com/7.x/personas/svg?seed=Sofia", "twitter": "@sofiaretro", "is_keynote": False},
    ]
    speakers = []
    for sd in speakers_data:
        speaker = db.query(models.Speaker).filter(
            models.Speaker.convention_id == conv.id,
            models.Speaker.name == sd["name"]
        ).first()
        if not speaker:
            speaker = models.Speaker(convention_id=conv.id, **sd)
            db.add(speaker)
            db.commit()
            db.refresh(speaker)
            print(f"Created speaker: {sd['name']}")
        speakers.append(speaker)

    # Sessions (2 days, 3 per day across stages)
    sessions_data = [
        # Day 1 - Aug 15
        {"stage_id": stages[0].id, "speaker_id": speakers[0].id, "title": "Keynote: El Futuro del Anime", "description": "Akira Yamamoto presenta las tendencias del anime para los próximos 5 años.", "session_type": "talk", "start_time": datetime(2025, 8, 15, 11, 0), "end_time": datetime(2025, 8, 15, 12, 0), "tags_json": json.dumps(["anime", "keynote", "arte"])},
        {"stage_id": stages[1].id, "speaker_id": speakers[2].id, "title": "Cómic Mexicano: Pasado y Futuro", "description": "Historia y evolución del cómic nacional.", "session_type": "panel", "start_time": datetime(2025, 8, 15, 13, 0), "end_time": datetime(2025, 8, 15, 14, 30), "tags_json": json.dumps(["comics", "cultura"])},
        {"stage_id": stages[2].id, "speaker_id": speakers[1].id, "title": "Masterclass: Técnicas Pro FGC", "description": "María González comparte técnicas avanzadas de juegos de pelea.", "session_type": "workshop", "start_time": datetime(2025, 8, 15, 15, 0), "end_time": datetime(2025, 8, 15, 16, 30), "tags_json": json.dumps(["gaming", "esports", "fgc"])},
        # Day 2 - Aug 16
        {"stage_id": stages[0].id, "speaker_id": speakers[3].id, "title": "Keynote: La Economía del Creator", "description": "Cómo monetizar tu pasión por la cultura pop en 2025.", "session_type": "talk", "start_time": datetime(2025, 8, 16, 11, 0), "end_time": datetime(2025, 8, 16, 12, 0), "tags_json": json.dumps(["streaming", "creator", "youtube"])},
        {"stage_id": stages[1].id, "speaker_id": None, "title": "Panel: Cosplay Competition Prep", "description": "Tips para competir en el concurso de cosplay de MexiCon.", "session_type": "panel", "start_time": datetime(2025, 8, 16, 14, 0), "end_time": datetime(2025, 8, 16, 15, 0), "tags_json": json.dumps(["cosplay"])},
        {"stage_id": stages[2].id, "speaker_id": speakers[1].id, "title": "Ceremonia de Clausura Torneos", "description": "Premiación y ceremonia de cierre de los torneos oficiales.", "session_type": "ceremony", "start_time": datetime(2025, 8, 16, 18, 0), "end_time": datetime(2025, 8, 16, 19, 0), "tags_json": json.dumps(["torneos", "ceremonia"])},
    ]
    for sd in sessions_data:
        existing = db.query(models.Session).filter(
            models.Session.convention_id == conv.id,
            models.Session.title == sd["title"]
        ).first()
        if not existing:
            session = models.Session(convention_id=conv.id, **sd)
            db.add(session)
            db.commit()
            print(f"Created session: {sd['title']}")

    # Stands - 12 stands in 4x3 grid
    stand_configs = [
        # Row A
        {"number": "A-01", "name": "Pixel Studios", "category": "sponsor", "size": "large", "price": 8000, "status": "sold", "x_pos": 5, "y_pos": 5, "width": 18, "height": 12, "contact_name": "Akira Y.", "contact_email": "akira@pixel.jp"},
        {"number": "A-02", "name": "MangaMax", "category": "merch", "size": "standard", "price": 4500, "status": "sold", "x_pos": 28, "y_pos": 5, "width": 13, "height": 12, "contact_name": "Pedro L.", "contact_email": "pedro@mangamax.mx"},
        {"number": "A-03", "name": None, "category": "general", "size": "standard", "price": 3500, "status": "available", "x_pos": 46, "y_pos": 5, "width": 13, "height": 12},
        {"number": "A-04", "name": "Retro Games MX", "category": "gaming", "size": "standard", "price": 4000, "status": "reserved", "x_pos": 64, "y_pos": 5, "width": 13, "height": 12, "contact_name": "Ana V.", "contact_email": "ana@retrogames.mx"},
        # Row B
        {"number": "B-01", "name": "Tacos del Futuro", "category": "food", "size": "small", "price": 2500, "status": "sold", "x_pos": 5, "y_pos": 22, "width": 13, "height": 10, "contact_name": "Chef Robles", "contact_email": "chef@tacosfuturo.mx"},
        {"number": "B-02", "name": None, "category": "general", "size": "standard", "price": 3500, "status": "available", "x_pos": 23, "y_pos": 22, "width": 13, "height": 10},
        {"number": "B-03", "name": "Cómics del Norte", "category": "merch", "size": "standard", "price": 4000, "status": "sold", "x_pos": 41, "y_pos": 22, "width": 13, "height": 10, "contact_name": "Carlos R.", "contact_email": "carlos@comicsnorte.mx"},
        {"number": "B-04", "name": None, "category": "gaming", "size": "small", "price": 3000, "status": "available", "x_pos": 59, "y_pos": 22, "width": 13, "height": 10},
        # Row C
        {"number": "C-01", "name": "Cosplay Central", "category": "merch", "size": "standard", "price": 4500, "status": "reserved", "x_pos": 5, "y_pos": 37, "width": 13, "height": 10, "contact_name": "Lili M.", "contact_email": "lili@cosplaycentral.mx"},
        {"number": "C-02", "name": None, "category": "general", "size": "standard", "price": 3500, "status": "available", "x_pos": 23, "y_pos": 37, "width": 13, "height": 10},
        {"number": "C-03", "name": None, "category": "food", "size": "small", "price": 2000, "status": "available", "x_pos": 41, "y_pos": 37, "width": 13, "height": 10},
        {"number": "C-04", "name": "Team México FGC", "category": "gaming", "size": "large", "price": 6000, "status": "sold", "x_pos": 59, "y_pos": 37, "width": 18, "height": 10, "contact_name": "María G.", "contact_email": "maria@teammxfgc.com"},
    ]
    for sc in stand_configs:
        existing = db.query(models.Stand).filter(
            models.Stand.convention_id == conv.id,
            models.Stand.number == sc["number"]
        ).first()
        if not existing:
            stand = models.Stand(convention_id=conv.id, **sc)
            db.add(stand)
    db.commit()
    print("Stands seeded")

    # Sponsors
    sponsors_data = [
        {"name": "Pixel Studios Japan", "logo_url": "https://api.dicebear.com/7.x/initials/svg?seed=PS", "website": "https://pixel.jp", "tier": "title", "amount_sponsored": 150000},
        {"name": "Konami MX", "logo_url": "https://api.dicebear.com/7.x/initials/svg?seed=KM", "website": "https://konami.com", "tier": "gold", "amount_sponsored": 50000},
        {"name": "MangaMax", "logo_url": "https://api.dicebear.com/7.x/initials/svg?seed=MM", "website": "https://mangamax.mx", "tier": "bronze", "amount_sponsored": 15000},
        {"name": "Retro Games MX", "logo_url": "https://api.dicebear.com/7.x/initials/svg?seed=RG", "website": "https://retrogames.mx", "tier": "bronze", "amount_sponsored": 10000},
    ]
    for sd in sponsors_data:
        existing = db.query(models.Sponsor).filter(
            models.Sponsor.convention_id == conv.id,
            models.Sponsor.name == sd["name"]
        ).first()
        if not existing:
            sponsor = models.Sponsor(convention_id=conv.id, **sd)
            db.add(sponsor)
    db.commit()
    print("Sponsors seeded")

    # Ticket Types
    ticket_types_data = [
        {"name": "General", "description": "Acceso general a todas las áreas públicas", "price": 350.0, "quantity_total": 500, "benefits_json": json.dumps(["Acceso a todas las áreas públicas", "Acceso a paneles (sujeto a cupo)", "Programa oficial digital"]), "color": "#6366f1"},
        {"name": "VIP", "description": "Experiencia premium con acceso prioritario", "price": 850.0, "quantity_total": 100, "benefits_json": json.dumps(["Todo lo de General", "Acceso prioritario a paneles", "Área VIP exclusiva", "Meet & Greet con invitados", "Kit oficial de MexiCon"]), "color": "#f59e0b"},
        {"name": "Exhibitor", "description": "Pase para expositores con stand rentado", "price": 1500.0, "quantity_total": 50, "benefits_json": json.dumps(["Acceso completo al evento", "Acceso al área de exhibidores", "2 pases de cortesía", "Estacionamiento incluido"]), "color": "#10b981"},
    ]
    ticket_types = []
    for ttd in ticket_types_data:
        tt = db.query(models.TicketType).filter(
            models.TicketType.convention_id == conv.id,
            models.TicketType.name == ttd["name"]
        ).first()
        if not tt:
            tt = models.TicketType(convention_id=conv.id, **ttd)
            db.add(tt)
            db.commit()
            db.refresh(tt)
            print(f"Created ticket type: {ttd['name']}")
        ticket_types.append(tt)

    # Tournaments
    tournaments_data = [
        {"name": "Street Fighter 6 Tournament", "game": "Street Fighter 6", "format": "double_elim", "max_participants": 32, "prize_pool": 2000.0, "prize_description": "1er lugar $1200 | 2do $500 | 3ro $300", "entry_fee": 50.0, "start_time": datetime(2025, 8, 16, 10, 0), "status": "open", "stage_id": stages[2].id},
        {"name": "Pokémon TCG Open", "game": "Pokémon Trading Card Game", "format": "swiss", "max_participants": 64, "prize_pool": 0.0, "prize_description": "Trofeo + productos oficiales Pokémon", "entry_fee": 30.0, "start_time": datetime(2025, 8, 15, 9, 0), "status": "open", "stage_id": stages[2].id},
    ]
    for td in tournaments_data:
        existing = db.query(models.Tournament).filter(
            models.Tournament.convention_id == conv.id,
            models.Tournament.name == td["name"]
        ).first()
        if not existing:
            t = models.Tournament(convention_id=conv.id, **td)
            db.add(t)
    db.commit()
    print("Tournaments seeded")

    # Sample Payments & Tickets
    if db.query(models.TicketPayment).filter(models.TicketPayment.convention_id == conv.id).count() == 0:
        buyers = [
            ("Juan Pérez", "juan@test.mx", "succeeded"),
            ("Ana López", "ana@test.mx", "succeeded"),
            ("Roberto Díaz", "roberto@test.mx", "succeeded"),
            ("Carmen Vega", "carmen@test.mx", "pending"),
            ("Miguel Torres", "miguel@test.mx", "succeeded"),
        ]
        tt_general = ticket_types[0]
        tt_vip = ticket_types[1]
        for bname, bemail, bstatus in buyers:
            is_vip = "vip" in bemail or bname.startswith("Ana")
            chosen_tt = tt_vip if is_vip else tt_general
            price = chosen_tt.price
            pf = round(price * conv.platform_fee_percent / 100, 2)
            oa = round(price - pf, 2)
            payment = models.TicketPayment(
                convention_id=conv.id,
                amount=price,
                platform_fee=pf,
                organizer_amount=oa,
                status=bstatus,
                buyer_name=bname,
                buyer_email=bemail,
                items_json=json.dumps([{"ticket_type_id": chosen_tt.id, "name": chosen_tt.name, "quantity": 1, "price": price, "subtotal": price}]),
            )
            db.add(payment)
            db.flush()
            if bstatus == "succeeded":
                ticket = models.Ticket(
                    ticket_type_id=chosen_tt.id,
                    convention_id=conv.id,
                    attendee_name=bname,
                    attendee_email=bemail,
                    qr_code=secrets.token_hex(8).upper(),
                    status="paid",
                    payment_id=payment.id,
                )
                db.add(ticket)
                chosen_tt.quantity_sold += 1
        db.commit()
        print("Sample payments and tickets seeded")

    print("Seed complete!")
    db.close()


if __name__ == "__main__":
    seed()
