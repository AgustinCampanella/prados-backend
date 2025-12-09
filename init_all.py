¡Ese error significa que el endpoint `/api/init-database` **no existe** en el código que está en Render!

---

## 🔍 EL PROBLEMA

El código en **GitHub** no tiene el endpoint de inicialización que agregamos. Render despliega desde GitHub, así que necesitamos actualizar el repositorio.

---

## ✅ SOLUCIÓN: ACTUALIZAR GITHUB

### PASO 1: Agregar el endpoint a GitHub

1. **Ve a tu repositorio:** https://github.com/AgustinCampanella/prados-backend

2. **Abre el archivo `server.py`**

3. **Click en el ícono de lápiz (editar)**

4. **Busca estas líneas:**
   ```python
   @api_router.get("/")
   async def root():
       return {"message": "Hello World"}
   ```

5. **JUSTO DESPUÉS, agrega este código:**

```python

# Endpoint temporal para inicializar la base de datos
@api_router.get("/init-database")
async def initialize_database():
    """
    Endpoint temporal para inicializar la base de datos con datos de prueba.
    Visita: https://tu-dominio.com/api/init-database
    IMPORTANTE: Elimina este endpoint después de usarlo por seguridad.
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
            },
            "nota": "ELIMINA ESTE ENDPOINT después de usarlo por seguridad"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "mensaje": "Error al inicializar la base de datos"
        }
```

6. **Scroll hacia abajo y click en "Commit changes"**
7. **Agrega un mensaje:** "Add init-database endpoint"
8. **Click en "Commit changes"** (botón verde)

---

### PASO 2: Verificar que `init_all.py` existe en GitHub

1. **En el repositorio, verifica si existe el archivo `init_all.py`**
2. **Si NO existe, créalo:**
   - Click en "Add file" → "Create new file"
   - Nombre: `init_all.py`
   - Contenido: (te lo paso abajo)

---

## 📄 CONTENIDO DE `init_all.py` (si no existe)
Action: file_editor view /app/backend/init_all.py
Observation: /app/backend/init_all.py:
1|"""
2|Script de inicialización completa de la base de datos
3|Ejecuta todos los scripts init_* en orden
4|"""
5|import asyncio
6|from motor.motor_asyncio import AsyncIOMotorClient
7|from auth_utils import hash_password
8|from datetime import datetime, timezone
9|import uuid
10|import os
11|from dotenv import load_dotenv
12|
13|load_dotenv()
14|
15|async def init_all():
16|    """Inicializa toda la base de datos con datos de prueba"""
17|    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
18|    db = client[os.environ['DB_NAME']]
19|    
20|    results = {
21|        "usuarios": 0,
22|        "banners": 0,
23|        "blogs": 0,
24|        "proyectos": 0,
25|        "errores": []
26|    }
27|    
28|    # ===== USUARIOS =====
29|    try:
30|        existing_users = await db.users.count_documents({})
31|        if existing_users == 0:
32|            users = [
33|                {
34|                    "id": str(uuid.uuid4()),
35|                    "email": "admin@prados.com",
36|                    "name": "Administrador",
37|                    "role": "admin",
38|                    "hashed_password": hash_password("admin123"),
39|                    "created_at": datetime.now(timezone.utc).isoformat()
40|                },
41|                {
42|                    "id": str(uuid.uuid4()),
43|                    "email": "colaborador@prados.com",
44|                    "name": "Colaborador",
45|                    "role": "colaborador",
46|                    "hashed_password": hash_password("colab123"),
47|                    "created_at": datetime.now(timezone.utc).isoformat()
48|                },
49|                {
50|                    "id": str(uuid.uuid4()),
