from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

# Import des schémas et services
from core.schemas.attribution_schema import AttributionMinimal, AttributionResponse, AttributionCreate
from core.services import attribution_service
from  database import get_db
from core.models import User
from utils.get_current_user import get_current_admin_user, get_current_user
from utils.jwt import verify_token

router = APIRouter(
    prefix="/api/insuance",
    tags=["attributions"]
)

@router.post("/", response_model=AttributionResponse, status_code=status.HTTP_201_CREATED)
def create_new_attribution(
    attribution_data: AttributionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):

    try:
        db_attribution = attribution_service.create_attribution(
            db=db,
            attribution_data=attribution_data
        )
        return db_attribution
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur interne est survenue: {e}")

@router.get("/{attribution_id}", response_model=AttributionResponse)
def get_attribution(
    attribution_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Récupère une attribution par son ID.
    """
    attribution = attribution_service.get_attribution_by_id(
        db=db,
        attribution_id=attribution_id
    )
    if not attribution:
        raise HTTPException(status_code=404, detail="Attribution non trouvée")
    return attribution

@router.get("/{attribution_id}/certificate", response_model=str)
def get_certificate(
    attribution_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Récupère le fichier de certificat d'émission associé à une attribution.
    """
    certificate_file = attribution_service.get_certificate_file_by_attribution_id(
        db=db,
        attribution_id=attribution_id
    )
    if not certificate_file:
        raise HTTPException(status_code=404, detail="Certificat non trouvé")
    return certificate_file 

@router.get("/", response_model=List[AttributionMinimal])
def read_all_attributions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Récupère la liste des attributions pour l'utilisateur connecté.
    """
    all_attributions = attribution_service.get_all_attributions(
        db=db,
        user=current_user, # On passe l'utilisateur au service
        skip=skip,
        limit=limit
    )
    return all_attributions