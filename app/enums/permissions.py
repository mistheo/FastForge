"""
./app/enums/permissions.py
Permissions, User Roles, FieldVisibility enumerations
"""

from enum import Enum


class Permission(str, Enum):
    """Enumération des permissions"""
    PUBLIC = "public"
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserRole(str, Enum):
    """Enumération des rôles utilisateur"""
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class FieldVisibility(str, Enum):
    """Enumération de la visibilité des champs"""
    PUBLIC = "public"
    USERS = "users"
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"