from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from models import QuoteRequest, User
from auth_utils import get_current_admin_or_colaborador

router = APIRouter(prefix="/quotes", tags=["Quotes"])

async def get_db():
    """Dependency to get database instance"""
    from server import db
    return db

@router.post("/", response_model=QuoteRequest)
async def create_quote(
    quote: QuoteRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new quote request (public endpoint)"""
    quote_dict = quote.model_dump()
    quote_dict["created_at"] = quote_dict["created_at"].isoformat()
    
    await db.quotes.insert_one(quote_dict)
    return quote

@router.get("/", response_model=List[QuoteRequest])
async def get_all_quotes(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Get all quote requests (admin and colaborador only)"""
    quotes = await db.quotes.find({}, {"_id": 0}).to_list(1000)
    return quotes

@router.delete("/{quote_id}")
async def delete_quote(
    quote_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Delete a quote request (admin and colaborador only)"""
    result = await db.quotes.delete_one({"id": quote_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    return {"message": "Quote deleted successfully"}