from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")  # student/tutor/admin
    school = Column(String(20), nullable=False, default="OTHER")  # UAM/UNAM/POLI/IPN/ITESM/OTHER
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    courses = relationship("Course", back_populates="tutor")
    enrollments = relationship("Enrollment", back_populates="student")
    time_slots = relationship("TimeSlot", back_populates="tutor")
    bookings_as_student = relationship("Booking", foreign_keys="Booking.student_id", back_populates="student")
    bookings_as_tutor = relationship("Booking", foreign_keys="Booking.tutor_id", back_populates="tutor")
    reviews = relationship("Review", back_populates="reviewer")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # Matemáticas/Física/Química/Programación/Historia/Inglés/etc
    thumbnail_url = Column(String(500), nullable=True)
    price = Column(Float, default=0.0)  # 0 = free
    school_restricted = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tutor = relationship("User", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course", order_by="Lesson.order")
    enrollments = relationship("Enrollment", back_populates="course")
    reviews = relationship("Review", back_populates="course")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    video_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=1)
    duration_mins = Column(Integer, default=0)

    course = relationship("Course", back_populates="lessons")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Integer, default=0)  # 0-100

    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String(10), nullable=False)  # HH:MM
    end_time = Column(String(10), nullable=False)    # HH:MM
    is_available = Column(Boolean, default=True)
    price_per_hour = Column(Float, default=0.0)
    school_restricted = Column(Boolean, default=False)

    tutor = relationship("User", back_populates="time_slots")
    bookings = relationship("Booking", back_populates="slot")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False)
    date = Column(String(20), nullable=False)  # YYYY-MM-DD
    status = Column(String(20), default="pending")  # pending/confirmed/cancelled/completed
    subject = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", foreign_keys=[student_id], back_populates="bookings_as_student")
    tutor = relationship("User", foreign_keys=[tutor_id], back_populates="bookings_as_tutor")
    slot = relationship("TimeSlot", back_populates="bookings")
    reviews = relationship("Review", back_populates="booking")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="reviews")
    booking = relationship("Booking", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")
