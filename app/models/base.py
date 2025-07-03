"""
./app/models/base.py
BaseModel avec champs standardisés
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from bson import ObjectId
import uuid


class BaseModel:
    """Modèle de base standardisé pour tous les modèles"""
    
    def __init__(self):
        self._id: Optional[ObjectId] = None
        self.id_public: str = str(uuid.uuid4(timezone.utc))
        self.creation_date: datetime = datetime.now(timezone.utc)
        self.update_date: datetime = datetime.now()
        self.id_create_by: Optional[str] = None
        self.is_active: bool = True
        self.metadata: Dict[str, Any] = {}
    
    def save(self):
        """Sauvegarde l'objet en base de données"""
        pass
    
    def delete(self):
        """Supprime l'objet de la base de données"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire"""
        pass