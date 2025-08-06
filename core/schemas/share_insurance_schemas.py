from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

from core.models import Company


class CompanyBase(BaseModel):
    company_name: str

class CompanyCreate(CompanyBase):
    adresse_id: Optional[uuid.UUID] = None
    share_insurance_ids: Optional[List[uuid.UUID]] = None

class CompanyResponse(CompanyBase):
    id: uuid.UUID
    adresse_id: Optional[uuid.UUID] = None
    share_insurance_ids: Optional[List[uuid.UUID]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ShareInsuranceBase(BaseModel):
    number_of_share: int = 0
    type_action: Optional[str] = None
    unit_price: float = 0.000

class ShareInsuranceCreate(ShareInsuranceBase):
    company_id: Optional[uuid.UUID] = None

# Schéma de réponse pour l'entité ShareInsurance
class ShareInsurance(ShareInsuranceBase):
    id: uuid.UUID
    company_id: Optional[uuid.UUID] = None
    created_at: datetime
    
    # Pour inclure les relations dans la réponse, décommentez et ajustez ces lignes
    company: Optional[CompanyResponse] = None
    # attribution: Optional[List[Attribution]] = None

    class Config:
        from_attributes = True