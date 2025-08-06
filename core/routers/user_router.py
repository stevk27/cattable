from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.schemas.user_schemas import User, UserCreate,UserUpdate
from core.services import user_service 
from database import get_db
from utils.jwt import verify_token

##########################################################################################
router = APIRouter(
    prefix="/users",
    tags=["users"],
    
)


@router.get("/", response_model=List[User])
def read_all_users(db: Session = Depends(get_db)):
    users = user_service.get_users(db=db)
    return users

@router.put("/{user_id}", response_model=User)
def update_existing_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=User)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db=db,user=user)
    return user

