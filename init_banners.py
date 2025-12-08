import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

async def init_banners():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Check if banners already exist
    existing_banners = await db.banners.count_documents({})
    if existing_banners > 0:
        print(f"⚠️  Base de datos ya tiene {existing_banners} banners. No se crearon nuevos banners.")
        return
    
    banners = [
        {
            "id": str(uuid.uuid4()),
            "title": "Vive en Armonía con la Naturaleza",
            "description": "Descubre tu hogar ideal en el Norte Chico",
            "content": "Proyectos ecológicos con biohuertos y energía solar",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
            "order": 1,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Casa Huerto Ecológico",
            "description": "Tu propio oasis verde en Huacho",
            "content": "Lotes desde 500 m² con espacio para biohuerto",
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64",
            "order": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.banners.insert_many(banners)
    print(f"✓ {len(banners)} banners creados exitosamente")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_banners())