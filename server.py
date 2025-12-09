from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

# Endpoint temporal para inicializar la base de datos
@api_router.get("/init-database")
async def initialize_database():
    """
    Endpoint temporal para inicializar la base de datos con datos de prueba.
    """
    try:
        from init_all import init_all
        results = await init_all()
        return {
            "success": True,
            "message": "Base de datos inicializada correctamente",
            "detalles": {
                "usuarios_creados": results["usuarios"],
                "banners_creados": results["banners"],
                "blogs_creados": results["blogs"],
                "proyectos_creados": results["proyectos"],
                "errores": results["errores"]
            },
            "credenciales": {
                "admin": "admin@prados.com / admin123",
                "colaborador": "colaborador@prados.com / colab123",
                "usuario": "user@prados.com / user123"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "mensaje": "Error al inicializar la base de datos"
        }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Import authentication routes
from routes.auth import router as auth_router
from routes.quotes import router as quotes_router
from routes.blogs import router as blogs_router
from routes.users import router as users_router
from routes.projects import router as projects_router
from routes.banners import router as banners_router
from routes.referrals import router as referrals_router
from routes.land_sales import router as land_sales_router
from routes.event_registrations import router as event_registrations_router

# Include routers
api_router.include_router(auth_router)
api_router.include_router(quotes_router)
api_router.include_router(blogs_router)
api_router.include_router(users_router)
api_router.include_router(projects_router)
api_router.include_router(banners_router)
api_router.include_router(referrals_router, prefix="/referrals", tags=["referrals"])
api_router.include_router(land_sales_router, prefix="/land-sales", tags=["land-sales"])
api_router.include_router(event_registrations_router, prefix="/event-registrations", tags=["event-registrations"])

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
