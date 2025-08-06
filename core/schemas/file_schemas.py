from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class FileBase(BaseModel):
    file_name: str
    storage_path: str
    type_of_file: Optional[str] = None

class File(FileBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True