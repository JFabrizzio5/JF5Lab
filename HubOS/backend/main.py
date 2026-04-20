from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
import models  # noqa — registers ORM

from routers import auth, contacts, deals, content, templates, chat

Base.metadata.create_all(bind=engine)


def _migrate_conversation_fk():
    """Allow conversations to survive session deletion — nullable session_id
    with ON DELETE SET NULL. Idempotent."""
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE conversations ALTER COLUMN session_id DROP NOT NULL"
            ))
        except Exception:
            pass
        try:
            # Drop existing FK if any, then re-create with ON DELETE SET NULL
            conn.execute(text(
                "ALTER TABLE conversations DROP CONSTRAINT IF EXISTS conversations_session_id_fkey"
            ))
            conn.execute(text(
                "ALTER TABLE conversations ADD CONSTRAINT conversations_session_id_fkey "
                "FOREIGN KEY (session_id) REFERENCES evolution_sessions(id) ON DELETE SET NULL"
            ))
        except Exception as e:
            print(f"[migrate] FK alter skipped: {e}")

_migrate_conversation_fk()


def _backfill_conversation_owner():
    """Existing conversations may have assigned_to=NULL.
    Derive from session's user_id so list_conversations (which filters by
    assigned_to) shows them."""
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text("""
                UPDATE conversations c
                SET assigned_to = s.user_id
                FROM evolution_sessions s
                WHERE c.session_id = s.id AND c.assigned_to IS NULL
            """))
        except Exception as e:
            print(f"[migrate] backfill assigned_to skipped: {e}")

_backfill_conversation_owner()


def _migrate_contact_session_col():
    """Add source_session_id column to contacts if missing."""
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE contacts ADD COLUMN IF NOT EXISTS source_session_id INTEGER "
                "REFERENCES evolution_sessions(id) ON DELETE SET NULL"
            ))
        except Exception as e:
            print(f"[migrate] contacts.source_session_id skipped: {e}")

_migrate_contact_session_col()


def _migrate_conversation_lid_col():
    """Add lid_jid column to conversations if missing. Stores the original
    @lid JID after a user links a real phone, so inbound @lid messages still
    route to the same conversation without re-prompting."""
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE conversations ADD COLUMN IF NOT EXISTS lid_jid VARCHAR(120)"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_conversations_lid_jid ON conversations(lid_jid)"
            ))
        except Exception as e:
            print(f"[migrate] conversations.lid_jid skipped: {e}")

_migrate_conversation_lid_col()


def _backfill_conversation_preview():
    """Populate conversations.last_message / last_message_at from their newest
    message. Earlier sync code added messages without touching these columns,
    leaving the chat list with blank previews and broken sort order."""
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text("""
                UPDATE conversations c
                SET last_message_at = sub.ts,
                    last_message = COALESCE(c.last_message, sub.body)
                FROM (
                    SELECT DISTINCT ON (conversation_id)
                        conversation_id, timestamp AS ts, body
                    FROM messages
                    ORDER BY conversation_id, timestamp DESC
                ) sub
                WHERE c.id = sub.conversation_id
                  AND (c.last_message_at IS NULL OR sub.ts > c.last_message_at)
            """))
        except Exception as e:
            print(f"[migrate] backfill conv preview skipped: {e}")

_backfill_conversation_preview()


def _migrate_message_author_phone_col():
    """Add author_phone so group messages remember who sent them. Lets the UI
    resolve the display name via the CRM at read time — renaming a contact
    later retroactively updates every bubble attributed to them."""
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE messages ADD COLUMN IF NOT EXISTS author_phone VARCHAR(50)"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_messages_author_phone ON messages(author_phone)"
            ))
        except Exception as e:
            print(f"[migrate] messages.author_phone skipped: {e}")

_migrate_message_author_phone_col()


def _migrate_lid_pn_unique():
    """Enforce one PN per (workspace, lid). Table itself is auto-created by
    Base.metadata.create_all; only the composite unique index needs an extra
    pass because SQLAlchemy can't express it cleanly on this model."""
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text(
                "CREATE UNIQUE INDEX IF NOT EXISTS ix_lid_pn_unique "
                "ON lid_pn_map(workspace_id, lid_jid)"
            ))
        except Exception as e:
            print(f"[migrate] lid_pn_map unique skipped: {e}")

_migrate_lid_pn_unique()

app = FastAPI(title="HubOS API", version="1.0.0", description="CRM + CMS + Evolution chat + Template builder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(deals.router)
app.include_router(content.router)
app.include_router(templates.router)
app.include_router(chat.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "HubOS API"}
