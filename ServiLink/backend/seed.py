"""Seed demo data: superadmin, client, freelancers with CDMX coordinates."""
from database import SessionLocal, engine
import models
import auth as auth_utils
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        if db.query(models.User).count() > 0:
            print("DB ya tiene datos. Skip seed.")
            return

        # --- Categories ---
        categories_data = [
            ("Plomería", "🔧", "Reparaciones de tuberías, fugas, instalaciones"),
            ("Electricidad", "⚡", "Instalaciones eléctricas, cortocircuitos, luminarias"),
            ("Limpieza", "🧹", "Limpieza del hogar, oficinas, post-obra"),
            ("Jardinería", "🌿", "Poda, mantenimiento de jardines, paisajismo"),
            ("Pintura", "🎨", "Pintura interior y exterior, acabados"),
            ("Carpintería", "🪚", "Muebles a medida, reparaciones, instalaciones"),
            ("Cerrajería", "🔑", "Apertura de cerraduras, duplicado de llaves"),
            ("Mudanzas", "📦", "Traslados locales, empaque, carga y descarga"),
            ("Aire Acondicionado", "❄️", "Instalación, mantenimiento y reparación de A/C"),
            ("Tecnología", "💻", "Reparación de PCs, redes, instalación de software"),
        ]
        categories = []
        for name, icon, desc in categories_data:
            cat = models.Category(name=name, icon=icon, description=desc)
            db.add(cat)
            categories.append(cat)
        db.commit()
        for c in categories:
            db.refresh(c)

        # --- Superadmin ---
        admin = models.User(
            email="admin@servilink.com",
            name="Super Admin",
            password_hash=auth_utils.hash_password("admin123"),
            role="superadmin",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=admin",
            phone="+52 55 0000 0001",
        )
        db.add(admin)

        # --- Client ---
        client = models.User(
            email="cliente@servilink.com",
            name="María González",
            password_hash=auth_utils.hash_password("cliente123"),
            role="client",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=maria",
            phone="+52 55 1234 5678",
        )
        db.add(client)
        db.commit()
        db.refresh(admin)
        db.refresh(client)

        # --- Freelancers (CDMX coords) ---
        freelancers_data = [
            {
                "email": "freelancer@servilink.com",
                "name": "Carlos Ramírez",
                "phone": "+52 55 9876 5432",
                "bio": "Plomero certificado con 10 años de experiencia. Especialista en reparaciones de emergencia.",
                "hourly_rate": 350.0,
                "experience_years": 10,
                "lat": 19.4326, "lng": -99.1332,
                "address": "Colonia Centro, CDMX",
                "categories": [0, 1],
                "plan": "pro",
                "rating_avg": 4.8, "total_reviews": 47, "total_jobs": 53,
            },
            {
                "email": "electricista@servilink.com",
                "name": "Ana Martínez",
                "phone": "+52 55 5555 1234",
                "bio": "Electricista profesional, instalaciones residenciales y comerciales.",
                "hourly_rate": 400.0,
                "experience_years": 7,
                "lat": 19.4270, "lng": -99.1680,
                "address": "Condesa, CDMX",
                "categories": [1],
                "plan": "basic",
                "rating_avg": 4.6, "total_reviews": 31, "total_jobs": 35,
            },
            {
                "email": "limpieza@servilink.com",
                "name": "Roberto Jiménez",
                "phone": "+52 55 7777 8888",
                "bio": "Servicio de limpieza profesional. Puntual y confiable.",
                "hourly_rate": 200.0,
                "experience_years": 5,
                "lat": 19.4150, "lng": -99.1820,
                "address": "Narvarte, CDMX",
                "categories": [2],
                "plan": "premium",
                "rating_avg": 4.9, "total_reviews": 89, "total_jobs": 102,
            },
            {
                "email": "jardinero@servilink.com",
                "name": "Luis Torres",
                "phone": "+52 55 3333 4444",
                "bio": "Jardinero con pasión por el diseño verde. Más de 8 años transformando espacios.",
                "hourly_rate": 280.0,
                "experience_years": 8,
                "lat": 19.4480, "lng": -99.1900,
                "address": "Polanco, CDMX",
                "categories": [3, 4],
                "plan": "basic",
                "rating_avg": 4.7, "total_reviews": 22, "total_jobs": 28,
            },
            {
                "email": "carpintero@servilink.com",
                "name": "Pedro Sánchez",
                "phone": "+52 55 6666 7777",
                "bio": "Carpintero artesanal. Muebles a medida y reparaciones de alta calidad.",
                "hourly_rate": 450.0,
                "experience_years": 15,
                "lat": 19.3900, "lng": -99.1500,
                "address": "Iztapalapa, CDMX",
                "categories": [5, 7],
                "plan": "pro",
                "rating_avg": 4.5, "total_reviews": 63, "total_jobs": 70,
            },
        ]

        freelancer_users = []
        for fd in freelancers_data:
            u = models.User(
                email=fd["email"],
                name=fd["name"],
                password_hash=auth_utils.hash_password("freelancer123"),
                role="freelancer",
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={fd['email']}",
                phone=fd["phone"],
            )
            db.add(u)
            db.commit()
            db.refresh(u)

            prof = models.ProfessionalProfile(
                user_id=u.id,
                bio=fd["bio"],
                hourly_rate=fd["hourly_rate"],
                experience_years=fd["experience_years"],
                lat=fd["lat"], lng=fd["lng"],
                address=fd["address"],
                is_available=True,
                subscription_plan=fd["plan"],
                rating_avg=fd["rating_avg"],
                total_reviews=fd["total_reviews"],
                total_jobs=fd["total_jobs"],
            )
            db.add(prof)
            db.commit()
            db.refresh(prof)

            for cat_idx in fd["categories"]:
                pc = models.ProfessionalCategory(professional_id=prof.id, category_id=categories[cat_idx].id)
                db.add(pc)

            sub = models.Subscription(
                user_id=u.id,
                plan=fd["plan"],
                status="active",
                price_monthly={"free": 0, "basic": 199, "pro": 499, "premium": 999}[fd["plan"]],
                expires_at=datetime.utcnow() + timedelta(days=30),
            )
            db.add(sub)
            db.commit()
            freelancer_users.append(u)

        # --- Demo bookings ---
        first_freelancer = freelancer_users[0]
        b1 = models.Booking(
            client_id=client.id,
            professional_id=first_freelancer.id,
            category_id=categories[0].id,
            description="Necesito reparar una fuga en el baño principal urgente",
            status="completed",
            client_address="Av. Insurgentes Sur 1234, CDMX",
            client_lat=19.4200, client_lng=-99.1700,
            price=350.0,
            created_at=datetime.utcnow() - timedelta(days=5),
        )
        b2 = models.Booking(
            client_id=client.id,
            professional_id=freelancer_users[1].id,
            category_id=categories[1].id,
            description="Instalar 3 puntos eléctricos en la sala",
            status="in_progress",
            client_address="Colonia Roma Norte, CDMX",
            client_lat=19.4190, client_lng=-99.1600,
            price=400.0,
            created_at=datetime.utcnow() - timedelta(days=1),
        )
        b3 = models.Booking(
            client_id=client.id,
            professional_id=freelancer_users[2].id,
            category_id=categories[2].id,
            description="Limpieza profunda del departamento 3 recámaras",
            status="pending",
            client_address="Colonia Del Valle, CDMX",
            client_lat=19.3980, client_lng=-99.1650,
            price=200.0,
            created_at=datetime.utcnow() - timedelta(hours=2),
        )
        db.add_all([b1, b2, b3])
        db.commit()
        db.refresh(b1)

        # --- Review for completed booking ---
        review = models.Review(
            booking_id=b1.id,
            client_id=client.id,
            professional_id=first_freelancer.id,
            rating=5,
            comment="Excelente trabajo, muy puntual y profesional. Resolvió el problema en menos de una hora.",
        )
        db.add(review)
        db.commit()

        print("✅ Seed completado.")
        print("\n=== USUARIOS DEMO ===")
        print("👑 Superadmin: admin@servilink.com       / admin123")
        print("👤 Cliente:    cliente@servilink.com     / cliente123")
        print("🔧 Freelancer: freelancer@servilink.com  / freelancer123")
        print("   (también: electricista@, limpieza@, jardinero@, carpintero@ — todos con /freelancer123)")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
