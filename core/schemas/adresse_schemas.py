from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Schéma pour la création ou la mise à jour d'une adresse
# Tous les champs sont optionnels car l'adresse peut être créée de manière partielle
class AdresseBase(BaseModel):
    longitude: Optional[float] = None
    latitude: Optional[float] = None # J'ai corrigé "longitude" en "latitude"
    city: Optional[str] = None
    country: Optional[str] = None
    bp: Optional[str] = None
    phone_number: Optional[str] = None

# Schéma pour la réponse de l'API
# Inclut les champs générés par la base de données
class Adresse(AdresseBase):
    id: uuid.UUID
    created_at: datetime
    
    # Configuration pour la compatibilité avec SQLAlchemy
    class Config:
        from_attributes = True