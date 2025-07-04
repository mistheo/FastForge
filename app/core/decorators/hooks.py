"""
./app/core/decorators/hooks.py
@hooks - Système de hooks
"""

from typing import Dict, List, Callable, Any
from ...enums.hooks import HookType
from ...exceptions.base import FastForgeException


class HooksDecorator:
    """Décorateur pour le système de hooks"""
    
    def __init__(self, hooks_config: Dict[str, List[str]], hooks_params: Dict[str, Dict[str, Any]] = {}):
        self.hooks_config = hooks_config
        self.hooks_params = hooks_params
        
        self._validate_hook_config()
    
    def _validate_hook_config(self):
        """Valide que la configuration des hooks est correcte"""
        valid_hook_types = {e.value for e in HookType} + {"hook_params"}
        
        for hook_type, hook_names in self.hooks_config.items():
            if hook_type not in valid_hook_types:
                raise FastForgeException(
                    f"Invalid hook type: {hook_type}. Valid types: {valid_hook_types}",
                    status_code=500
                )
            
            if not isinstance(hook_names, list):
                raise FastForgeException(
                    f"Hook names must be a list for type {hook_type}",
                    status_code=500
                )
    
    def _execute_with_hooks(self, func: Callable, is_async: bool, *args, **kwargs):
        """Exécute la fonction avec tous ses hooks"""
        pass
    
    def __call__(self, func: Callable) -> Callable:
        """Applique le décorateur à la fonction"""
        pass
    
    def execute_hooks(self, hook_type: HookType, **kwargs) -> Any:
        """Exécute les hooks d'un type donné"""
        pass
    


def hooks(**hooks_config) -> Callable:
    """
    Décorateur pour le système de hooks
    
    Args:
        before_request: Liste des hooks à exécuter avant traitement de la requête
        after_request: Liste des hooks à exécuter après traitement de la requête  
        before_auth: Liste des hooks à exécuter avant authentification
        after_auth: Liste des hooks à exécuter après authentification
        before_response: Liste des hooks à exécuter avant envoi de la réponse
        on_error: Liste des hooks à exécuter en cas d'erreur
        hook_params: Paramètres spécifiques pour chaque hook
        
    Example:
        @hooks(
            before_request=["log_request"],
            after_auth=["update_last_login"],
            hook_params={
                "log_request": {"log_level": "INFO"}
            }
        )
        def my_endpoint():
            return {"data": "response"}

    """
        
    def decorator(func: Callable) -> Callable:
        func._fastforge_hooks_config = hooks_config
        return func
    
    return decorator