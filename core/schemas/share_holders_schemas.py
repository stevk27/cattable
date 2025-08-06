from pydantic import BaseModel,Field
from typing import Optional
import uuid
from datetime import datetime
from .user_schemas import User, UserBase, UserCreate


class ShareHolderBase(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    phone_number: str


class ShareHolderCreate(ShareHolderBase):
    user:UserCreate
    created_by_id: Optional[uuid.UUID] = None

class ShareHolderUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserMinimal(BaseModel):
    id: uuid.UUID
    email: str

    class Config:
        orm_mode = True


class ShareHolderResponse(ShareHolderBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_by_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    user: User
    created_by: Optional[User] = None
    
    class Config:
        from_attributes = True