from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

# Import des modèles SQLAlchemy
from core.models import Participation,ShareHolders,Company,Attribution, ShareInsurance

from sqlalchemy import func

def update_or_create_participation(
    db: Session,
    share_holder_id: uuid.UUID,
    company_id: uuid.UUID,
    new_shares: int
):
    """
    Met à jour la participation d'un actionnaire ou la crée si elle n'existe pas.
    """
    # 1. Tente de trouver une participation existante pour cet actionnaire et cette entreprise
    db_participation = db.query(Participation).filter(
        Participation.share_holder_id == share_holder_id,
        Participation.company_id == company_id
    ).first()
    
    # 2. Si une participation existe, mettez-la à jour
    if db_participation:
        db_participation.total_share += new_shares
        
        # Mettez à jour le pourcentage sur le capital (nécessite le capital total de l'entreprise)
        company = db.query(Company).filter(Company.id == company_id).first()
        if company :
            insuance =  db.query(ShareInsurance).filter(Company.id == company_id).order_by(ShareInsurance.created_at.desc()).first()
            if insuance.number_of_share > 0:
                db_participation.percentage_on_capital = (db_participation.total_share / insuance.number_of_share) * 100

    # 3. Si aucune participation n'existe, créez-en une nouvelle
    else:
        # Calculez le pourcentage sur le capital si l'entreprise existe
        percentage = None
        company = db.query(Company).filter(Company.id == company_id).first()
        if company :
            insuance =  db.query(ShareInsurance).filter(Company.id == company_id).order_by(ShareInsurance.created_at.desc()).first()
            if insuance.number_of_share > 0:
                percentage = (new_shares / insuance.number_of_share) * 100
            
        db_participation = Participation(
            share_holder_id=share_holder_id,
            company_id=company_id,
            total_share=new_shares,
            percentage_on_capital=percentage
        )
        db.add(db_participation)
    
    db.commit()
    db.refresh(db_participation)
    return db_participation

def get_participation_by_share_holder_and_company(
    db: Session,
    share_holder_id: uuid.UUID,
) -> Optional[Participation]:
    """
    Récupère la participation d'un actionnaire pour une entreprise donnée.
    """
    return db.query(Participation).filter(
        Participation.share_holder_id == share_holder_id,
    ).first()   

def get_participation_by_id(
    db: Session,
    participation_id: uuid.UUID
) -> Optional[Participation]:
    """
    Récupère une participation par son ID.
    """
    return db.query(Participation).filter(Participation.id == participation_id).first()
def get_all_participations(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Participation]:
    """
    Récupère une liste de toutes les participations d'actionnaires.
    """
    return db.query(Participation).offset(skip).limit(limit).all()
def create_participation(
    db: Session,
    participation_data: Participation
) -> Participation:
    """
    Crée une nouvelle participation d'actionnaire dans une entreprise.
    """
    # Vérification de l'existence de l'actionnaire et de l'entreprise
    share_holder = db.query(ShareHolders).filter(ShareHolders.id == participation_data.share_holder_id).first()
    company = db.query(Company).filter(Company.id == participation_data.company_id).first()
    
    if not share_holder or not company:
        raise ValueError("Share holder or company does not exist.")
    
    # Mise à jour ou création de la participation
    return update_or_create_participation(
        db=db,
        share_holder_id=participation_data.share_holder_id,
        company_id=participation_data.company_id,
        new_shares=participation_data.total_share
    )   