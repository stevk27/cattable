from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

from .models import User 
from enurations import UserRole

# Schéma de base pour les attributs communs de l'utilisateur
class UserBase(BaseModel):
    email: EmailStr
    status: UserRole = UserRole.USER

# Schéma pour la création d'un utilisateur
# Inclut le mot de passe qui est requis pour l'enregistrement
class UserCreate(UserBase):
    password: str

# Schéma pour la mise à jour d'un utilisateur
# Tous les champs sont optionnels pour permettre des mises à jour partielles
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: Optional[UserRole] = None

# Schéma pour la réponse de l'API (ce qui est renvoyé au client)
# Il ne contient pas le mot de passe haché
class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    # Configuration pour SQLAlchemy
    # Permet de convertir un objet SQLAlchemy en un objet Pydantic
    class Config:
        from_attributes = True



