from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.properties.models.models import Property

class PropertyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int) -> list[Property]:
        result = await self.db.execute(select(Property).where(Property.user_id == user_id).order_by(Property.created_at.desc()))
        return result.scalars().all()

    async def get_by_id(self, property_id: int, user_id: int) -> Property | None:
        result = await self.db.execute(select(Property).where(Property.id == property_id, Property.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user_id: int, data: dict) -> Property:
        prop = Property(user_id=user_id, **data)
        self.db.add(prop)
        await self.db.commit()
        await self.db.refresh(prop)
        return prop

    async def update(self, prop: Property, data: dict) -> Property:
        for k, v in data.items():
            setattr(prop, k, v)
        await self.db.commit()
        await self.db.refresh(prop)
        return prop

    async def delete(self, prop: Property):
        await self.db.delete(prop)
        await self.db.commit()
