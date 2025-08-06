from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from core.models import ShareInsurance 
from core.schemas.share_insuance_schemas import ShareInsuanceCreate,ShareInsurance,ShareInsuanceBase

from core.services import share_insurance_service
from  database import get_db
from utils.jwt import verify_token

router = APIRouter(
    prefix="/api/share-insuances",
    tags=["insuances"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_token)]
)

@router.post("/", response_model=ShareInsurance, status_code=status.HTTP_201_CREATED)
def create_new_share_insuance(
    share_insurance: ShareInsuanceCreate,
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel enregistrement d'assurance d'action.
    """
    # Ici, vous pourriez ajouter une validation supplémentaire avant de créer
    # par exemple, vérifier si l'entreprise existe (avec company_id)
    db_share_insurance = share_insurance_service.create_share_insurance(
        db=db,
        share_insurance_data=share_insurance
    )
    return db_share_insurance

@router.get("/{share_insurance_id}", response_model=ShareInsurance)
def read_share_insurance(
    share_insurance_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Récupère un enregistrement d'assurance d'action par son ID.
    """
    share_insurance = share_insurance_service.get_share_insurance_by_id(
        db=db,
        share_insurance_id=share_insurance_id
    )
    if share_insurance is None:
        raise HTTPException(status_code=404, detail="Share insurance not found")
    return share_insurance

@router.get("/", response_model=List[ShareInsurance])
def read_all_share_insurances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère une liste de tous les enregistrements d'assurance d'action.
    """
    all_insurances = share_insurance_service.get_all_share_insurances(
        db=db,
        skip=skip,
        limit=limit
    )
    return all_insurances