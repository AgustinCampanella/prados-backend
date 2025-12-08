import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth_utils import hash_password
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

async def init_users():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Check if users already exist
    existing_users = await db.users.count_documents({})
    if existing_users > 0:
        print(f"⚠️  Base de datos ya tiene {existing_users} usuarios. No se crearon nuevos usuarios.")
        return
    
    users = [
        {
            "id": str(uuid.uuid4()),
            "email": "admin@prados.com",
            "name": "Administrador",
            "role": "admin",
            "hashed_password": hash_password("admin123"),
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "email": "colaborador@prados.com",
            "name": "Colaborador",
            "role": "colaborador",
            "hashed_password": hash_password("colab123"),
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "email": "user@prados.com",
            "name": "Usuario Demo",
            "role": "user",
            "hashed_password": hash_password("user123"),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.users.insert_many(users)
    print(f"✓ {len(users)} usuarios creados exitosamente")
    print("  - admin@prados.com / admin123")
    print("  - colaborador@prados.com / colab123")
    print("  - user@prados.com / user123")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_users())