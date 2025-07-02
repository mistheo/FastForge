"""
@custom_endpoint - Endpoints personnalisés
"""

from typing import List, Dict, Callable
from ...enums.http import HTTPMethod
from ...enums.permissions import Permission


class CustomEndpointDecorator:
    """Décorateur pour les endpoints personnalisés"""
    
    def __init__(
        self,
        method: HTTPMethod,
        path: str,
        permissions: List[Permission],
        auth_required: bool = True,
        rate_limit: Dict[str, int] = None
    ):
        self.method = method
        self.path = path
        self.permissions = permissions
        self.auth_required = auth_required
        self.rate_limit = rate_limit or {}
    
    def __call__(self, func: Callable) -> Callable:
        """Applique le décorateur à la fonction"""
        pass


def custom_endpoint(
    method: HTTPMethod,
    path: str,
    permissions: List[Permission] = None,
    auth_required: bool = True,
    rate_limit: Dict[str, int] = None
) -> Callable:
    """Décorateur pour endpoints personnalisés"""
    
    def decorator(func: Callable) -> Callable:
        func._fastforge_endpoint_config = {
            'method': method,
            'path': path,
            'permissions': permissions or [],
            'auth_required': auth_required,
            'rate_limit': rate_limit or {}
        }
        return func
    
    return decorator