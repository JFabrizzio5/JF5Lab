import json
from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(models.User).count() > 0:
            print("Database already seeded, skipping.")
            return

        print("Seeding database...")

        # Users
        admin = models.User(
            email="admin@salonos.mx",
            name="Super Admin",
            password_hash=pwd_context.hash("demo123"),
            role="superadmin",
            phone="+525500000000",
        )
        owner = models.User(
            email="dueno@jardines.mx",
            name="Carlos Jardines",
            password_hash=pwd_context.hash("demo123"),
            role="venue_owner",
            phone="+525511223344",
        )
        client_user = models.User(
            email="cliente@test.mx",
            name="Ana García",
            password_hash=pwd_context.hash("demo123"),
            role="client",
            phone="+525598765432",
        )

        db.add_all([admin, owner, client_user])
        db.flush()

        # Venue
        gallery = json.dumps([
            "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800",
            "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800",
            "https://images.unsplash.com/photo-1478146896981-b80fe463b330?w=800",
            "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800",
        ])
        amenities = json.dumps([
            "Estacionamiento", "Cocina equipada", "Aire acondicionado",
            "Sonido profesional", "Iluminación LED", "WiFi", "Valet parking",
        ])

        venue = models.Venue(
            owner_id=owner.id,
            name="Jardines del Valle",
            slug="jardines-del-valle",
            tagline="El lugar perfecto para los momentos más importantes de tu vida",
            description=(
                "Jardines del Valle es el espacio de eventos más exclusivo del Valle de México. "
                "Con más de 20 años de experiencia, ofrecemos espacios únicos rodeados de naturaleza "
                "para bodas, quinceañeras, graduaciones y eventos corporativos. "
                "Nuestro equipo de expertos garantiza que cada detalle sea perfecto."
            ),
            logo_url="https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=200",
            cover_url="https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1600",
            theme_color="#7c3aed",
            accent_color="#f59e0b",
            phone="+52 55 1234 5678",
            email="contacto@jardines.mx",
            whatsapp_number="525512345678",
            whatsapp_message="Hola, me interesa reservar un evento en Jardines del Valle.",
            address="Av. del Valle 1500, Pedregal",
            city="Ciudad de México",
            lat=19.3437,
            lng=-99.1824,
            gallery_json=gallery,
            amenities_json=amenities,
            platform_fee_percent=5.0,
        )
        db.add(venue)
        db.flush()

        # Branches
        branch1 = models.VenueBranch(
            venue_id=venue.id,
            name="Jardines del Valle — Sede Principal",
            address="Av. del Valle 1500, Pedregal, CDMX",
            lat=19.3437,
            lng=-99.1824,
            phone="+52 55 1234 5678",
        )
        branch2 = models.VenueBranch(
            venue_id=venue.id,
            name="Jardines del Valle — Satélite",
            address="Blvd. Manuel Ávila Camacho 2000, Naucalpan",
            lat=19.4978,
            lng=-99.2336,
            phone="+52 55 8765 4321",
        )
        db.add_all([branch1, branch2])
        db.flush()

        # Event Spaces
        space_amenities = json.dumps(["Pista de baile", "Escenario", "Aire acondicionado", "Luz LED"])
        space_images = json.dumps([
            "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800",
        ])
        garden_amenities = json.dumps(["Jardín natural", "Fuente", "Pérgola", "Iluminación exterior"])
        garden_images = json.dumps([
            "https://images.unsplash.com/photo-1478146896981-b80fe463b330?w=800",
        ])
        vip_amenities = json.dumps(["Bar privado", "Terraza", "Sala lounge", "Smart TV 85\""])
        vip_images = json.dumps([
            "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800",
        ])

        space1 = models.EventSpace(
            venue_id=venue.id,
            branch_id=branch1.id,
            name="Salón Principal",
            description="Nuestro salón más grande con capacidad para 300 personas. Equipado con pista de baile, escenario y sistema de sonido profesional.",
            capacity=300,
            price_per_hour=2500.0,
            price_event=15000.0,
            images_json=space_images,
            amenities_json=space_amenities,
            floor_plan_url="https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800",
        )
        space2 = models.EventSpace(
            venue_id=venue.id,
            branch_id=branch1.id,
            name="Jardín Principal",
            description="Un hermoso jardín al aire libre ideal para ceremonias y cocteles. Capacidad para 150 personas con vista a las montañas.",
            capacity=150,
            price_per_hour=1200.0,
            price_event=8000.0,
            images_json=garden_images,
            amenities_json=garden_amenities,
        )
        space3 = models.EventSpace(
            venue_id=venue.id,
            branch_id=branch2.id,
            name="Sala VIP",
            description="Espacio exclusivo para eventos íntimos con servicio personalizado. Perfecto para reuniones corporativas y celebraciones privadas.",
            capacity=50,
            price_per_hour=800.0,
            price_event=4000.0,
            images_json=vip_images,
            amenities_json=vip_amenities,
        )
        db.add_all([space1, space2, space3])
        db.flush()

        # Clients
        c1 = models.Client(
            venue_id=venue.id,
            name="María López",
            email="maria@gmail.com",
            phone="+52 55 1111 2222",
            source="web",
            notes="Interesada en boda para 200 personas en primavera",
        )
        c2 = models.Client(
            venue_id=venue.id,
            name="Roberto Sánchez",
            email="roberto@empresa.com",
            phone="+52 55 3333 4444",
            source="referral",
            notes="Evento corporativo anual, presupuesto amplio",
        )
        c3 = models.Client(
            venue_id=venue.id,
            name="Sofía Ramírez",
            email="sofia@hotmail.com",
            phone="+52 55 5555 6666",
            source="whatsapp",
            notes="XV años para junio",
        )
        db.add_all([c1, c2, c3])
        db.flush()

        # Bookings
        now = datetime.utcnow()
        b1 = models.EventBooking(
            venue_id=venue.id,
            space_id=space1.id,
            client_id=c1.id,
            title="Boda María & Juan",
            event_type="boda",
            start_datetime=now + timedelta(days=45),
            end_datetime=now + timedelta(days=45, hours=8),
            guests_count=200,
            status="confirmed",
            total_price=35000.0,
            deposit_amount=10000.0,
            notes="Decoración en blanco y dorado. Cena de 3 tiempos.",
        )
        b2 = models.EventBooking(
            venue_id=venue.id,
            space_id=space2.id,
            client_id=c2.id,
            title="Convención Anual TechCorp",
            event_type="corporativo",
            start_datetime=now + timedelta(days=15),
            end_datetime=now + timedelta(days=15, hours=6),
            guests_count=80,
            status="deposit_paid",
            total_price=20000.0,
            deposit_amount=5000.0,
            notes="Requiere proyector, mesas de trabajo y coffee break.",
        )
        b3 = models.EventBooking(
            venue_id=venue.id,
            space_id=space3.id,
            client_id=c3.id,
            title="XV Años Sofía",
            event_type="xv",
            start_datetime=now + timedelta(days=90),
            end_datetime=now + timedelta(days=90, hours=7),
            guests_count=50,
            status="inquiry",
            total_price=12000.0,
            deposit_amount=3000.0,
            notes="Temática princesa Disney.",
        )
        db.add_all([b1, b2, b3])
        db.flush()

        # Chat room for c1
        room = models.ChatRoom(venue_id=venue.id, client_id=c1.id)
        db.add(room)
        db.flush()

        msg1 = models.ChatMessage(
            room_id=room.id,
            sender_name="María López",
            sender_type="client",
            content="Hola, me gustaría saber más detalles sobre la decoración del salón principal.",
        )
        msg2 = models.ChatMessage(
            room_id=room.id,
            sender_user_id=owner.id,
            sender_name="Carlos Jardines",
            sender_type="staff",
            content="¡Hola María! Con gusto te ayudamos. Trabajamos con varios decoradores de confianza. ¿Tienes alguna temática en mente?",
        )
        db.add_all([msg1, msg2])
        db.commit()

        print("Seed completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
