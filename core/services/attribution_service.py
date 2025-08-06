from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
import os
import io

# Import des modèles SQLAlchemy
from core.models import Attribution,ShareInsurance,ShareHolders,File,User
from core.enurations import UserRole
from core.services.participation_service import update_or_create_participation

# Import des schémas Pydantic
from core.schemas.attribution_schema import AttributionCreate

# Import de la bibliothèque pour la génération de PDF
from fpdf import FPDF
###############################################################################################################
# Définissez le dossier de stockage pour les fichiers
STORAGE_DIR = "storage/certificats_emission"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def generate_and_save_pdf(attribution: Attribution, db: Session):
    """
    Génère un certificat d'émission au format PDF et l'enregistre.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Contenu du PDF
    pdf.cell(200, 10, txt="Certificat d'Émission d'Actions", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Numéro d'attribution : {attribution.id}", ln=2, align="L")
    pdf.cell(200, 10, txt=f"Actionnaire : {attribution.share_holder.first_name} {attribution.share_holder.last_name}", ln=2, align="L")
    pdf.cell(200, 10, txt=f"Nombre d'actions : {attribution.number_of_share}", ln=2, align="L")
    
    # Nom du fichier et chemin de stockage
    file_name = f"certificat_attribution_{attribution.id}.pdf"
    file_path = os.path.join(STORAGE_DIR, file_name)
    
    # Sauvegarde du fichier
    pdf.output(file_path)
    
    # Création d'un enregistrement dans la base de données pour le fichier
    db_file = File(
        file_name=file_name,
        storage_path=file_path,
        type_of_file="application/pdf"
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return db_file

def create_attribution(db: Session, attribution_data: AttributionCreate):
    """
    Crée une nouvelle attribution après avoir vérifié la disponibilité des actions.
    """
    # 1. Vérification de l'existence de l'assurance d'action et de l'actionnaire
    share_insurance = db.query(ShareInsurance).filter(ShareInsurance.id == attribution_data.share_insurance_id).first()
    if not share_insurance:
        raise ValueError("L'assurance d'action n'existe pas.")

    share_holder = db.query(ShareHolders).filter(ShareHolders.id == attribution_data.share_holder_id).first()
    if not share_holder:
        raise ValueError("L'actionnaire n'existe pas.")

    # 2. Logique de vérification du nombre d'actions
    
    # Calcule le nombre d'actions déjà attribuées pour cette assurance d'action
    total_attributed_shares = db.query(
        func.sum(Attribution.number_of_share)
    ).filter(
        Attribution.share_insurance_id == attribution_data.share_insurance_id
    ).scalar() or 0 # 'or 0' gère le cas où aucune attribution n'existe encore
    
    # Vérifie si la nouvelle attribution dépasse la limite
    if (total_attributed_shares + attribution_data.number_of_share) > share_insurance.number_of_share:
        raise ValueError("Le nombre total d'actions attribuées dépasse le nombre total disponible.")

    # 3. Création de l'objet Attribution SQLAlchemy
    db_attribution = Attribution(
        share_insurance_id=attribution_data.share_insurance_id,
        share_holder_id=attribution_data.share_holder_id,
        number_of_share=attribution_data.number_of_share,
        attribution_date=attribution_data.attribution_date
    )
    
    db.add(db_attribution)
    db.commit()
    db.refresh(db_attribution)


    #update the participation of the share holder
    company_id = db.query(ShareInsurance.company_id).filter(
            ShareInsurance.id == attribution_data.share_insurance_id
        ).scalar()
        
    update_or_create_participation(
        db=db,
        share_holder_id=attribution_data.share_holder_id,
        company_id=company_id,
        new_shares=attribution_data.number_of_share
    )
    
    # 4. Génération et enregistrement du PDF
    db_file = generate_and_save_pdf(db_attribution, db)
    
    # 5. Mise à jour de l'attribution avec l'ID du fichier
    db_attribution.emission_certificate_file_id = db_file.id
    db.add(db_attribution)
    db.commit()
    db.refresh(db_attribution)
    
    return db_attribution


def get_attribution_by_id(db: Session, attribution_id: uuid.UUID):
    """
    Récupère une attribution par son ID.
    """
    return db.query(Attribution).filter(Attribution.id == attribution_id).first()

def get_all_attributions(
    db: Session,
    user: User,
    skip: int = 0,
    limit: int = 100
):
    """
    Récupère une liste d'attributions en fonction du rôle de l'utilisateur.
    """
    if user.status == UserRole.ADMIN:
        # Si c'est un ADMIN, retourne toutes les attributions
        return db.query(Attribution).offset(skip).limit(limit).all()
    else:
        # Si c'est un USER, retourne seulement ses attributions
        # On doit utiliser la relation pour filtrer les attributions par l'ID de l'actionnaire
        share_holder_id = user.share_holder.id
        if not share_holder_id:
            return [] # L'utilisateur n'est pas un actionnaire, donc aucune attribution
            
        return db.query(Attribution)\
                 .filter(Attribution.share_holder_id == share_holder_id)\
                 .offset(skip).limit(limit).all()


def get_certificate_file_by_attribution_id(db: Session, attribution_id: uuid.UUID):
    """
    Récupère le fichier de certificat d'émission associé à une attribution.
    """
    attribution = get_attribution_by_id(db, attribution_id)
    if not attribution or not attribution.emission_certificate_file:
        return None
    return attribution.emission_certificate_file.storage_path

#################################################################################################" 


