"""Tenant context extraction.

Acepta tenant_id por header `X-Tenant-Id` (preferido) o query `?tenant=<uuid>`
(fallback para enlaces directos).
"""
from fastapi import Header, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_sql_db, UUID_RE


async def get_tenant_id(
    x_tenant_id: str | None = Header(default=None),
    tenant: str | None = Query(default=None),
) -> str:
    tid = x_tenant_id or tenant
    if not tid:
        raise HTTPException(status_code=401, detail="Falta X-Tenant-Id (header) o ?tenant= (query).")
    if not UUID_RE.match(tid):
        raise HTTPException(status_code=400, detail="Tenant id invalido")
    return tid


async def tenant_db(tenant_id: str = Depends(get_tenant_id)):
    async for session in get_sql_db(tenant_id):
        yield session


async def raw_db():
    async for session in get_sql_db(None):
        yield session
