from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from datetime import date
from config.database import get_db
from core.dependencies import get_current_user
from modules.tenants.services.tenant_service import TenantService, ContractService

router = APIRouter(tags=["tenants"])

class TenantCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    rfc: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    rfc: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class ContractCreate(BaseModel):
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    rent_amount: float
    deposit_amount: Optional[float] = 0
    status: Optional[str] = "active"
    notes: Optional[str] = None

class ContractUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    rent_amount: Optional[float] = None
    deposit_amount: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

tenants_router = APIRouter(prefix="/tenants/v1")
contracts_router = APIRouter(prefix="/contracts/v1")

@tenants_router.get("/")
async def list_tenants(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await TenantService(db).list_tenants(user.id)

@tenants_router.post("/")
async def create_tenant(body: TenantCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await TenantService(db).create_tenant(user.id, body.model_dump())

@tenants_router.get("/{tenant_id}")
async def get_tenant(tenant_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await TenantService(db).get_tenant(tenant_id, user.id)

@tenants_router.put("/{tenant_id}")
async def update_tenant(tenant_id: int, body: TenantUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await TenantService(db).update_tenant(tenant_id, user.id, body.model_dump())

@tenants_router.delete("/{tenant_id}")
async def delete_tenant(tenant_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await TenantService(db).delete_tenant(tenant_id, user.id)

@contracts_router.get("/")
async def list_contracts(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await ContractService(db).list_contracts(user.id)

@contracts_router.post("/")
async def create_contract(body: ContractCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await ContractService(db).create_contract(user.id, body.model_dump())

@contracts_router.get("/{contract_id}")
async def get_contract(contract_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await ContractService(db).get_contract(contract_id, user.id)

@contracts_router.put("/{contract_id}")
async def update_contract(contract_id: int, body: ContractUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await ContractService(db).update_contract(contract_id, user.id, body.model_dump())
