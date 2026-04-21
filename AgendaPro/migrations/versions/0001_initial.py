"""AgendaPro initial + RLS.

Revision ID: 0001
Revises:
Create Date: 2026-04-21
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


TENANT_TABLES = [
    "tenant_plans", "staff", "services",
    "availability_rules", "availability_exceptions",
    "customers", "appointments", "payments", "reminders", "reviews",
]


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
    bind.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))

    import sys, os
    sys.path.append(os.getcwd())
    from config.database import Base
    import modules.agenda.models  # noqa: F401
    Base.metadata.create_all(bind=bind)

    for t in TENANT_TABLES:
        bind.execute(sa.text(f"ALTER TABLE {t} ENABLE ROW LEVEL SECURITY"))
        bind.execute(sa.text(f"ALTER TABLE {t} FORCE ROW LEVEL SECURITY"))
        bind.execute(sa.text(f"""
            CREATE POLICY rls_{t}_isolation ON {t}
            USING (tenant_id::text = current_setting('app.tenant_id', true))
            WITH CHECK (tenant_id::text = current_setting('app.tenant_id', true))
        """))


def downgrade() -> None:
    bind = op.get_bind()
    for t in TENANT_TABLES:
        bind.execute(sa.text(f"DROP POLICY IF EXISTS rls_{t}_isolation ON {t}"))
        bind.execute(sa.text(f"ALTER TABLE IF EXISTS {t} DISABLE ROW LEVEL SECURITY"))
    import sys, os
    sys.path.append(os.getcwd())
    from config.database import Base
    import modules.agenda.models  # noqa: F401
    Base.metadata.drop_all(bind=bind)
