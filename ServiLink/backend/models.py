from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


class UserRole(str, enum.Enum):
    superadmin = "superadmin"
    client = "client"
    freelancer = "freelancer"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class SubscriptionPlan(str, enum.Enum):
    free = "free"
    basic = "basic"
    pro = "pro"
    premium = "premium"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default=UserRole.client)
    avatar_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("ProfessionalProfile", back_populates="user", uselist=False)
    bookings_as_client = relationship("Booking", foreign_keys="Booking.client_id", back_populates="client")
    bookings_as_professional = relationship("Booking", foreign_keys="Booking.professional_id", back_populates="professional")
    reviews_given = relationship("Review", foreign_keys="Review.client_id", back_populates="client")
    reviews_received = relationship("Review", foreign_keys="Review.professional_id", back_populates="professional")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, default="🔧")
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    professional_categories = relationship("ProfessionalCategory", back_populates="category")


class ProfessionalProfile(Base):
    __tablename__ = "professional_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(Text, nullable=True)
    hourly_rate = Column(Float, default=0.0)
    experience_years = Column(Integer, default=0)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    subscription_plan = Column(String, default=SubscriptionPlan.free)
    rating_avg = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    total_jobs = Column(Integer, default=0)
    portfolio_urls = Column(Text, nullable=True)
    cover_url = Column(String, nullable=True)
    tagline = Column(String, nullable=True)
    theme_color = Column(String, default="#6366f1")
    services_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profile")
    categories = relationship("ProfessionalCategory", back_populates="professional")


class ProfessionalCategory(Base):
    __tablename__ = "professional_categories"
    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professional_profiles.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    professional = relationship("ProfessionalProfile", back_populates="categories")
    category = relationship("Category", back_populates="professional_categories")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    professional_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text, nullable=True)
    status = Column(String, default=BookingStatus.pending)
    client_address = Column(String, nullable=True)
    client_lat = Column(Float, nullable=True)
    client_lng = Column(Float, nullable=True)
    price = Column(Float, nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("User", foreign_keys=[client_id], back_populates="bookings_as_client")
    professional = relationship("User", foreign_keys=[professional_id], back_populates="bookings_as_professional")
    category = relationship("Category")
    review = relationship("Review", back_populates="booking", uselist=False)


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    professional_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="review")
    client = relationship("User", foreign_keys=[client_id], back_populates="reviews_given")
    professional = relationship("User", foreign_keys=[professional_id], back_populates="reviews_received")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    plan = Column(String, default=SubscriptionPlan.free)
    status = Column(String, default="active")
    price_monthly = Column(Float, default=0.0)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("User", foreign_keys=[client_id])
    professional = relationship("User", foreign_keys=[professional_id])
    messages = relationship("ChatMessage", back_populates="room", order_by="ChatMessage.created_at")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id])
