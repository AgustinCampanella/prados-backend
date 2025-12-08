from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import os

from models import Referral, ReferralCreate, User
from auth_utils import get_current_admin_user, get_current_admin_or_colaborador

router = APIRouter()

def get_db():
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME', 'prados_paraiso')]
    return db

@router.post("/", response_model=Referral)
async def create_referral(referral: ReferralCreate):
    """Create a new referral submission"""
    db = get_db()
    
    referral_data = Referral(**referral.dict())
    referral_dict = referral_data.dict()
    
    # Convert datetime to ISO string for MongoDB
    referral_dict['created_at'] = referral_dict['created_at'].isoformat()
    
    await db.referrals.insert_one(referral_dict)
    
    return referral_data

@router.get("/", response_model=List[Referral])
async def get_all_referrals(current_user: User = Depends(get_current_admin_or_colaborador)):
    """Get all referrals - Admin and Colaborador only"""
    db = get_db()
    
    referrals = await db.referrals.find({}, {"_id": 0}).to_list(1000)
    return referrals

@router.delete("/{referral_id}")
async def delete_referral(referral_id: str, current_user: User = Depends(get_current_admin_user)):
    """Delete a referral - Admin only"""
    db = get_db()
    
    result = await db.referrals.delete_one({"id": referral_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Referral not found")
    
    return {"message": "Referral deleted successfully"}