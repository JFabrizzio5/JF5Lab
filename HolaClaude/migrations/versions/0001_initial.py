"""initial owner + audit_log with PIN bcrypt seed

Revision ID: 0001_initial
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

PIN_HASH_SEED = "$2b$12$Kf76/waTMkT/10/k1qB2pOa0OFKACaXL9DqeZvQ/J.UP3FCC6I.oO"


def upgrade() -> None:
    op.create_table(
        "owner",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("face_descriptor", postgresql.ARRAY(sa.Float), nullable=False),
        sa.Column("pin_hash", sa.String, nullable=False, server_default=sa.text(f"'{PIN_HASH_SEED}'")),
        sa.Column("owner_locked", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("disabled", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("disabled_at", sa.DateTime, nullable=True),
        sa.Column("enrolled_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("failed_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_attempt_at", sa.DateTime, nullable=True),
        sa.CheckConstraint("pin_hash IS NOT NULL", name="owner_pin_not_null"),
        sa.CheckConstraint("length(pin_hash) > 20", name="owner_pin_hash_valid"),
    )

    op.create_table(
        "audit_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("kind", sa.String, nullable=False),
        sa.Column("ip", sa.String, nullable=True),
        sa.Column("ok", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("detail", postgresql.JSONB, nullable=True),
    )
    op.create_index("ix_audit_log_at", "audit_log", ["at"])
    op.create_index("ix_audit_log_kind", "audit_log", ["kind"])


def downgrade() -> None:
    # PIN irremovible: migracion no permite dropear la tabla owner
    raise RuntimeError("Owner table downgrade bloqueado por diseno")
