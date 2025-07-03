"""
Implémentation cache mémoire
"""

from typing import Any, Dict
import time


class MemoryCache:
    """Cache en mémoire pour le développement"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Any:
        """Récupère une valeur du cache mémoire"""
        pass
    
    def set(self, key: str, value: Any, duration: int = 300):
        """Stocke une valeur dans le cache mémoire"""
        pass
    
    def delete(self, key: str):
        """Supprime une clé du cache mémoire"""
        pass
    
    def clear(self):
        """Vide le cache mémoire"""
        pass
    
    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """Vérifie si une entrée du cache est expirée"""
        pass