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
    role = Column(String, default="attendee")  # superadmin / organizer / attendee
    avatar_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Convention(Base):
    __tablename__ = "conventions"
    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    edition = Column(String, nullable=True)
    tagline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)
    theme_color = Column(String, default="#7c3aed")
    accent_color = Column(String, default="#f59e0b")
    bg_color = Column(String, default="#0a0a0f")
    font_style = Column(String, default="modern")
    venue_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default="draft")
    max_attendees = Column(Integer, nullable=True)
    website = Column(String, nullable=True)
    social_json = Column(Text, nullable=True)
    rules_text = Column(Text, nullable=True)
    stripe_account_id = Column(String, nullable=True)
    stripe_onboarding_complete = Column(Boolean, default=False)
    platform_fee_percent = Column(Float, default=5.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    organizer = relationship("User", foreign_keys=[organizer_id])
    stages = relationship("Stage", back_populates="convention")
    stands = relationship("Stand", back_populates="convention")
    sponsors = relationship("Sponsor", back_populates="convention")
    ticket_types = relationship("TicketType", back_populates="convention")
    tournaments = relationship("Tournament", back_populates="convention")


class Stage(Base):
    __tablename__ = "stages"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=True)
    color = Column(String, default="#6366f1")
    location_in_venue = Column(String, nullable=True)
    stream_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    convention = relationship("Convention", back_populates="stages")
    sessions = relationship("Session", back_populates="stage")


class Speaker(Base):
    __tablename__ = "speakers"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    is_keynote = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)
    speaker_id = Column(Integer, ForeignKey("speakers.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    session_type = Column(String, default="talk")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    tags_json = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    stage = relationship("Stage", back_populates="sessions")
    speaker = relationship("Speaker")


class Stand(Base):
    __tablename__ = "stands"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    number = Column(String, nullable=False)
    name = Column(String, nullable=True)
    category = Column(String, default="general")
    size = Column(String, default="standard")
    price = Column(Float, default=0.0)
    status = Column(String, default="available")
    x_pos = Column(Float, nullable=True)
    y_pos = Column(Float, nullable=True)
    width = Column(Float, default=5.0)
    height = Column(Float, default=5.0)
    contact_name = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    convention = relationship("Convention", back_populates="stands")


class Sponsor(Base):
    __tablename__ = "sponsors"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    name = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    website = Column(String, nullable=True)
    tier = Column(String, default="bronze")
    amount_sponsored = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    convention = relationship("Convention", back_populates="sponsors")


class TicketType(Base):
    __tablename__ = "ticket_types"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, default=0.0)
    quantity_total = Column(Integer, nullable=True)
    quantity_sold = Column(Integer, default=0)
    benefits_json = Column(Text, nullable=True)
    color = Column(String, default="#6366f1")
    sale_start = Column(DateTime, nullable=True)
    sale_end = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    convention = relationship("Convention", back_populates="ticket_types")


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_type_id = Column(Integer, ForeignKey("ticket_types.id"), nullable=False)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    attendee_name = Column(String, nullable=False)
    attendee_email = Column(String, nullable=False)
    attendee_phone = Column(String, nullable=True)
    qr_code = Column(String, nullable=True)
    status = Column(String, default="pending")
    payment_id = Column(Integer, ForeignKey("ticket_payments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    ticket_type = relationship("TicketType")


class TicketPayment(Base):
    __tablename__ = "ticket_payments"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    stripe_payment_intent_id = Column(String, nullable=True)
    stripe_session_id = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="mxn")
    platform_fee = Column(Float, default=0.0)
    organizer_amount = Column(Float, default=0.0)
    status = Column(String, default="pending")
    buyer_name = Column(String, nullable=False)
    buyer_email = Column(String, nullable=False)
    items_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True, index=True)
    convention_id = Column(Integer, ForeignKey("conventions.id"), nullable=False)
    name = Column(String, nullable=False)
    game = Column(String, nullable=True)
    format = Column(String, default="single_elim")
    max_participants = Column(Integer, default=32)
    participants_count = Column(Integer, default=0)
    prize_pool = Column(Float, default=0.0)
    prize_description = Column(Text, nullable=True)
    entry_fee = Column(Float, default=0.0)
    start_time = Column(DateTime, nullable=True)
    status = Column(String, default="open")
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=True)
    rules_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    convention = relationship("Convention", back_populates="tournaments")


class TournamentRegistration(Base):
    __tablename__ = "tournament_registrations"
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    player_name = Column(String, nullable=False)
    player_email = Column(String, nullable=False)
    player_tag = Column(String, nullable=True)
    status = Column(String, default="registered")
    created_at = Column(DateTime, default=datetime.utcnow)
    tournament = relationship("Tournament")
