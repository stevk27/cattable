from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from typing import Annotated
import os

from ..database import get_db
from .models import File

router = APIRouter()

UPLOAD_DIRECTORY = "./uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/upload/")
async def upload_file(
    file: Annotated[UploadFile, File()],
    db: Session = Depends(get_db)
):
    try:
        # Chemin où le fichier sera stocké
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

        # Écriture du fichier sur le disque
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Création d'un enregistrement dans la base de données
        new_file = File(
            file_name=file.filename,
            storage_path=file_path,
            type_of_file=file.content_type
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
    
    except Exception as e:
        return {"message": "Erreur lors du téléchargement du fichier"}
    
    return {"message": "Fichier téléchargé avec succès", "id": new_file.id}
