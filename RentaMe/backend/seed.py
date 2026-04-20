import json
from datetime import datetime, timedelta
from database import SessionLocal, engine
import models
from auth import hash_password

models.Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(models.User).filter(models.User.email == "superadmin@rentame.mx").first():
            print("Ya existe seed. Saltando.")
            return

        # ── Users ──────────────────────────────────────────────
        admin = models.User(
            email="superadmin@rentame.mx",
            name="Super Admin",
            password_hash=hash_password("demo123"),
            role="superadmin",
        )
        vendor1_user = models.User(
            email="barcos@rentame.mx",
            name="Carlos Marina",
            password_hash=hash_password("demo123"),
            role="vendor",
        )
        vendor2_user = models.User(
            email="muebles@rentame.mx",
            name="Laura Muebles",
            password_hash=hash_password("demo123"),
            role="vendor",
        )
        customer1 = models.User(
            email="cliente@ejemplo.mx",
            name="Juan Pérez",
            password_hash=hash_password("demo123"),
            role="customer",
        )
        db.add_all([admin, vendor1_user, vendor2_user, customer1])
        db.commit()
        db.refresh(vendor1_user)
        db.refresh(vendor2_user)

        # ── Vendor Profiles ────────────────────────────────────
        v1 = models.VendorProfile(
            user_id=vendor1_user.id,
            slug="aqua-adventures",
            business_name="Aqua Adventures",
            tagline="Vive el mar como nunca antes",
            description="Rentamos embarcaciones, kayaks y motos de agua en Acapulco. Experiencias únicas en el mar con equipos de primera calidad y guías expertos.",
            cover_url="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1600",
            logo_url="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=200&h=200&fit=crop",
            theme_color="#0ea5e9",
            accent_color="#f59e0b",
            phone="+52 744 123 4567",
            email="info@aqua-adventures.mx",
            whatsapp="527441234567",
            instagram_url="https://instagram.com/aquaadventures",
            facebook_url="https://facebook.com/aquaadventures",
            city="Acapulco",
            address="Marina Acapulco, Local 12",
            deposit_percent=30.0,
            cancellation_policy="Cancelaciones con más de 48 horas: reembolso total. Entre 24-48 horas: 50% de reembolso. Menos de 24 horas: sin reembolso.",
            platform_fee_percent=5.0,
            is_active=True,
        )
        v2 = models.VendorProfile(
            user_id=vendor2_user.id,
            slug="renta-muebles-mx",
            business_name="Renta Muebles MX",
            tagline="Tu evento, perfectamente amoblado",
            description="Especialistas en renta de mobiliario para eventos sociales y corporativos en CDMX. Sillas Tiffany, mesas, carpas y más.",
            cover_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=1600",
            logo_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=200&h=200&fit=crop",
            theme_color="#7c3aed",
            accent_color="#f59e0b",
            phone="+52 55 1234 5678",
            email="info@rentamueblesmx.com",
            whatsapp="525512345678",
            instagram_url="https://instagram.com/rentamueblesmx",
            facebook_url="https://facebook.com/rentamueblesmx",
            city="CDMX",
            address="Col. Polanco, CDMX",
            deposit_percent=40.0,
            cancellation_policy="Cancelaciones con más de 72 horas: reembolso total menos gastos administrativos. Menos de 72 horas: 50% de cargo.",
            platform_fee_percent=5.0,
            is_active=True,
        )
        db.add_all([v1, v2])
        db.commit()
        db.refresh(v1)
        db.refresh(v2)

        # ── Items Vendor 1 (Aqua Adventures) ──────────────────
        i1 = models.RentalItem(
            vendor_id=v1.id,
            name="Lancha Pescadora 20ft",
            description="Lancha ideal para pesca deportiva y paseos. Equipada con todo lo necesario para una experiencia segura y divertida en el mar.",
            category="boats",
            images_json=json.dumps([
                "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
                "https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?w=800",
            ]),
            price_per_day=2500.0,
            price_per_weekend=4500.0,
            quantity=2,
            min_rental_hours=4,
            advance_booking_days=1,
            specifications_json=json.dumps({
                "Capacidad": "6 personas",
                "Motor": "115HP Yamaha",
                "Eslora": "6.1m",
                "Combustible": "No incluido",
            }),
            included_json=json.dumps(["Chalecos salvavidas", "Ancla", "Cuerda de remolque", "Extintor"]),
            not_included_json=json.dumps(["Combustible", "Guía", "Carnada"]),
            requirements="Se requiere mayor de 18 años. Licencia náutica obligatoria para manejo propio o contratar guía.",
            deposit_amount=750.0,
            is_active=True,
            is_featured=True,
        )
        i2 = models.RentalItem(
            vendor_id=v1.id,
            name="Kayak Doble",
            description="Kayak para dos personas, perfecto para explorar las costas y bahías de Acapulco. Fácil de manejar, no requiere experiencia previa.",
            category="sports",
            images_json=json.dumps([
                "https://images.unsplash.com/photo-1544463457-5e4bd1eb48d4?w=800",
            ]),
            price_per_hour=200.0,
            price_per_day=600.0,
            quantity=5,
            min_rental_hours=1,
            advance_booking_days=0,
            specifications_json=json.dumps({
                "Capacidad": "2 personas",
                "Longitud": "5.2m",
                "Material": "Polietileno",
            }),
            included_json=json.dumps(["Remos", "Chalecos salvavidas", "Instructivo de uso"]),
            not_included_json=json.dumps(["Guía", "Transporte"]),
            requirements="Saber nadar. Menores de 12 años deben ir acompañados.",
            deposit_amount=200.0,
            is_active=True,
            is_featured=True,
        )
        i3 = models.RentalItem(
            vendor_id=v1.id,
            name="Moto de Agua Seadoo",
            description="Emocionante moto de agua para los más aventureros. Velocidad y adrenalina garantizadas en las aguas de Acapulco.",
            category="sports",
            images_json=json.dumps([
                "https://images.unsplash.com/photo-1600456899121-68eda5706087?w=800",
            ]),
            price_per_hour=800.0,
            price_per_day=3500.0,
            quantity=3,
            min_rental_hours=1,
            advance_booking_days=0,
            specifications_json=json.dumps({
                "Capacidad": "3 personas",
                "Motor": "130HP",
                "Velocidad máx": "80 km/h",
            }),
            included_json=json.dumps(["Chaleco salvavidas", "Gafas acuáticas", "Instrucción básica"]),
            not_included_json=json.dumps(["Combustible incluido por horas"]),
            requirements="Mayor de 18 años. Licencia de conducir vigente. Firmar carta responsiva.",
            deposit_amount=1000.0,
            is_active=True,
            is_featured=False,
        )

        # ── Items Vendor 2 (Renta Muebles MX) ─────────────────
        i4 = models.RentalItem(
            vendor_id=v2.id,
            name="Paquete Sillas Tiffany x50",
            description="50 sillas Tiffany de alta calidad disponibles en varios colores. Perfectas para bodas, quinceañeras y eventos corporativos.",
            category="furniture",
            images_json=json.dumps([
                "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
            ]),
            price_per_day=1500.0,
            price_per_weekend=2500.0,
            quantity=4,
            min_rental_hours=8,
            advance_booking_days=3,
            specifications_json=json.dumps({
                "Cantidad": "50 sillas",
                "Material": "Acrílico",
                "Colores": "Blanco, Dorado, Plateado",
                "Capacidad": "hasta 150kg c/u",
            }),
            included_json=json.dumps(["Entrega y recogida en CDMX", "Limpieza básica"]),
            not_included_json=json.dumps(["Moños o decoración", "Cojines"]),
            requirements="Se requiere depósito de seguridad. Entrega mínima 3 días hábiles de anticipación.",
            deposit_amount=600.0,
            is_active=True,
            is_featured=True,
        )
        i5 = models.RentalItem(
            vendor_id=v2.id,
            name="Mesa Redonda 10 personas",
            description="Mesa redonda de 1.8m de diámetro con capacidad para 10 personas. Incluye mantel blanco de cortesía.",
            category="furniture",
            images_json=json.dumps([
                "https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=800",
            ]),
            price_per_day=300.0,
            price_per_weekend=500.0,
            quantity=20,
            min_rental_hours=8,
            advance_booking_days=2,
            specifications_json=json.dumps({
                "Diámetro": "1.8m",
                "Capacidad": "10 personas",
                "Material": "Madera MDF",
                "Altura": "75cm",
            }),
            included_json=json.dumps(["Mantel blanco", "Entrega y recogida CDMX"]),
            not_included_json=json.dumps(["Sillas", "Decoración adicional"]),
            requirements="Depósito por daños requerido.",
            deposit_amount=150.0,
            is_active=True,
            is_featured=True,
        )
        i6 = models.RentalItem(
            vendor_id=v2.id,
            name="Carpa 6x6m con iluminación",
            description="Carpa resistente de 6x6 metros con iluminación LED integrada. Ideal para fiestas al aire libre, bodas en jardín y eventos corporativos.",
            category="party",
            images_json=json.dumps([
                "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?w=800",
            ]),
            price_per_day=2800.0,
            price_per_weekend=4500.0,
            quantity=3,
            min_rental_hours=24,
            advance_booking_days=5,
            specifications_json=json.dumps({
                "Dimensiones": "6m x 6m",
                "Altura": "3.5m",
                "Capacidad": "hasta 40 personas",
                "Iluminación": "LED RGB incluida",
            }),
            included_json=json.dumps(["Armado y desarmado", "Iluminación LED", "Anclas y tensores"]),
            not_included_json=json.dumps(["Piso especial", "Calefacción", "Ventiladores"]),
            requirements="Espacio mínimo de 7x7m libre. Se requiere acceso para camioneta de entrega.",
            deposit_amount=1000.0,
            is_active=True,
            is_featured=False,
        )

        db.add_all([i1, i2, i3, i4, i5, i6])
        db.commit()
        db.refresh(i1)
        db.refresh(i2)
        db.refresh(i4)
        db.refresh(i5)

        # ── Bookings Vendor 1 ──────────────────────────────────
        now = datetime.utcnow()
        b1 = models.Booking(
            vendor_id=v1.id,
            item_id=i1.id,
            customer_name="Miguel Torres",
            customer_email="miguel@email.com",
            customer_phone="+52 744 987 6543",
            start_datetime=now + timedelta(days=3),
            end_datetime=now + timedelta(days=4),
            rental_unit="day",
            quantity=1,
            unit_price=2500.0,
            subtotal=2500.0,
            deposit_amount=750.0,
            total=2500.0,
            status="confirmed",
            notes="Salida temprano 7am si es posible",
        )
        b2 = models.Booking(
            vendor_id=v1.id,
            item_id=i2.id,
            customer_name="Ana García",
            customer_email="ana@email.com",
            customer_phone="+52 744 111 2222",
            start_datetime=now + timedelta(days=1),
            end_datetime=now + timedelta(days=1, hours=3),
            rental_unit="hour",
            quantity=2,
            unit_price=200.0,
            subtotal=1200.0,
            deposit_amount=0.0,
            total=1200.0,
            status="inquiry",
            notes="Somos 4 personas",
        )
        b3 = models.Booking(
            vendor_id=v1.id,
            item_id=i3.id,
            customer_name="Roberto Silva",
            customer_email="roberto@email.com",
            customer_phone="+52 744 333 4444",
            start_datetime=now - timedelta(days=5),
            end_datetime=now - timedelta(days=4),
            rental_unit="day",
            quantity=1,
            unit_price=3500.0,
            subtotal=3500.0,
            deposit_amount=1000.0,
            total=3500.0,
            status="completed",
        )

        # ── Bookings Vendor 2 ──────────────────────────────────
        b4 = models.Booking(
            vendor_id=v2.id,
            item_id=i4.id,
            customer_name="Patricia López",
            customer_email="patricia@email.com",
            customer_phone="+52 55 5555 1234",
            start_datetime=now + timedelta(days=10),
            end_datetime=now + timedelta(days=11),
            rental_unit="day",
            quantity=1,
            unit_price=1500.0,
            subtotal=1500.0,
            deposit_amount=600.0,
            total=1500.0,
            status="deposit_paid",
            notes="Boda en jardín, colores dorado",
        )
        b5 = models.Booking(
            vendor_id=v2.id,
            item_id=i5.id,
            customer_name="Carlos Mendez",
            customer_email="carlos@email.com",
            customer_phone="+52 55 6666 7777",
            start_datetime=now + timedelta(days=15),
            end_datetime=now + timedelta(days=17),
            rental_unit="weekend",
            quantity=10,
            unit_price=500.0,
            subtotal=5000.0,
            deposit_amount=2000.0,
            total=5000.0,
            status="confirmed",
            notes="Quinceañera, necesitamos 10 mesas redondas",
        )
        b6 = models.Booking(
            vendor_id=v2.id,
            item_id=i6.id,
            customer_name="Sandra Ruiz",
            customer_email="sandra@email.com",
            customer_phone="+52 55 8888 9999",
            start_datetime=now - timedelta(days=2),
            end_datetime=now - timedelta(days=1),
            rental_unit="day",
            quantity=2,
            unit_price=2800.0,
            subtotal=5600.0,
            deposit_amount=2000.0,
            total=5600.0,
            status="completed",
        )

        db.add_all([b1, b2, b3, b4, b5, b6])
        db.commit()
        print("Seed completado exitosamente.")
    except Exception as e:
        db.rollback()
        print(f"Error en seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
