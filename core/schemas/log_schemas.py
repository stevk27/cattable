from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Import du schéma utilisateur pour la relation
from core.schemas.user_schemas import User

class AuditEvent(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    action: str
    details: Optional[str] = None
    created_at: datetime
    
    user: User # Pour afficher les informations de l'utilisateur
    
    class Config:
        from_attributes = True