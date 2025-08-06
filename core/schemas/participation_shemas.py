from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

from core.schemas.share_holders_schemas import ShareHolderResponse

# Schéma pour la réponse de l'API, incluant l'actionnaire et l'entreprise
class Participation(BaseModel):
    id: uuid.UUID
    share_holder_id: uuid.UUID
    company_id: Optional[uuid.UUID] = None
    total_share: int
    percentage_on_capital: Optional[float] = None
    created_at: datetime
    
    # Relations (si vous souhaitez les imbriquer dans la réponse)
    share_holder: ShareHolderResponse
    # company: Company
    
    class Config:
        from_attributes = True