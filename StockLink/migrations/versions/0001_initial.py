"""StockLink initial schema + RLS

Revision ID: 0001
Revises:
Create Date: 2026-04-21

Crea todas las tablas de dominio usando `Base.metadata.create_all` y aplica Row
Level Security (RLS) sobre `tenant_id` en cada tabla multi-tenant. RLS lee el
valor de `current_setting('app.tenant_id', true)` seteado por FastAPI en cada
sesión vía `tenant_db` dependency.
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


TENANT_TABLES = [
    "tenant_plans", "api_keys", "warehouses", "locations", "categories", "suppliers",
    "items", "stock_levels", "movements", "labels", "employees", "shifts",
    "attendance", "webhook_events",
]


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
    bind.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))

    # Importar modelos y crear todas las tablas del metadata
    import sys, os
    sys.path.append(os.getcwd())
    from config.database import Base
    import modules.inventory.models  # noqa: F401 — registra todas las tablas

    Base.metadata.create_all(bind=bind)

    # Row Level Security
    for t in TENANT_TABLES:
        bind.execute(sa.text(f"ALTER TABLE {t} ENABLE ROW LEVEL SECURITY"))
        bind.execute(sa.text(f"ALTER TABLE {t} FORCE ROW LEVEL SECURITY"))
        bind.execute(sa.text(f"""
            CREATE POLICY rls_{t}_isolation ON {t}
            USING (tenant_id::text = current_setting('app.tenant_id', true))
            WITH CHECK (tenant_id::text = current_setting('app.tenant_id', true))
        """))

    # Tabla `tenants` no tiene tenant_id — políticamente abierta (admin-only vía app layer)
    # Tabla `plans` es catálogo global, abierta


def downgrade() -> None:
    bind = op.get_bind()
    for t in TENANT_TABLES:
        bind.execute(sa.text(f"DROP POLICY IF EXISTS rls_{t}_isolation ON {t}"))
        bind.execute(sa.text(f"ALTER TABLE IF EXISTS {t} DISABLE ROW LEVEL SECURITY"))
    import sys, os
    sys.path.append(os.getcwd())
    from config.database import Base
    import modules.inventory.models  # noqa: F401

    Base.metadata.drop_all(bind=bind)
