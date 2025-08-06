# tests/conftest.py
# (Ce fichier est lu par pytest et contient les fixtures de test)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.enurations import UserRole
from main import app
from database import Base, get_db
from fastapi.testclient import TestClient

from core.models import ShareHolders, ShareInsurance, User

# Utiliser une base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture de base de données
@pytest.fixture()
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture pour remplacer la dépendance de la BDD
@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def setup_attribution_data(db_session):
    # Crée un utilisateur
    user = User(email="testuser@example.com", password="hashed_password", status=UserRole.USER)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Crée un actionnaire
    share_holder = ShareHolders(
        first_name="Jane",
        last_name="Doe",
        phone_number="123456789",
        user_id=user.id
    )
    db_session.add(share_holder)
    db_session.commit()
    db_session.refresh(share_holder)

    # Crée une assurance d'actions avec un nombre total de 500
    share_insurance = ShareInsurance(
        number_of_share=500,
        type_action="Class A",
        unit_price=10.0
    )
    db_session.add(share_insurance)
    db_session.commit()
    db_session.refresh(share_insurance)

    return {
        "user": user,
        "share_holder": share_holder,
        "share_insurance": share_insurance
    }