from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from core.schemas.user_schemas import User
from core.services.user_service import authenticate_user
from database import get_db
from utils.jwt import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from core.schemas.login_schemas import Token  # Importez le schéma Token

router = APIRouter(
    tags=["auth"]
)

@router.post("/token", response_model=Token) # Utilisez le nouveau schéma ici
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants de connexion invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # La conversion est gérée par Pydantic grâce à `response_model=Token`
    return {"access_token": access_token, "token_type": "bearer", "user": user} 