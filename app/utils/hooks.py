"""
HookRegistry pour le système de hooks
"""

from typing import Dict, List, Callable, Any
from ..enums.hooks import HookType


class HookRegistry:
    """Registre des hooks pour le système de middleware"""
    
    def __init__(self):
        self.registered_hooks: Dict[str, Dict[str, Any]] = {}
    
    def register_hook(self, name: str, hook_type: HookType, func: Callable):
        """Enregistre un hook"""
        pass
    
    def execute_hook(self, name: str, **kwargs) -> Any:
        """Exécute un hook spécifique"""
        pass
    
    def get_hooks_by_type(self, hook_type: HookType) -> List[Callable]:
        """Récupère tous les hooks d'un type donné"""
        pass
    
    def unregister_hook(self, name: str):
        """Désenregistre un hook"""
        pass