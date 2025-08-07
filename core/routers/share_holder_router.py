import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.schemas.share_holders_schemas import ShareHolderBase,ShareHolderCreate,ShareHolderResponse,ShareHolderUpdate, ShareHolderWithLastParticipation 
from database import get_db
from core.services import share_holder_service
from core.models import ShareHolders, User
from utils.get_current_user import get_current_admin_user, get_current_user
from utils.jwt import verify_token 

#############################################################################################################################
router = APIRouter(
    prefix="/api/shareholders",
    tags=["shareholders"]
)


# @router.get("/", response_model=List[ShareHolderResponse])
# def read_all_share_holder(db: Session = Depends(get_db)):
#     share_holder = share_holder_service.get_share_holders(db=db)
#     return share_holder

@router.put("/{share_holders_id}", response_model=ShareHolderResponse)
def update_existing_share_holder(user_id: int, share_holders_update: ShareHolderUpdate, db: Session = Depends(get_db)):
    db_share_holder = share_holder_service.update_share_holder(db=db, user_id=user_id, share_holders_update=share_holders_update)
    if db_share_holder is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_share_holder

@router.delete("/{share_holders_id}", response_model=ShareHolderResponse)
def delete_existing_share_holder(share_holders_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_admin_user),):
    db_share_holder = share_holder_service.delete_share_holder(db=db, share_holders_id=share_holders_id)
    if db_share_holder is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_share_holder

@router.post("/", response_model=ShareHolderResponse)
def create_new_share_holder(share_holder: ShareHolderCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    print("current_user",current_user.id)
    share_holder = share_holder_service.create_shareholder_with_user(db=db,payload=share_holder,current_user=current_user)
    return share_holder

@router.get("/", response_model=List[ShareHolderWithLastParticipation])
def get_all_share_holders(db: Session = Depends(get_db),current_user: User = Depends(get_current_admin_user),):
    """
    Récupère tous les actionnaires avec leur dernière participation.
    """
    share_holders = share_holder_service.get_all_share_holders_with_last_participation(db=db)
    return share_holders

# Vous pouvez également créer un endpoint pour un seul actionnaire
@router.get("/{share_holder_id}", response_model=ShareHolderWithLastParticipation)
def get_share_holder(share_holder_id: uuid.UUID, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    """
    Récupère un actionnaire par son ID avec sa dernière participation.
    """
    share_holder = share_holder_service.get_share_holder_with_last_participation(db=db, shareholder_id=share_holder_id)
    if not share_holder:
        raise HTTPException(status_code=404, detail="Shareholder not found")
    return share_holder