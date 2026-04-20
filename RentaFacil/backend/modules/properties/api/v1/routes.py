from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from config.database import get_db
from core.dependencies import get_current_user
from modules.properties.services.property_service import PropertyService

router = APIRouter(prefix="/properties/v1", tags=["properties"])

class PropertyCreate(BaseModel):
    name: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    property_type: Optional[str] = "apartment"
    monthly_rent: float
    status: Optional[str] = "vacant"
    notes: Optional[str] = None

class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    property_type: Optional[str] = None
    monthly_rent: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

@router.get("/")
async def list_properties(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PropertyService(db).list_properties(user.id)

@router.post("/")
async def create_property(body: PropertyCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PropertyService(db).create_property(user.id, body.model_dump())

@router.get("/{property_id}")
async def get_property(property_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PropertyService(db).get_property(property_id, user.id)

@router.put("/{property_id}")
async def update_property(property_id: int, body: PropertyUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PropertyService(db).update_property(property_id, user.id, body.model_dump())

@router.delete("/{property_id}")
async def delete_property(property_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await PropertyService(db).delete_property(property_id, user.id)
