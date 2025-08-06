# tests/test_services.py
import pytest
from core.services.attribution_service import attribution_service, user_service
from core.schemas.attribution_schema import AttributionCreate
from core.models import Participation, User,ShareHolders,ShareInsurance
from core.enurations import UserRole
from datetime import datetime
import uuid

def test_create_attribution_exceeds_limit(db_session):
    # Crée un utilisateur et un actionnaire pour le test
    test_user = user_service.create_user(db_session, email="test@example.com", password="password")
    share_holder = ShareHolders(first_name="John", phone_number="123456789", user_id=test_user.id)
    db_session.add(share_holder)
    db_session.commit()
    db_session.refresh(share_holder)

    # Crée une emission d'action avec seulement 100 parts
    share_insurance = ShareInsurance(number_of_share=100)
    db_session.add(share_insurance)
    db_session.commit()
    db_session.refresh(share_insurance)

    # Simule une attribution qui dépasse la limite
    attribution_data = AttributionCreate(
        share_insurance_id=share_insurance.id,
        share_holder_id=share_holder.id,
        number_of_share=150,
        attribution_date=datetime.now()
    )

    # Vérifie que la fonction lève une erreur
    with pytest.raises(ValueError, match="Le nombre total d'actions attribuées dépasse le nombre total disponible."):
        attribution_service.create_attribution(db_session, attribution_data)

def test_get_all_attributions_as_admin(db_session):
    # Crée un utilisateur ADMIN
    admin_user = User(email="admin@example.com", status=UserRole.ADMIN)
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)
    
    
    # Vérifie que l'ADMIN voit toutes les attributions
    attributions = attribution_service.get_all_attributions(db_session, user=admin_user)
    assert len(attributions) > 0

def test_create_attribution_updates_participation(db_session, setup_attribution_data):
    # Récupère les données préparées par la fixture
    share_holder = setup_attribution_data["share_holder"]
    share_insurance = setup_attribution_data["share_insurance"]

    # 1. Première attribution
    attribution_data_1 = AttributionCreate(
        share_insurance_id=share_insurance.id,
        share_holder_id=share_holder.id,
        number_of_share=50,
        attribution_date=datetime.now()
    )
    attribution_service.create_attribution(db_session, attribution_data_1)

    # Vérifie que la participation a été créée avec 50 parts
    participation = db_session.query(Participation).filter(
        Participation.share_holder_id == share_holder.id
    ).first()
    assert participation is not None
    assert participation.total_share == 50

    # 2. Deuxième attribution
    attribution_data_2 = AttributionCreate(
        share_insurance_id=share_insurance.id,
        share_holder_id=share_holder.id,
        number_of_share=30,
        attribution_date=datetime.now()
    )
    attribution_service.create_attribution(db_session, attribution_data_2)

    # Vérifie que la participation a été mise à jour avec 80 parts (50 + 30)
    db_session.refresh(participation)
    assert participation.total_share == 80