import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, JSON, CheckConstraint, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from config.database import Base


class Owner(Base):
    __tablename__ = "owner"
    __table_args__ = (
        CheckConstraint("pin_hash IS NOT NULL", name="owner_pin_not_null"),
        CheckConstraint("length(pin_hash) > 20", name="owner_pin_hash_valid"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    face_descriptor = Column(ARRAY(Float), nullable=False)
    pin_hash = Column(String, nullable=False)
    owner_locked = Column(Boolean, nullable=False, default=True)
    disabled = Column(Boolean, nullable=False, default=False)
    disabled_at = Column(DateTime, nullable=True)
    enrolled_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    failed_attempts = Column(Integer, nullable=False, default=0)
    last_attempt_at = Column(DateTime, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    kind = Column(String, nullable=False, index=True)
    ip = Column(String, nullable=True)
    ok = Column(Boolean, nullable=False, default=True)
    detail = Column(JSON, nullable=True)
