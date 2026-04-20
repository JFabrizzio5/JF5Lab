from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
)
from sqlalchemy.orm import relationship
from database import Base


class Workspace(Base):
    """Tenant isolation. Each user belongs to a workspace; all data is scoped here."""
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(80), unique=True, nullable=False)
    plan = Column(String(40), default="free")
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(200))
    role = Column(String(40), default="agent")  # owner | admin | agent
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    workspace = relationship("Workspace")


# CRM -------------------------------------------------------------------
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200))
    phone = Column(String(50), index=True)
    company = Column(String(200))
    tags = Column(JSON, default=list)
    notes = Column(Text)
    source = Column(String(60), default="manual")  # manual | whatsapp | web
    # Track which WhatsApp session imported/owns this contact so user can split
    # their contact lists by session (e.g. business number vs personal number).
    source_session_id = Column(Integer, ForeignKey("evolution_sessions.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Pipeline(Base):
    __tablename__ = "pipelines"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    stages = Column(JSON, default=list)  # ["Nuevo", "Contactado", "Propuesta", "Ganado", "Perdido"]


class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    title = Column(String(300), nullable=False)
    value = Column(Float, default=0)
    currency = Column(String(8), default="MXN")
    stage = Column(String(80), default="Nuevo")
    status = Column(String(30), default="open")  # open | won | lost
    owner_id = Column(Integer, ForeignKey("users.id"))
    expected_close = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    contact = relationship("Contact")


# CMS -------------------------------------------------------------------
class Content(Base):
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    kind = Column(String(30), default="page")  # page | post | snippet
    title = Column(String(300), nullable=False)
    slug = Column(String(160), index=True)
    body = Column(Text)
    blocks = Column(JSON, default=list)  # block-based content
    status = Column(String(20), default="draft")  # draft | published
    cover_url = Column(String(500))
    author_id = Column(Integer, ForeignKey("users.id"))
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Template builder ------------------------------------------------------
class Template(Base):
    """Reusable document templates: support responses, presentations, tech docs."""
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(60), default="general")  # support | presentation | tech_doc | general
    description = Column(Text)
    blocks = Column(JSON, default=list)  # [{type, content, ...}]
    variables = Column(JSON, default=list)  # [{key, label, default}]
    is_public = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Chat / Evolution ------------------------------------------------------
class EvolutionSession(Base):
    """Each user connects their own WhatsApp number via Evolution API. One session per agent."""
    __tablename__ = "evolution_sessions"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instance_name = Column(String(120), unique=True, nullable=False)  # Evolution instance id
    display_name = Column(String(200))
    phone_number = Column(String(50))
    status = Column(String(30), default="disconnected")  # connecting | connected | disconnected
    qr_code = Column(Text)  # last QR base64
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    # Nullable + ON DELETE SET NULL so conversations survive Evolution session teardown.
    # The actual FK constraint is applied in main.py via _migrate_conversation_fk.
    session_id = Column(Integer, ForeignKey("evolution_sessions.id", ondelete="SET NULL"), nullable=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    remote_jid = Column(String(120), index=True)  # WhatsApp JID e.g. 5215512345678@s.whatsapp.net
    # Preserves the original @lid JID after a user links a real phone, so future
    # webhook messages that still arrive as @lid can be routed to the same
    # conversation without prompting again.
    lid_jid = Column(String(120), index=True, nullable=True)
    contact_name = Column(String(200))
    contact_phone = Column(String(50))
    last_message = Column(Text)
    last_message_at = Column(DateTime)
    unread = Column(Integer, default=0)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    status = Column(String(30), default="open")  # open | pending | closed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LidPnMap(Base):
    """Bridges WhatsApp LID identifiers to real phone numbers (PN). Needed
    because Evolution v2 / Baileys v7 expose `participant: <lid>@lid` in group
    messages without the participant's PN. We reconstruct the mapping from
    `Chat.lastMessage.key.remoteJidAlt` (direct chats carry both forms) and
    by matching `pushName` across LID+PN entries in `findContacts`."""
    __tablename__ = "lid_pn_map"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    lid_jid = Column(String(120), nullable=False, index=True)
    pn_jid = Column(String(120), nullable=False, index=True)
    push_name = Column(String(200))
    source = Column(String(30), default="chat_alt")  # chat_alt | pushname | manual
    created_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    direction = Column(String(10))  # inbound | outbound
    body = Column(Text)
    media_url = Column(String(500))
    media_type = Column(String(40))  # image | audio | video | document
    evolution_message_id = Column(String(200))
    from_me = Column(Boolean, default=False)
    author_name = Column(String(200))
    # Digits-only phone of the message author (group messages). Lets us resolve
    # the display name from the CRM at read time — so renaming a contact later
    # retroactively updates every bubble attributed to them.
    author_phone = Column(String(50), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
