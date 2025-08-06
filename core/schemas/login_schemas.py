from pydantic import BaseModel
from typing import Optional
from core.schemas.user_schemas import User # Importez le schéma User qui a `from_attributes=True`

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
    
    class Config:
        from_attributes = True