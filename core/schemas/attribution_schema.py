from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Importez les schémas des entités liées
from core.schemas.share_insuance_schemas import ShareInsurance
from core.schemas.share_holders_schemas import  ShareHolderResponse
from core.schemas.file_schemas import File

class AttributionBase(BaseModel):
    number_of_share: int = 0
    attribution_date: datetime

class AttributionCreate(AttributionBase):
    share_insurance_id: uuid.UUID
    share_holder_id: uuid.UUID

class AttributionMinimal(BaseModel):
    id: uuid.UUID
    created_at: datetime


    emission_certificate_file: Optional[File] = None
    share_insurance: ShareInsurance
    share_holder: ShareHolderResponse
    class Config:
        orm_mode = True
    

# Schéma de réponse qui peut inclure les relations
class AttributionResponse(AttributionBase):
    id: uuid.UUID
    share_insurance_id: uuid.UUID
    share_holder_id: uuid.UUID
    emission_certificate_file_id: Optional[uuid.UUID] = None
    created_at: datetime
    
    # Relations imbriquées pour une réponse enrichie
    share_insurance: ShareInsurance
    share_holder: ShareHolderResponse
    emission_certificate_file: Optional[File] = None

    class Config:
        from_attributes = True