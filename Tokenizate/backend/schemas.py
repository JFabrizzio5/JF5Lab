from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from models import EditorRole, ReviewStatus, PlanType, SubscriptionStatus


# ── AUTH ─────────────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str
    editor: "EditorOut"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── PLAN / SUBSCRIPTION ──────────────────────────────────────────────────────

class PlanOut(BaseModel):
    id: int
    name: PlanType
    display_name: str
    price_monthly: int
    price_yearly: int
    max_editors: int
    max_reviews: int

    class Config:
        from_attributes = True


class SubscriptionOut(BaseModel):
    id: int
    plan_id: int
    status: SubscriptionStatus
    current_period_end: Optional[datetime]
    plan: Optional[PlanOut] = None

    class Config:
        from_attributes = True


class CheckoutRequest(BaseModel):
    plan_id: int
    billing: str = "monthly"  # "monthly" | "yearly"
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    checkout_url: str


# ── EDITOR ────────────────────────────────────────────────────────────────────

class EditorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[EditorRole] = EditorRole.editor


class EditorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[EditorRole] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None


class EditorOut(BaseModel):
    id: int
    name: str
    email: str
    role: EditorRole
    is_active: bool
    avatar_url: Optional[str]
    created_at: datetime
    subscription: Optional[SubscriptionOut] = None

    class Config:
        from_attributes = True


# ── REVIEW ────────────────────────────────────────────────────────────────────

class ReviewCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content_url: Optional[str] = None
    priority: Optional[str] = "medium"
    assigned_editor_id: Optional[int] = None
    deadline: Optional[datetime] = None


class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    priority: Optional[str] = None
    assigned_editor_id: Optional[int] = None
    deadline: Optional[datetime] = None


class ReviewStatusUpdate(BaseModel):
    status: ReviewStatus
    note: Optional[str] = None


class ReviewCommentCreate(BaseModel):
    comment: str


class ReviewCommentOut(BaseModel):
    id: int
    editor_id: int
    comment: str
    created_at: datetime
    editor: Optional[EditorOut] = None

    class Config:
        from_attributes = True


class ReviewHistoryOut(BaseModel):
    id: int
    old_status: Optional[ReviewStatus]
    new_status: ReviewStatus
    changed_by_id: int
    note: Optional[str]
    changed_at: datetime
    changed_by_editor: Optional[EditorOut] = None

    class Config:
        from_attributes = True


class ReviewOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    content_url: Optional[str]
    status: ReviewStatus
    priority: str
    assigned_editor_id: Optional[int]
    created_by_id: int
    deadline: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    assigned_editor: Optional[EditorOut] = None
    created_by_editor: Optional[EditorOut] = None
    comments: List[ReviewCommentOut] = []
    history: List[ReviewHistoryOut] = []

    class Config:
        from_attributes = True


class ReviewListOut(BaseModel):
    id: int
    title: str
    status: ReviewStatus
    priority: str
    assigned_editor_id: Optional[int]
    created_by_id: int
    deadline: Optional[datetime]
    created_at: datetime
    assigned_editor: Optional[EditorOut] = None

    class Config:
        from_attributes = True


Token.model_rebuild()
