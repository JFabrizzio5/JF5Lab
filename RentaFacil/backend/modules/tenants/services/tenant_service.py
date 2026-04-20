from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from modules.tenants.repositories.tenant_repository import TenantRepository, ContractRepository

class TenantService:
    def __init__(self, db: AsyncSession):
        self.repo = TenantRepository(db)

    async def list_tenants(self, user_id: int):
        return await self.repo.get_all(user_id)

    async def get_tenant(self, tenant_id: int, user_id: int):
        tenant = await self.repo.get_by_id(tenant_id, user_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return tenant

    async def create_tenant(self, user_id: int, data: dict):
        return await self.repo.create(user_id, data)

    async def update_tenant(self, tenant_id: int, user_id: int, data: dict):
        tenant = await self.get_tenant(tenant_id, user_id)
        return await self.repo.update(tenant, {k: v for k, v in data.items() if v is not None})

    async def delete_tenant(self, tenant_id: int, user_id: int):
        tenant = await self.get_tenant(tenant_id, user_id)
        await self.repo.delete(tenant)
        return {"message": "Deleted"}

class ContractService:
    def __init__(self, db: AsyncSession):
        self.repo = ContractRepository(db)

    async def list_contracts(self, user_id: int):
        return await self.repo.get_all(user_id)

    async def get_contract(self, contract_id: int, user_id: int):
        contract = await self.repo.get_by_id(contract_id, user_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        return contract

    async def create_contract(self, user_id: int, data: dict):
        return await self.repo.create(user_id, data)

    async def update_contract(self, contract_id: int, user_id: int, data: dict):
        contract = await self.get_contract(contract_id, user_id)
        return await self.repo.update(contract, {k: v for k, v in data.items() if v is not None})
