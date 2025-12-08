from fastapi import APIRouter, HTTPException, Depends, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from models import Project, ProjectCreate, ProjectUpdate, User
from auth_utils import get_current_admin_or_colaborador
import re

router = APIRouter(prefix="/projects", tags=["Projects"])

async def get_db():
    """Dependency to get database instance"""
    from server import db
    return db

@router.get("/search/", response_model=List[Project])
async def search_projects(
    ubicacion: Optional[str] = Query(None, description="Filter by location"),
    precio: Optional[str] = Query(None, description="Filter by price range"),
    orden: Optional[str] = Query(None, description="Sort order"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Search and filter projects with optional parameters
    - ubicacion: 'todas', 'casa-huerto', 'villa-eco', 'huacho', 'el-paraiso'
    - precio: 'todos', '0-500', '500-1000', '1000-plus'
    - orden: 'alfabetico-az', 'alfabetico-za', 'precio-menor', 'precio-mayor', 'reciente'
    """
    # Build filter query
    filter_query = {}
    
    # Location filter
    if ubicacion and ubicacion != 'todas':
        location_map = {
            'casa-huerto': r'Casa Huerto',
            'villa-eco': r'Villa Eco',
            'huacho': r'Huacho',
            'el-paraiso': r'Paraíso'
        }
        if ubicacion in location_map:
            filter_query['$or'] = [
                {'title': {'$regex': location_map[ubicacion], '$options': 'i'}},
                {'address': {'$regex': location_map[ubicacion], '$options': 'i'}},
                {'description': {'$regex': location_map[ubicacion], '$options': 'i'}}
            ]
    
    # Get projects
    projects = await db.projects.find(filter_query, {"_id": 0}).to_list(1000)
    
    # Price filter (applied in Python since MongoDB doesn't store numeric prices)
    if precio and precio != 'todos':
        filtered_projects = []
        for project in projects:
            price_str = project.get('price', '')
            # Extract numeric value from price string
            numbers = re.findall(r'\d+', price_str.replace(',', ''))
            if numbers:
                price_value = int(numbers[0])
                
                if precio == '0-500' and price_value <= 500:
                    filtered_projects.append(project)
                elif precio == '500-1000' and 500 < price_value <= 1000:
                    filtered_projects.append(project)
                elif precio == '1000-plus' and price_value > 1000:
                    filtered_projects.append(project)
        projects = filtered_projects
    
    # Sorting
    if orden:
        if orden == 'alfabetico-az':
            projects = sorted(projects, key=lambda x: x.get('title', '').lower())
        elif orden == 'alfabetico-za':
            projects = sorted(projects, key=lambda x: x.get('title', '').lower(), reverse=True)
        elif orden == 'precio-menor':
            def get_price_value(project):
                price_str = project.get('price', '')
                numbers = re.findall(r'\d+', price_str.replace(',', ''))
                return int(numbers[0]) if numbers else 0
            projects = sorted(projects, key=get_price_value)
        elif orden == 'precio-mayor':
            def get_price_value(project):
                price_str = project.get('price', '')
                numbers = re.findall(r'\d+', price_str.replace(',', ''))
                return int(numbers[0]) if numbers else 0
            projects = sorted(projects, key=get_price_value, reverse=True)
        elif orden == 'reciente':
            projects = sorted(projects, key=lambda x: x.get('created_at', ''), reverse=True)
    
    return projects

@router.get("/", response_model=List[Project])
async def get_all_projects(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get all projects (public endpoint)"""
    projects = await db.projects.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    return projects

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get a specific project by ID"""
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.post("/", response_model=Project)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Create a new project (admin or colaborador)"""
    project = Project(**project_data.model_dump())
    
    # Save to database
    project_dict = project.model_dump()
    project_dict["created_at"] = project_dict["created_at"].isoformat()
    
    await db.projects.insert_one(project_dict)
    
    return project

@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Update a project (admin or colaborador)"""
    # Check if project exists
    existing_project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update only provided fields
    update_data = {k: v for k, v in project_update.model_dump().items() if v is not None}
    
    if update_data:
        await db.projects.update_one(
            {"id": project_id},
            {"$set": update_data}
        )
    
    # Get updated project
    updated_project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    return Project(**updated_project)

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_colaborador)
):
    """Delete a project (admin or colaborador)"""
    result = await db.projects.delete_one({"id": project_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {"message": "Project deleted successfully"}