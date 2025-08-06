from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from core.models import Company
from core.schemas.company_shemas import CompanyCreate, CompanyUpdate

def create_company(db: Session, company_data: CompanyCreate):
    
    db_company = Company(
        company_name=company_data.company_name,
        adresse_id=company_data.adresse_id
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_company_by_id(db: Session, company_id: uuid.UUID):

    return db.query(Company).filter(Company.id == company_id).first()

def get_all_companies(db: Session, skip: int = 0, limit: int = 100):
   
    return db.query(Company).offset(skip).limit(limit).all()

def update_company(db: Session, company_id: uuid.UUID, company_update: CompanyUpdate):
    
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        return None
    
    update_data = company_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_company, key, value)
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: uuid.UUID):
    
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        return None
        
    db.delete(db_company)
    db.commit()
    return db_company