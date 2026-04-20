import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, DATABASE_URL
from models import User, Course, Lesson, TimeSlot, Enrollment, Review
from auth import get_password_hash

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)


def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).filter(User.email == "admin@edulink.mx").first():
            print("Seed data already exists, skipping.")
            return

        print("Seeding database...")

        # Create users
        admin = User(
            email="admin@edulink.mx",
            name="Admin EduLink",
            password_hash=get_password_hash("demo123"),
            role="admin",
            school="OTHER",
            avatar_url="https://ui-avatars.com/api/?name=Admin+EduLink&background=f59e0b&color=fff"
        )
        tutor = User(
            email="tutor@edulink.mx",
            name="Prof. Carlos Mendoza",
            password_hash=get_password_hash("demo123"),
            role="tutor",
            school="UNAM",
            avatar_url="https://ui-avatars.com/api/?name=Carlos+Mendoza&background=10b981&color=fff"
        )
        student = User(
            email="alumno@edulink.mx",
            name="Ana García",
            password_hash=get_password_hash("demo123"),
            role="student",
            school="UNAM",
            avatar_url="https://ui-avatars.com/api/?name=Ana+Garcia&background=6366f1&color=fff"
        )
        db.add_all([admin, tutor, student])
        db.commit()
        db.refresh(tutor)
        db.refresh(student)

        # Create courses
        course1 = Course(
            tutor_id=tutor.id,
            title="Cálculo Diferencial e Integral",
            description="Curso completo de cálculo para ingeniería y ciencias. Desde límites hasta integrales múltiples con aplicaciones prácticas.",
            category="Matemáticas",
            thumbnail_url="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=225&fit=crop",
            price=0.0,
            school_restricted=False,
            is_published=True
        )
        course2 = Course(
            tutor_id=tutor.id,
            title="Python para Ciencia de Datos",
            description="Aprende Python desde cero hasta análisis de datos con pandas, numpy y matplotlib. Ideal para estudiantes de ingeniería.",
            category="Programación",
            thumbnail_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&h=225&fit=crop",
            price=199.0,
            school_restricted=True,
            is_published=True
        )
        course3 = Course(
            tutor_id=tutor.id,
            title="Física Moderna: Relatividad y Cuántica",
            description="Introducción a la física del siglo XX: teoría de la relatividad especial y mecánica cuántica básica.",
            category="Física",
            thumbnail_url="https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=400&h=225&fit=crop",
            price=149.0,
            school_restricted=False,
            is_published=True
        )
        db.add_all([course1, course2, course3])
        db.commit()
        db.refresh(course1)
        db.refresh(course2)
        db.refresh(course3)

        # Create lessons
        lessons = [
            # Cálculo
            Lesson(course_id=course1.id, title="Introducción a Límites", video_url="https://www.youtube.com/embed/riXcZT2ICjA", description="Concepto fundamental del cálculo.", order=1, duration_mins=18),
            Lesson(course_id=course1.id, title="Reglas de Derivación", video_url="https://www.youtube.com/embed/5yfh5cf4-0U", description="Derivadas de funciones básicas.", order=2, duration_mins=22),
            Lesson(course_id=course1.id, title="Integrales Indefinidas", video_url="https://www.youtube.com/embed/rfG8ce4nNh0", description="Antiderivadas y técnicas de integración.", order=3, duration_mins=25),
            # Python
            Lesson(course_id=course2.id, title="Variables y Tipos de Datos", video_url="https://www.youtube.com/embed/kqtD5dpn9C8", description="Fundamentos de Python.", order=1, duration_mins=15),
            Lesson(course_id=course2.id, title="NumPy: Arrays y Operaciones", video_url="https://www.youtube.com/embed/QUT1VHiLmmI", description="Librería NumPy para cálculo numérico.", order=2, duration_mins=30),
            Lesson(course_id=course2.id, title="Pandas: DataFrames", video_url="https://www.youtube.com/embed/vmEHCJofslg", description="Manipulación de datos con Pandas.", order=3, duration_mins=35),
            # Física
            Lesson(course_id=course3.id, title="Postulados de la Relatividad", video_url="https://www.youtube.com/embed/yuD34tEpRFw", description="Los dos postulados de Einstein.", order=1, duration_mins=20),
            Lesson(course_id=course3.id, title="Dilatación del Tiempo", video_url="https://www.youtube.com/embed/IM630Z8lho8", description="Efectos relativistas del tiempo.", order=2, duration_mins=24),
        ]
        db.add_all(lessons)
        db.commit()

        # Create time slots for tutor
        days = [0, 1, 2, 3, 4]  # Mon-Fri
        for day in days:
            slot = TimeSlot(
                tutor_id=tutor.id,
                day_of_week=day,
                start_time="10:00",
                end_time="11:00",
                is_available=True,
                price_per_hour=200.0,
                school_restricted=False
            )
            db.add(slot)
            slot2 = TimeSlot(
                tutor_id=tutor.id,
                day_of_week=day,
                start_time="16:00",
                end_time="17:00",
                is_available=True,
                price_per_hour=200.0,
                school_restricted=True
            )
            db.add(slot2)
        db.commit()

        # Enroll student in course1
        enrollment = Enrollment(
            student_id=student.id,
            course_id=course1.id,
            progress=35
        )
        db.add(enrollment)
        db.commit()

        # Add review
        review = Review(
            course_id=course1.id,
            reviewer_id=student.id,
            rating=5,
            comment="Excelente curso, muy bien explicado. El profesor es muy claro."
        )
        db.add(review)
        db.commit()

        print("Seed completed successfully!")

    except Exception as e:
        print(f"Seed error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
