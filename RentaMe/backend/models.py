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
    role = Column(String, default="customer")  # superadmin / vendor / customer
    avatar_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VendorProfile(Base):
    __tablename__ = "vendor_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    # Landing customization
    slug = Column(String, unique=True, nullable=False, index=True)
    business_name = Column(String, nullable=False)
    tagline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    theme_color = Column(String, default="#6366f1")
    accent_color = Column(String, default="#f59e0b")
    # Contact & social
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    facebook_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    tiktok_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    # Policies
    cancellation_policy = Column(Text, nullable=True)
    deposit_percent = Column(Float, default=30.0)
    # Stripe
    stripe_account_id = Column(String, nullable=True)
    stripe_onboarding_complete = Column(Boolean, default=False)
    platform_fee_percent = Column(Float, default=5.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
    items = relationship("RentalItem", back_populates="vendor")
    bookings = relationship("Booking", back_populates="vendor")


class RentalItem(Base):
    __tablename__ = "rental_items"
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendor_profiles.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, default="general")
    images_json = Column(Text, nullable=True)
    price_per_hour = Column(Float, nullable=True)
    price_per_day = Column(Float, nullable=True)
    price_per_weekend = Column(Float, nullable=True)
    price_per_week = Column(Float, nullable=True)
    quantity = Column(Integer, default=1)
    min_rental_hours = Column(Integer, default=1)
    max_rental_days = Column(Integer, nullable=True)
    advance_booking_days = Column(Integer, default=0)
    specifications_json = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    included_json = Column(Text, nullable=True)
    not_included_json = Column(Text, nullable=True)
    deposit_amount = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    vendor = relationship("VendorProfile", back_populates="items")


class AvailabilityBlock(Base):
    __tablename__ = "availability_blocks"
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendor_profiles.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("rental_items.id"), nullable=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    reason = Column(String, default="blocked")
    note = Column(String, nullable=True)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendor_profiles.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("rental_items.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    rental_unit = Column(String, default="day")
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    deposit_amount = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    status = Column(String, default="inquiry")
    notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    vendor = relationship("VendorProfile", back_populates="bookings")
    item = relationship("RentalItem")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendor_profiles.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="mxn")
    stripe_payment_intent_id = Column(String, nullable=True)
    status = Column(String, default="pending")
    platform_fee = Column(Float, default=0.0)
    vendor_amount = Column(Float, default=0.0)
    payment_type = Column(String, default="deposit")
    created_at = Column(DateTime, default=datetime.utcnow)
    booking = relationship("Booking")
