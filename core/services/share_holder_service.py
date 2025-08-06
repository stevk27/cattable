import uuid
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from core.models import ShareHolders, User
from core.schemas.share_holders_schemas import ShareHolderCreate
from utils import get_current_user
from utils.security import hash_password
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
##################################################################################################
def get_share_holder(db: Session, share_holder_id: int):
    """
    Récupère un utilisateur par son ID.
    """
    return db.query(ShareHolders).filter(ShareHolders.id == share_holder_id).first()

def get_share_holders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ShareHolders).offset(skip).limit(limit).all()


def create_share_holder(db: Session, share_holder: ShareHolderCreate,current_user: User = Depends(get_current_user)):
    """
    Crée un nouvel utilisateur dans la base de données.
    """
    db_share_holder = ShareHolders(
        **share_holder.dict(),
        created_by_id=current_user.id
    )
    db.add(db_share_holder)
    db.commit()
    db.refresh(db_share_holder)
    return db_share_holder

def create_shareholder_with_user(db: Session, payload: ShareHolderCreate,current_user: User = Depends(get_current_user)):
    try:
        existing_user = db.query(User).filter_by(email=payload.user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="this email already exist.")
        
        with db.begin():  
            # 1. Créer le User
            new_user = User(
                id=uuid.uuid4(),
                email=payload.user.email,
                password=  hash_password(payload.user.password),  
                status="shareholder"
            )
            db.add(new_user)
            db.flush()  # pour récupérer new_user.id

            # 2. Créer le ShareHolder lié au user
            new_shareholder = ShareHolders(
                id=uuid.uuid4(),
                last_name=payload.last_name,
                first_name=payload.first_name,
                phone_number=payload.phone_number,
                user_id=new_user.id,
                created_by_id=payload.created_by_id
            )
            db.add(new_shareholder)

        return new_shareholder
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erreur d'intégrité (doublon email)")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la création")


def update_share_holder(db: Session, share_holder_id: int, share_holder_update: ShareHolderCreate):
    """
    Met à jour un utilisateur existant.
    """
    db_share_holder = db.query(ShareHolders).filter(ShareHolders.id == share_holder_id).first()
    if not db_share_holder:
        return None
    
    # Met à jour les attributs de l'utilisateur avec les valeurs non nulles
    update_data = share_holder_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_share_holder, key, value)
    
    db.add(db_share_holder)
    db.commit()
    db.refresh(db_share_holder)
    return db_share_holder

def delete_share_holder(db: Session, share_holder_id: int):
    """
    Supprime un utilisateur par son ID.
    """
    db_share_holder = db.query(ShareHolders).filter(ShareHolders.id == share_holder_id).first()
    if not db_share_holder:
        return None
    
    db.delete(db_share_holder)
    db.commit()
    return db_share_holder