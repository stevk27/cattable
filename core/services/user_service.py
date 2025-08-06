import datetime
from sqlalchemy.orm import Session
from typing import List
from core.models import User
from core.schemas.user_schemas import UserCreate,UserUpdate
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token

############################################################################################################################
################# User Service ########################### 
def get_user(db: Session, user_id: int):
    """
    Récupère un utilisateur par son ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère une liste d'utilisateurs.
    """
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """
    Crée un nouvel utilisateur dans la base de données.
    """
    # Ici, vous pourriez ajouter une logique comme le hachage du mot de passe
    # hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password= hash_password(user.password) , status=user.status)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """
    Met à jour un utilisateur existant.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    # Met à jour les attributs de l'utilisateur avec les valeurs non nulles
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """
    Supprime un utilisateur par son ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
        
    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Authentifie un utilisateur en vérifiant son email et son mot de passe.
    Retourne l'utilisateur si l'authentification est réussie, sinon None.
    """
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.password):
        return None
    
    # Met à jour la date de dernière connexion
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user