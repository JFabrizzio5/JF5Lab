"""Tenant context extraction.

MVP: tenant_id llega por header `X-Tenant-Id` (UUID). Cuando haya ApiIam,
decodificar JWT y extraer claim `tenant_id` en este mismo hook.
"""
from fastapi import Header, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_sql_db, UUID_RE


async def get_tenant_id(
    x_tenant_id: str | None = Header(default=None),
    tenant: str | None = Query(default=None, description="Fallback tenant id para GETs directos de navegador"),
) -> str:
    """Acepta `X-Tenant-Id` (preferido) o `?tenant=<uuid>` (fallback para `<img src>`/`<a href>`)."""
    tid = x_tenant_id or tenant
    if not tid:
        raise HTTPException(status_code=401, detail="Falta X-Tenant-Id (header o query param ?tenant=)")
    if not UUID_RE.match(tid):
        raise HTTPException(status_code=400, detail="Tenant id inválido")
    return tid


async def tenant_db(tenant_id: str = Depends(get_tenant_id)):
    async for session in get_sql_db(tenant_id):
        yield session
