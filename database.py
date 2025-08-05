from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Crée le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crée une instance de SessionLocal pour chaque requête
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crée une base de classe pour les modèles de la base de données
Base = declarative_base()

# Crée une fonction pour la gestion des sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()