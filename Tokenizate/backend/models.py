from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import relationship
from database import Base
import enum


class EditorRole(str, enum.Enum):
    editor = "editor"
    senior_editor = "senior_editor"
    admin = "admin"


class ReviewStatus(str, enum.Enum):
    draft = "draft"
    in_review = "in_review"
    revision_required = "revision_required"
    approved = "approved"
    rejected = "rejected"


class PlanType(str, enum.Enum):
    free = "free"
    starter = "starter"
    pro = "pro"
    enterprise = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    trialing = "trialing"
    canceled = "canceled"
    past_due = "past_due"


# ── SAAS PLAN ────────────────────────────────────────────────────────────────

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(PlanType), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    price_monthly = Column(BigInteger, nullable=False, default=0)  # cents
    price_yearly = Column(BigInteger, nullable=False, default=0)   # cents
    max_editors = Column(Integer, default=1)
    max_reviews = Column(Integer, default=10)
    stripe_price_id_monthly = Column(String(200), nullable=True)
    stripe_price_id_yearly = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    editor_id = Column(Integer, ForeignKey("editors.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.trialing)
    stripe_customer_id = Column(String(200), nullable=True)
    stripe_subscription_id = Column(String(200), nullable=True)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    editor = relationship("Editor", back_populates="subscription")
    plan = relationship("Plan", back_populates="subscriptions")


# ── EDITOR ────────────────────────────────────────────────────────────────────

class Editor(Base):
    __tablename__ = "editors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(EditorRole), default=EditorRole.editor)
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscription = relationship("Subscription", back_populates="editor", uselist=False)
    assigned_reviews = relationship("ReviewProcess", back_populates="assigned_editor", foreign_keys="ReviewProcess.assigned_editor_id")
    created_reviews = relationship("ReviewProcess", back_populates="created_by_editor", foreign_keys="ReviewProcess.created_by_id")
    comments = relationship("ReviewComment", back_populates="editor")
    history_entries = relationship("ReviewHistory", back_populates="changed_by_editor")


# ── REVIEW ────────────────────────────────────────────────────────────────────

class ReviewProcess(Base):
    __tablename__ = "review_processes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    content_url = Column(String(500), nullable=True)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.draft)
    priority = Column(Enum("low", "medium", "high", "urgent"), default="medium")
    assigned_editor_id = Column(Integer, ForeignKey("editors.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("editors.id"), nullable=False)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assigned_editor = relationship("Editor", back_populates="assigned_reviews", foreign_keys=[assigned_editor_id])
    created_by_editor = relationship("Editor", back_populates="created_reviews", foreign_keys=[created_by_id])
    comments = relationship("ReviewComment", back_populates="review", cascade="all, delete-orphan")
    history = relationship("ReviewHistory", back_populates="review", cascade="all, delete-orphan")


class ReviewComment(Base):
    __tablename__ = "review_comments"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("review_processes.id"), nullable=False)
    editor_id = Column(Integer, ForeignKey("editors.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("ReviewProcess", back_populates="comments")
    editor = relationship("Editor", back_populates="comments")


class ReviewHistory(Base):
    __tablename__ = "review_history"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("review_processes.id"), nullable=False)
    old_status = Column(Enum(ReviewStatus), nullable=True)
    new_status = Column(Enum(ReviewStatus), nullable=False)
    changed_by_id = Column(Integer, ForeignKey("editors.id"), nullable=False)
    note = Column(String(500), nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("ReviewProcess", back_populates="history")
    changed_by_editor = relationship("Editor", back_populates="history_entries")
