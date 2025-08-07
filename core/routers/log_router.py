from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.schemas.log_schemas import AuditEvent
from  database import get_db
from core.models import User
from core.services import log_service
from utils.get_current_user import get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/audit-log", response_model=List[AuditEvent])
def get_audit_log(
    current_user: User = Depends(get_current_admin_user), # Seuls les admins peuvent accéder
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Affiche le journal d'audit de toutes les actions critiques.
    """
    logs = log_service.get_all_audit_events(db=db, skip=skip, limit=limit)
    return logs