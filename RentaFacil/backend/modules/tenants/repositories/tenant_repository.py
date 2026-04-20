from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from modules.tenants.models.models import Tenant, Contract

class TenantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int) -> list[Tenant]:
        result = await self.db.execute(select(Tenant).where(Tenant.user_id == user_id).order_by(Tenant.name))
        return result.scalars().all()

    async def get_by_id(self, tenant_id: int, user_id: int) -> Tenant | None:
        result = await self.db.execute(
            select(Tenant).where(Tenant.id == tenant_id, Tenant.user_id == user_id)
            .options(selectinload(Tenant.contracts))
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, data: dict) -> Tenant:
        tenant = Tenant(user_id=user_id, **data)
        self.db.add(tenant)
        await self.db.commit()
        await self.db.refresh(tenant)
        return tenant

    async def update(self, tenant: Tenant, data: dict) -> Tenant:
        for k, v in data.items():
            setattr(tenant, k, v)
        await self.db.commit()
        await self.db.refresh(tenant)
        return tenant

    async def delete(self, tenant: Tenant):
        await self.db.delete(tenant)
        await self.db.commit()

class ContractRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int) -> list[Contract]:
        result = await self.db.execute(
            select(Contract).where(Contract.user_id == user_id)
            .options(selectinload(Contract.tenant), selectinload(Contract.property))
            .order_by(Contract.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_id(self, contract_id: int, user_id: int) -> Contract | None:
        result = await self.db.execute(
            select(Contract).where(Contract.id == contract_id, Contract.user_id == user_id)
            .options(selectinload(Contract.tenant), selectinload(Contract.property), selectinload(Contract.payments))
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, data: dict) -> Contract:
        contract = Contract(user_id=user_id, **data)
        self.db.add(contract)
        await self.db.commit()
        await self.db.refresh(contract)
        return contract

    async def update(self, contract: Contract, data: dict) -> Contract:
        for k, v in data.items():
            setattr(contract, k, v)
        await self.db.commit()
        await self.db.refresh(contract)
        return contract
