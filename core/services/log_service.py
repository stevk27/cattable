from sqlalchemy.orm import Session
from core.models import AuditEvent,User

##################################################################################################################""
def log_event(db: Session, user: User, action: str, details: str = None):
    """
    Enregistre un événement d'audit dans la base de données.
    """
    audit_event = AuditEvent(
        user_id=user.id,
        action=action,
        details=details
    )
    db.add(audit_event)
    db.commit()
    db.refresh(audit_event)
    return audit_event

def get_all_audit_events(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère la liste de tous les événements d'audit.
    """
    return db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).offset(skip).limit(limit).all()