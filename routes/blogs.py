from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from models import Blog, BlogCreate, BlogUpdate, User
from auth_utils import get_current_admin_or_colaborador

router = APIRouter(prefix="/blogs", tags=["Blogs"])

async def get_db():
    """Dependency to get database instance"""
    from server import db
    return db

@router.get("/", response_model=List[Blog])
async def get_all_blogs(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get all blog posts"""
    blogs = await db.blogs.find({}, {"_id": 0}).to_list(1000)
    return blogs

@router.get("/{blog_id}", response_model=Blog)
async def get_blog(blog_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get a specific blog post"""
    blog = await db.blogs.find_one({"id": blog_id}, {"_id": 0})
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )
    return Blog(**blog)

@router.post("/", response_model=Blog)
async def create_blog(
    blog_data: BlogCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Create a new blog post (admin and colaborador only)"""
    blog = Blog(**blog_data.model_dump())
    blog_dict = blog.model_dump()
    blog_dict["created_at"] = blog_dict["created_at"].isoformat()
    
    await db.blogs.insert_one(blog_dict)
    return blog

@router.put("/{blog_id}", response_model=Blog)
async def update_blog(
    blog_id: str,
    blog_update: BlogUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Update a blog post (admin and colaborador only)"""
    existing_blog = await db.blogs.find_one({"id": blog_id}, {"_id": 0})
    if not existing_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )
    
    update_data = {k: v for k, v in blog_update.model_dump().items() if v is not None}
    
    if update_data:
        await db.blogs.update_one(
            {"id": blog_id},
            {"$set": update_data}
        )
    
    updated_blog = await db.blogs.find_one({"id": blog_id}, {"_id": 0})
    return Blog(**updated_blog)

@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Delete a blog post (admin and colaborador only)"""
    result = await db.blogs.delete_one({"id": blog_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )
    
    return {"message": "Blog deleted successfully"}