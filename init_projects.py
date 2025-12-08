import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

async def init_projects():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Check if projects already exist
    existing_projects = await db.projects.count_documents({})
    if existing_projects > 0:
        print(f"⚠️  Base de datos ya tiene {existing_projects} proyectos. No se crearon nuevos proyectos.")
        return
    
    projects = [
        {
            "id": str(uuid.uuid4()),
            "title": "Casa Huerto Ecológico",
            "price": "$800 USD / m²",
            "address": "Huacho, Norte Chico",
            "area": "Desde 500 m²",
            "description": "Lotes con espacio para biohuerto propio y casa ecológica",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
            "status": "Disponible",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Villa Eco-Sostenible",
            "price": "$950 USD / m²",
            "address": "El Paraíso, Norte Chico",
            "area": "Desde 400 m²",
            "description": "Lotes frente a humedales con vista a la playa",
            "image": "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde",
            "status": "Disponible",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.projects.insert_many(projects)
    print(f"✓ {len(projects)} proyectos creados exitosamente")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_projects())