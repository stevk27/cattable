from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from core.models import ShareInsurance 
from core.schemas.share_insuance_schemas import ShareInsuanceCreate 

def create_share_insurance(db: Session, share_insurance_data: ShareInsuanceCreate):
     
    db_share_insurance = ShareInsurance(
        company_id=share_insurance_data.company_id,
        number_of_share=share_insurance_data.number_of_share,
        type_action=share_insurance_data.type_action,
        unit_price=share_insurance_data.unit_price
    )
    db.add(db_share_insurance)
    db.commit()
    db.refresh(db_share_insurance)
    return db_share_insurance

def get_share_insurance_by_id(db: Session, share_insurance_id: uuid.UUID):
   
    return db.query(ShareInsurance).filter(ShareInsurance.id == share_insurance_id).first()

def get_all_share_insurances(db: Session, skip: int = 0, limit: int = 100):
   
    return db.query(ShareInsurance).offset(skip).limit(limit).all()

