from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from core.schemas.company_shemas import Company, CompanyCreate, CompanyUpdate
from core.services import company_service
from database import get_db

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)

@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_new_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle entreprise.
    """
    return company_service.create_company(db=db, company_data=company)

@router.get("/{company_id}", response_model=Company)
def read_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Récupère une entreprise par son ID.
    """
    company = company_service.get_company_by_id(db=db, company_id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/", response_model=List[Company])
def read_all_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère la liste de toutes les entreprises.
    """
    companies = company_service.get_all_companies(db=db, skip=skip, limit=limit)
    return companies

@router.put("/{company_id}", response_model=Company)
def update_existing_company(company_id: uuid.UUID, company_update: CompanyUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une entreprise existante.
    """
    db_company = company_service.update_company(db=db, company_id=company_id, company_update=company_update)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Supprime une entreprise.
    """
    db_company = company_service.delete_company(db=db, company_id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return None