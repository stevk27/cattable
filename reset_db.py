# reset_db.py

from core.models import Base  # ← adapte ce chemin si nécessaire
from database import engine    # ← idem

print("⚠️ Suppression de toutes les tables...")
Base.metadata.drop_all(bind=engine)

print("✅ Recréation de toutes les tables...")
Base.metadata.create_all(bind=engine)

print("🎉 Base de données réinitialisée avec succès.")
