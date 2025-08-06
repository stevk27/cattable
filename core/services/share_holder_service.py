import uuid
from fastapi import Depends
from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from typing import List
from core.models import Participation, ShareHolders, User
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

def create_shareholder_with_user(db: Session, payload: ShareHolderCreate, current_user: User):

    try:
        print("payload.user.email", payload.user.email)
        existing_user = db.query(User).filter_by(email=payload.user.email).first()
        print("existing_user", existing_user)
        if existing_user:
            raise HTTPException(status_code=400, detail="this email already exist.")
        
        # 1. Créer le User
        new_user = User(
            email=payload.user.email,
            password=hash_password(payload.user.password),
            status=payload.user.status
        )
        db.add(new_user)
        db.flush()  # permet de récupérer new_user.id

       
        # 2. Créer le ShareHolder lié au user
        new_shareholder = ShareHolders(
            last_name=payload.last_name,
            first_name=payload.first_name,
            phone_number=payload.phone_number,
            user_id=new_user.id,
            created_by_id=current_user.id
        )
        db.add(new_shareholder)

        db.commit()  # <-- n'oublie pas de valider manuellement

        return new_shareholder

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erreur d'intégrité (doublon email)")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


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

def get_share_holder_with_last_participation(db: Session, shareholder_id: uuid.UUID):
    """
    Récupère un actionnaire et charge sa dernière participation.
    """
    # 1. Récupère l'actionnaire
    share_holder = db.query(ShareHolders).filter(ShareHolders.id == shareholder_id).first()
    if not share_holder:
        return None

    # 2. Récupère la dernière participation de cet actionnaire
    # On utilise .order_by(desc(Participation.created_at)) pour s'assurer d'avoir la dernière
    last_participation = db.query(Participation)\
        .filter(Participation.share_holder_id == shareholder_id)\
        .order_by(desc(Participation.created_at))\
        .first()
    
    # 3. Ajoute la dernière participation à l'objet SQLAlchemy
    # Il est important de faire cela manuellement car SQLAlchemy ne sait pas
    # qu'il s'agit de la "dernière" participation par défaut.
    share_holder.last_participation = last_participation
    
    return share_holder

def get_all_share_holders_with_last_participation(db: Session) -> List[ShareHolders]:
    """
    Récupère tous les actionnaires et leur dernière participation.
    """
    # 1. Récupère tous les actionnaires
    share_holders = db.query(ShareHolders).options(joinedload(ShareHolders.user)).all()

    # 2. Crée un dictionnaire pour stocker les dernières participations
    last_participations = {}
    
    # 3. Récupère la dernière participation pour chaque actionnaire avec une seule requête
    # C'est une méthode avancée pour optimiser les requêtes
    if share_holders:
        share_holder_ids = [sh.id for sh in share_holders]
        
        # Sous-requête pour trouver la dernière participation de chaque actionnaire
        latest_participation_subquery = db.query(
            Participation.share_holder_id,
            func.max(Participation.created_at).label("max_created_at")
        ).filter(
            Participation.share_holder_id.in_(share_holder_ids)
        ).group_by(
            Participation.share_holder_id
        ).subquery()
        
        # Requête principale pour récupérer les participations complètes
        latest_participations = db.query(Participation)\
            .join(latest_participation_subquery,
                  (Participation.share_holder_id == latest_participation_subquery.c.share_holder_id) &
                  (Participation.created_at == latest_participation_subquery.c.max_created_at)
            )\
            .all()

        # Mappe les dernières participations aux actionnaires
        last_participations = {p.share_holder_id: p for p in latest_participations}

    # 4. Assigne la dernière participation à chaque actionnaire
    for share_holder in share_holders:
        share_holder.last_participation = last_participations.get(share_holder.id)

    return share_holders