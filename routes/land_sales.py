from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import os

from models import LandSale, LandSaleCreate, User
from auth_utils import get_current_admin_user, get_current_admin_or_colaborador

router = APIRouter()

def get_db():
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME', 'prados_paraiso')]
    return db

@router.post("/", response_model=LandSale)
async def create_land_sale(land_sale: LandSaleCreate):
    """Create a new land sale submission"""
    db = get_db()
    
    land_sale_data = LandSale(**land_sale.dict())
    land_sale_dict = land_sale_data.dict()
    
    # Convert datetime to ISO string for MongoDB
    land_sale_dict['created_at'] = land_sale_dict['created_at'].isoformat()
    
    await db.land_sales.insert_one(land_sale_dict)
    
    return land_sale_data

@router.get("/", response_model=List[LandSale])
async def get_all_land_sales(current_user: User = Depends(get_current_admin_or_colaborador)):
    """Get all land sale submissions - Admin and Colaborador only"""
    db = get_db()
    
    land_sales = await db.land_sales.find({}, {"_id": 0}).to_list(1000)
    return land_sales

@router.delete("/{land_sale_id}")
async def delete_land_sale(land_sale_id: str, current_user: User = Depends(get_current_admin_user)):
    """Delete a land sale submission - Admin only"""
    db = get_db()
    
    result = await db.land_sales.delete_one({"id": land_sale_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Land sale not found")
    
    return {"message": "Land sale deleted successfully"}