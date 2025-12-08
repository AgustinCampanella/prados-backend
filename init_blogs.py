import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

async def init_blogs():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Check if blogs already exist
    existing_blogs = await db.blogs.count_documents({})
    if existing_blogs > 0:
        print(f"⚠️  Base de datos ya tiene {existing_blogs} blogs. No se crearon nuevos blogs.")
        return
    
    blogs = [
        {
            "id": str(uuid.uuid4()),
            "title": "Vivir en Armonía con la Naturaleza",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
            "excerpt": "Descubre cómo nuestros proyectos integran espacios verdes y sostenibilidad.",
            "content": "En Prados de Paraíso creemos que vivir en armonía con la naturaleza no es solo un sueño, sino una realidad alcanzable...",
            "author": "Equipo Prados",
            "date": "15 de Noviembre, 2024",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Casa Huerto: Tu Propio Oasis Verde",
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64",
            "excerpt": "Conoce nuestro proyecto estrella que combina vivienda y agricultura orgánica.",
            "content": "Casa Huerto Ecológico es más que un lugar para vivir, es un estilo de vida...",
            "author": "María González",
            "date": "10 de Noviembre, 2024",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.blogs.insert_many(blogs)
    print(f"✓ {len(blogs)} blogs creados exitosamente")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_blogs())