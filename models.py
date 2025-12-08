from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime, timezone
import uuid

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: Literal["admin", "user", "colaborador"] = "user"

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: Literal["admin", "user", "colaborador"] = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[Literal["admin", "user", "colaborador"]] = None

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    role: Literal["admin", "user", "colaborador"] = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class QuoteRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    nombre: str
    email: EmailStr
    telefono: str
    proyecto: str
    mensaje: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BlogCreate(BaseModel):
    title: str
    image: str
    excerpt: str
    content: str
    author: str

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None

class Blog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    image: str
    excerpt: str
    content: str
    author: str
    date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime('%d de %B, %Y'))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProjectCreate(BaseModel):
    title: str
    price: str
    address: str
    area: str
    description: str
    image: str
    status: Optional[str] = "Disponible"

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[str] = None
    address: Optional[str] = None
    area: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    status: Optional[str] = None

class Project(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    price: str
    address: str
    area: str
    description: str
    image: str
    status: str = "Disponible"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BannerCreate(BaseModel):
    title: str
    description: str
    content: str
    image: str
    order: Optional[int] = 0

class BannerUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    order: Optional[int] = None

class Banner(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    content: str
    image: str
    order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Refiere y Gana Models
class ReferralCreate(BaseModel):
    nombreReferidor: str
    telefonoReferidor: str
    correoReferidor: EmailStr
    nombreReferido: str
    telefonoReferido: str

class Referral(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombreReferidor: str
    telefonoReferidor: str
    correoReferidor: EmailStr
    nombreReferido: str
    telefonoReferido: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Vende tu terreno Models
class LandSaleCreate(BaseModel):
    nombre: str
    telefono: str
    correo: EmailStr
    ubicacion: str
    area: str
    precio: Optional[str] = None
    proyecto: Optional[str] = None
    detalles: Optional[str] = None

class LandSale(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    telefono: str
    correo: EmailStr
    ubicacion: str
    area: str
    precio: Optional[str] = None
    proyecto: Optional[str] = None
    detalles: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Eventos Models
class EventRegistrationCreate(BaseModel):
    nombre: str
    telefono: str
    correo: EmailStr
    personas: str
    evento_id: str
    evento_title: str

class EventRegistration(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    telefono: str
    correo: EmailStr
    personas: str
    evento_id: str
    evento_title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))