"""
./app/core/decorators/hooks.py
@hooks - Système de hooks
"""

from typing import Dict, List, Callable, Any
from ...enums.hooks import HookType


class HooksDecorator:
    """Décorateur pour le système de hooks"""
    
    def __init__(self, hooks_config: Dict[str, List[str]], hooks_params: Dict[str, Dict[str, Any]] = None):
        self.hooks_config = hooks_config
        self.hooks_params = hooks_params
    
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