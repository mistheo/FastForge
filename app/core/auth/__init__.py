"""
./app/core/auth/__init__.py
Authentication module - Expose JWTAuth et PermissionManager
"""

from .jwt_manager import JWTAuth
from .permissions import PermissionManager

__all__ = [
    'JWTAuth',
    'PermissionManager'
]