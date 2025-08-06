from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from core.schemas.participation_shemas import Participation
from core.schemas.share_holders_schemas import ShareHolderResponse
from core.services import participation_service
from database import get_db

router = APIRouter(
    prefix="/participations",
    tags=["participations"]
)


@router.post("/", response_model=Participation, status_code=status.HTTP_201_CREATED)
def create_new_participation(
    participation_data: Participation,
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle participation d'actionnaire dans une entreprise.
    """
    db_participation = participation_service.create_participation(
        db=db,
        participation_data=participation_data
    )
    return db_participation

@router.get("/{participation_id}", response_model=Participation)
def read_participation(
    participation_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Récupère une participation d'actionnaire par son ID.
    """
    participation = participation_service.get_participation_by_id(
        db=db,
        participation_id=participation_id
    )
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")
    return participation    

@router.get("/", response_model=List[Participation])
def read_all_participations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère une liste de toutes les participations d'actionnaires.
    """
    participations = participation_service.get_all_participations(
        db=db,
        skip=skip,
        limit=limit
    )
    return participations   