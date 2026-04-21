"""PorCobrar initial + RLS

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


# payment_links SE QUEDA SIN RLS: los tokens son secure random y el endpoint
# `/public/pay/{token}` resuelve el tenant a partir del link antes de consultar
# otras tablas. El resto de tablas tiene RLS con FORCE.
TENANT_TABLES = [
    "tenant_plans", "debtors", "invoices",
    "dunning_flows", "dunning_templates", "dunning_runs",
    "payments", "payment_score_events", "notes_log",
]


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))

    import sys, os
    sys.path.append(os.getcwd())
    from config.database import Base
    import modules.cobranza.models  # noqa: F401
    Base.metadata.create_all(bind=bind)

    for t in TENANT_TABLES:
        bind.execute(sa.text(f"ALTER TABLE {t} ENABLE ROW LEVEL SECURITY"))
        bind.execute(sa.text(f"ALTER TABLE {t} FORCE ROW LEVEL SECURITY"))
        bind.execute(sa.text(f"""
            CREATE POLICY rls_{t}_isolation ON {t}
            USING (tenant_id::text = current_setting('app.tenant_id', true))
            WITH CHECK (tenant_id::text = current_setting('app.tenant_id', true))
        """))

    # GRANTs al rol de la app (si existe)
    bind.execute(sa.text("""
        DO $$
        BEGIN
          IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'porcobrar_app') THEN
            GRANT USAGE ON SCHEMA public TO porcobrar_app;
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO porcobrar_app;
            GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO porcobrar_app;
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO porcobrar_app;
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO porcobrar_app;
          END IF;
        END $$;
    """))


def downgrade() -> None:
    bind = op.get_bind()
    for t in TENANT_TABLES:
        bind.execute(sa.text(f"DROP POLICY IF EXISTS rls_{t}_isolation ON {t}"))
        bind.execute(sa.text(f"ALTER TABLE IF EXISTS {t} DISABLE ROW LEVEL SECURITY"))
    import sys, os
    sys.path.append(os.getcwd())
    from config.database import Base
    import modules.cobranza.models  # noqa: F401
    Base.metadata.drop_all(bind=bind)
