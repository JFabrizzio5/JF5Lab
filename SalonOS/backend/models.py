from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="client")  # superadmin / venue_owner / venue_staff / client
    avatar_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    tagline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    theme_color = Column(String, default="#7c3aed")
    accent_color = Column(String, default="#f59e0b")
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    whatsapp_number = Column(String, nullable=True)
    whatsapp_message = Column(String, default="Hola, me interesa reservar un evento en su salón.")
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    stripe_account_id = Column(String, nullable=True)
    stripe_onboarding_complete = Column(Boolean, default=False)
    platform_fee_percent = Column(Float, default=5.0)
    gallery_json = Column(Text, nullable=True)
    amenities_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", foreign_keys=[owner_id])
    branches = relationship("VenueBranch", back_populates="venue")
    spaces = relationship("EventSpace", back_populates="venue")
    clients = relationship("Client", back_populates="venue")


class VenueBranch(Base):
    __tablename__ = "venue_branches"
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    venue = relationship("Venue", back_populates="branches")
    spaces = relationship("EventSpace", back_populates="branch")


class EventSpace(Base):
    __tablename__ = "event_spaces"
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("venue_branches.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, default=50)
    price_per_hour = Column(Float, default=0.0)
    price_event = Column(Float, default=0.0)
    images_json = Column(Text, nullable=True)
    amenities_json = Column(Text, nullable=True)
    floor_plan_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    venue = relationship("Venue", back_populates="spaces")
    branch = relationship("VenueBranch", back_populates="spaces")


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    source = Column(String, default="web")
    created_at = Column(DateTime, default=datetime.utcnow)
    venue = relationship("Venue", back_populates="clients")


class EventBooking(Base):
    __tablename__ = "event_bookings"
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    space_id = Column(Integer, ForeignKey("event_spaces.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    title = Column(String, nullable=False)
    event_type = Column(String, default="boda")
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    guests_count = Column(Integer, default=0)
    status = Column(String, default="inquiry")
    total_price = Column(Float, default=0.0)
    deposit_amount = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    venue = relationship("Venue")
    space = relationship("EventSpace")
    client = relationship("Client")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("event_bookings.id"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="mxn")
    stripe_payment_intent_id = Column(String, nullable=True)
    status = Column(String, default="pending")
    platform_fee = Column(Float, default=0.0)
    venue_amount = Column(Float, default=0.0)
    payment_type = Column(String, default="deposit")
    created_at = Column(DateTime, default=datetime.utcnow)
    booking = relationship("EventBooking")


class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    venue = relationship("Venue")
    client = relationship("Client")
    messages = relationship("ChatMessage", back_populates="room")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    sender_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sender_name = Column(String, nullable=False)
    sender_type = Column(String, default="staff")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    room = relationship("ChatRoom", back_populates="messages")
