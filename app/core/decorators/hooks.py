"""
./app/core/decorators/hooks.py
@hooks - Système de hooks
"""

from typing import Dict, List, Callable, Any
from ...enums.hooks import HookType


class HooksDecorator:
    """Décorateur pour le système de hooks"""
    
    def __init__(self, hooks_config: Dict[str, List[str]]):
        self.hooks_config = hooks_config
    
    def __call__(self, func: Callable) -> Callable:
        """Applique le décorateur à la fonction"""
        pass
    
    def execute_hooks(self, hook_type: HookType, **kwargs) -> Any:
        """Exécute les hooks d'un type donné"""
        pass


def hooks(**hooks_config) -> Callable:
    """Décorateur pour le système de hooks"""
    
    def decorator(func: Callable) -> Callable:
        func._fastforge_hooks_config = hooks_config
        return func
    
    return decorator