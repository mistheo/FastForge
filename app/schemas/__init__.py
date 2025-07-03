"""
./app/schemas/__init__.py
Schemas module - Expose BaseSchema et tous les schémas
"""

from .base import BaseSchema
from .user import UserSchema

__all__ = [
    'BaseSchema',
    'UserSchema'
]