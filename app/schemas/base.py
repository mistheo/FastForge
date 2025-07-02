"""
BaseSchema pour réponses
"""

from datetime import datetime
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Schéma de base pour les réponses API"""
    
    id: str # Corresponds à l'id public pour BaseModel models.BaseModel
    creation_date: datetime
    update_date: datetime
    
    class Config:
        from_attributes = True