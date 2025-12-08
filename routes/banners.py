from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from models import Banner, BannerCreate, BannerUpdate, User
from auth_utils import get_current_admin_or_colaborador

router = APIRouter(prefix="/banners", tags=["Banners"])

async def get_db():
    """Dependency to get database instance"""
    from server import db
    return db

@router.get("/", response_model=List[Banner])
async def get_all_banners(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get all banners (public endpoint)"""
    banners = await db.banners.find({}, {"_id": 0}).sort("order", 1).to_list(1000)
    return banners

@router.get("/{banner_id}", response_model=Banner)
async def get_banner(banner_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get a specific banner by ID"""
    banner = await db.banners.find_one({"id": banner_id}, {"_id": 0})
    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found"
        )
    return banner

@router.post("/", response_model=Banner)
async def create_banner(
    banner_data: BannerCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Create a new banner (admin or colaborador)"""
    banner = Banner(**banner_data.model_dump())
    
    # Save to database
    banner_dict = banner.model_dump()
    banner_dict["created_at"] = banner_dict["created_at"].isoformat()
    
    await db.banners.insert_one(banner_dict)
    
    return banner

@router.put("/{banner_id}", response_model=Banner)
async def update_banner(
    banner_id: str,
    banner_update: BannerUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Update a banner (admin or colaborador)"""
    # Check if banner exists
    existing_banner = await db.banners.find_one({"id": banner_id}, {"_id": 0})
    if not existing_banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found"
        )
    
    # Update only provided fields
    update_data = {k: v for k, v in banner_update.model_dump().items() if v is not None}
    
    if update_data:
        await db.banners.update_one(
            {"id": banner_id},
            {"$set": update_data}
        )
    
    # Get updated banner
    updated_banner = await db.banners.find_one({"id": banner_id}, {"_id": 0})
    return Banner(**updated_banner)

@router.delete("/{banner_id}")
async def delete_banner(
    banner_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Delete a banner (admin or colaborador)"""
    result = await db.banners.delete_one({"id": banner_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found"
        )
    
    return {"message": "Banner deleted successfully"}