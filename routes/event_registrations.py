from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import os

from models import EventRegistration, EventRegistrationCreate, User
from auth_utils import get_current_admin_user, get_current_admin_or_colaborador

router = APIRouter()

def get_db():
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME', 'prados_paraiso')]
    return db

@router.post("/", response_model=EventRegistration)
async def create_event_registration(registration: EventRegistrationCreate):
    """Create a new event registration"""
    db = get_db()
    
    registration_data = EventRegistration(**registration.dict())
    registration_dict = registration_data.dict()
    
    # Convert datetime to ISO string for MongoDB
    registration_dict['created_at'] = registration_dict['created_at'].isoformat()
    
    await db.event_registrations.insert_one(registration_dict)
    
    return registration_data

@router.get("/", response_model=List[EventRegistration])
async def get_all_event_registrations(current_user: User = Depends(get_current_admin_or_colaborador)):
    """Get all event registrations - Admin and Colaborador only"""
    db = get_db()
    
    registrations = await db.event_registrations.find({}, {"_id": 0}).to_list(1000)
    return registrations

@router.get("/event/{evento_id}", response_model=List[EventRegistration])
async def get_registrations_by_event(evento_id: str, current_user: User = Depends(get_current_admin_or_colaborador)):
    """Get all registrations for a specific event - Admin and Colaborador only"""
    db = get_db()
    
    registrations = await db.event_registrations.find({"evento_id": evento_id}, {"_id": 0}).to_list(1000)
    return registrations

@router.delete("/{registration_id}")
async def delete_event_registration(registration_id: str, current_user: User = Depends(get_current_admin_user)):
    """Delete an event registration - Admin only"""
    db = get_db()
    
    result = await db.event_registrations.delete_one({"id": registration_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event registration not found")
    
    return {"message": "Event registration deleted successfully"}