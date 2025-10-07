# permissions.py
from enum import Enum
from typing import List, Type, Dict, Any
from .user_roles import UserRole

class PermissionsMode(Enum):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"

class PermissionsRegister:
    """Central registry managing model attribute permissions per user role."""

    _registry: Dict[str, Dict[UserRole, Dict[str, Any]]] = {}

    @classmethod
    def register(cls, model: Type, role: UserRole, mode: PermissionsMode, attributes: List[str]) -> None:
        """Register permissions for a model and a user role (no inheritance applied here)."""
        model_name = model.__name__.split('.')[0]
        if model_name not in cls._registry:
            cls._registry[model_name] = {}

        cls._registry[model_name][role] = {
            "mode": mode,
            "attributes": set(attributes),
        }

    @classmethod
    def get_permissions(cls, model: Type, role: UserRole) -> Dict[str, Any]:
        """Return merged permissions across the full inheritance chain (MRO)."""
        merged_mode = None
        merged_attributes: set = set()

        # Traverse MRO from base to derived class
        for base in reversed(model.__mro__):
            base_name = base.__name__.split('.')[0]
            # Skip non-registered classes
            if base_name not in cls._registry:
                continue

            role_permissions = cls._registry[base_name].get(role)
            if not role_permissions:
                continue

            # Merge modes and attributes
            base_mode = role_permissions["mode"]
            base_attributes = role_permissions["attributes"]

            if merged_mode is None:
                merged_mode = base_mode
            elif merged_mode != base_mode:
                # Child overrides the mode if different
                merged_mode = base_mode

            merged_attributes |= base_attributes  # Union of all sets

        # If nothing found, return empty dict
        if merged_mode is None:
            return {}

        return {"mode": merged_mode, "attributes": merged_attributes}

    @classmethod
    def has_access(cls, model: Type, role: UserRole, attribute: str) -> bool:
        """Check if a user role has access to a specific attribute."""
        perms = cls.get_permissions(model, role)
        if not perms:
            return False

        mode = perms["mode"]
        attrs = perms["attributes"]

        if mode == PermissionsMode.WHITELIST:
            return attribute in attrs
        elif mode == PermissionsMode.BLACKLIST:
            return attribute not in attrs
        return False



def Permissions(role: UserRole, mode: PermissionsMode, attributes: List[str]):
    """Decorator to register model attribute permissions for a given user role.
    Only allowed on subclasses of ModelData.
    """
    def decorator(cls):
        PermissionsRegister.register(cls, role, mode, attributes)
        return cls
    return decorator

def AllUserRolePermissions(mode:PermissionsMode, attributes: List[str]):
    
    def decorator(cls):
        for role in list(UserRole):
            PermissionsRegister.register(cls, role, mode, attributes)
        return cls
    
    return decorator