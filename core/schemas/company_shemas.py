from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

# Importez les schémas des relations
from core.schemas.adresse_schemas import Adresse
from core.schemas.share_insuance_schemas import ShareInsurance
from core.schemas.participation_shemas import Participation

class CompanyBase(BaseModel):
    company_name: str
    adresse_id: Optional[uuid.UUID] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Relations (pour les réponses enrichies)
    adresse: Optional[Adresse] = None
    share_insurance: Optional[List[ShareInsurance]] = None
    participation: Optional[List[Participation]] = None

    class Config:
        from_attributes = True