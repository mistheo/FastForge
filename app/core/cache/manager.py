"""
Interface unifiée du cache
"""

from typing import Any, Optional, Dict
from motor.motor_asyncio import AsyncIOMotorClient
from ...enums.cache import CacheType


class CacheManager:
    """Gestionnaire de cache unifié"""
    
    def __init__(self, cache_type: CacheType, db_client: Optional[AsyncIOMotorClient] = None):
        self.cache_type = cache_type
        self.memory_cache: Dict[str, Any] = {}
        self.db_client = db_client
    
    def get(self, key: str) -> Any:
        """Récupère une valeur du cache"""
        pass
    
    def set(self, key: str, value: Any, duration: int = 300):
        """Stocke une valeur dans le cache"""
        pass
    
    def delete(self, key: str):
        """Supprime une clé du cache"""
        pass
    
    def clear(self):
        """Vide le cache"""
        pass