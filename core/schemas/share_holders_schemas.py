from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from .user_schemas import User


class ShareHolderBase(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    phone_number: str


class ShareHolderCreate(ShareHolderBase):
    user_id: uuid.UUID


class ShareHolder(ShareHolderBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    user: User
    
    class Config:
        from_attributes = True