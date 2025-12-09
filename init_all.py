"""
Script de inicializacion completa de la base de datos
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth_utils import hash_password
from datetime import datetime, timezone
import uuid
import os

async def init_all():
    """Inicializa toda la base de datos con datos de prueba"""
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME', 'prados_paraiso')]
    
    results = {
        "usuarios": 0,
        "banners": 0,
        "blogs": 0,
        "proyectos": 0,
        "errores": []
    }
    
    # USUARIOS
    try:
        existing_users = await db.users.count_documents({})
        if existing_users == 0:
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
            results["usuarios"] = len(users)
    except Exception as e:
        results["errores"].append(f"Error usuarios: {str(e)}")
    
    # BANNERS
    try:
        existing_banners = await db.banners.count_documents({})
        if existing_banners == 0:
            banners = [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Vive en Armonia con la Naturaleza",
                    "description": "Descubre tu hogar ideal en el Norte Chico",
                    "content": "Proyectos ecologicos con biohuertos y energia solar",
                    "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
                    "order": 1,
                    "created_at": datetime.now(timezone.utc).isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Casa Huerto Ecologico",
                    "description": "Tu propio oasis verde en Huacho",
                    "content": "Lotes desde 500 m2 con espacio para biohuerto",
                    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64",
                    "order": 2,
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
            ]
            await db.banners.insert_many(banners)
            results["banners"] = len(banners)
    except Exception as e:
        results["errores"].append(f"Error banners: {str(e)}")
    
    # BLOGS
    try:
        existing_blogs = await db.blogs.count_documents({})
        if existing_blogs == 0:
            blogs = [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Vivir en Armonia con la Naturaleza",
                    "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
                    "excerpt": "Descubre como nuestros proyectos integran espacios verdes y sostenibilidad.",
                    "content": "En Prados de Paraiso creemos que vivir en armonia con la naturaleza no es solo un sueno, sino una realidad alcanzable...",
                    "author": "Equipo Prados",
                    "date": "15 de Noviembre, 2024",
                    "created_at": datetime.now(timezone.utc).isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Casa Huerto: Tu Propio Oasis Verde",
                    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64",
                    "excerpt": "Conoce nuestro proyecto estrella que combina vivienda y agricultura organica.",
                    "content": "Casa Huerto Ecologico es mas que un lugar para vivir, es un estilo de vida...",
                    "author": "Maria Gonzalez",
                    "date": "10 de Noviembre, 2024",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
            ]
            await db.blogs.insert_many(blogs)
            results["blogs"] = len(blogs)
    except Exception as e:
        results["errores"].append(f"Error blogs: {str(e)}")
    
    # PROYECTOS
    try:
        existing_projects = await db.projects.count_documents({})
        if existing_projects == 0:
            projects = [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Casa Huerto Ecologico",
                    "price": "$800 USD / m2",
                    "address": "Huacho, Norte Chico",
                    "area": "Desde 500 m2",
                    "description": "Lotes con espacio para biohuerto propio y casa ecologica",
                    "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
                    "status": "Disponible",
                    "created_at": datetime.now(timezone.utc).isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Villa Eco-Sostenible",
                    "price": "$950 USD / m2",
                    "address": "El Paraiso, Norte Chico",
                    "area": "Desde 400 m2",
                    "description": "Lotes frente a humedales con vista a la playa",
                    "image": "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde",
                    "status": "Disponible",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
            ]
            await db.projects.insert_many(projects)
            results["proyectos"] = len(projects)
    except Exception as e:
        results["errores"].append(f"Error proyectos: {str(e)}")
    
    client.close()
    return results

if __name__ == "__main__":
    result = asyncio.run(init_all())
    print(f"Usuarios: {result['usuarios']}")
    print(f"Banners: {result['banners']}")
    print(f"Blogs: {result['blogs']}")
    print(f"Proyectos: {result['proyectos']}")
