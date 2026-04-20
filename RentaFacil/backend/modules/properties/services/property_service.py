from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from modules.properties.repositories.property_repository import PropertyRepository

class PropertyService:
    def __init__(self, db: AsyncSession):
        self.repo = PropertyRepository(db)

    async def list_properties(self, user_id: int):
        return await self.repo.get_all(user_id)

    async def get_property(self, property_id: int, user_id: int):
        prop = await self.repo.get_by_id(property_id, user_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        return prop

    async def create_property(self, user_id: int, data: dict):
        return await self.repo.create(user_id, data)

    async def update_property(self, property_id: int, user_id: int, data: dict):
        prop = await self.get_property(property_id, user_id)
        return await self.repo.update(prop, {k: v for k, v in data.items() if v is not None})

    async def delete_property(self, property_id: int, user_id: int):
        prop = await self.get_property(property_id, user_id)
        await self.repo.delete(prop)
        return {"message": "Deleted"}
