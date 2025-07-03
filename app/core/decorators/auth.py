"""
./app/core/decorators/auth.py
@requires_auth - Authentification
"""

from typing import List, Callable, Any
from ...enums.permissions import UserRole


class AuthDecorator:
    """Décorateur pour l'authentification"""
    
    def __init__(
        self,
        roles: List[UserRole],
        owner_access: bool = False,
        optional: bool = False
    ):
        self.roles = roles
        self.owner_access = owner_access
        self.optional = optional
    
    def __call__(self, func: Callable) -> Callable:
        """Applique le décorateur à la fonction"""
        pass


def requires_auth(
    roles: List[UserRole] = None,
    owner_access: bool = False,
    optional: bool = False
) -> Callable:
    """Décorateur pour l'authentification"""
    
    def decorator(func: Callable) -> Callable:
        func._fastforge_auth_config = {
            'roles': roles or [],
            'owner_access': owner_access,
            'optional': optional
        }
        return func
    
    return decorator