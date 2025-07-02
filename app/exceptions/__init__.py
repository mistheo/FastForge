"""
Exceptions module - Expose FastForgeException and common exception classes
"""

from .base import FastForgeException
from .common import PermissionDenied, ResourceNotFound, ServerError, BadRequest

__all__ = [
    'FastForgeException',
    'PermissionDenied',
    'ResourceNotFound',
    'ServerError',
    'BadRequest'
]