from sqlalchemy import String, Numeric, ForeignKey, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base, TimestampMixin
from datetime import date

class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    rfc: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    owner = relationship("User", back_populates="tenants")
    contracts = relationship("Contract", back_populates="tenant")

class Contract(Base, TimestampMixin):
    __tablename__ = "contracts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    rent_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    deposit_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    status: Mapped[str] = mapped_column(String(20), default="active")
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    owner = relationship("User", back_populates="contracts")
    property = relationship("Property", back_populates="contracts")
    tenant = relationship("Tenant", back_populates="contracts")
    payments = relationship("Payment", back_populates="contract", cascade="all, delete-orphan")
