# permissions.py
from enum import Enum
from typing import List, Type, Dict, Any
from .user_roles import UserRole

class PermissionsMode(Enum):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"

class PermissionsRegister:
    """Central registry storing permissions for each model and user role."""

    _registry: Dict[str, Dict[UserRole, Dict[str, Any]]] = {}

    @classmethod
    def register(cls, model: Type, role: UserRole, mode: PermissionsMode, attributes: List[str]) -> None:
        """Register permissions for a specific model and user role, including inherited permissions."""
        model_name = model.__name__

        # Initialize entry
        if model_name not in cls._registry:
            cls._registry[model_name] = {}

        # Start from inherited permissions
        inherited_mode = None
        inherited_attrs = set()

        for base in model.__mro__[1:]:  # skip self
            base_name = base.__name__
            if base_name in cls._registry and role in cls._registry[base_name]:
                base_perm = cls._registry[base_name][role]
                inherited_mode = base_perm["mode"]
                inherited_attrs |= set(base_perm["attributes"])

        # Merge logic between inherited and current
        if inherited_mode is None:
            # No inheritance: just register the provided configuration
            merged_mode = mode
            merged_attrs = set(attributes)
        else:
            # If modes are the same: merge the attribute lists
            if inherited_mode == mode:
                merged_mode = mode
                merged_attrs = inherited_attrs | set(attributes)
            else:
                # If modes differ, the child definition takes precedence
                merged_mode = mode
                merged_attrs = set(attributes)

        # Register merged result
        cls._registry[model_name][role] = {
            "mode": merged_mode,
            "attributes": merged_attrs
        }

    @classmethod
    def get_permissions(cls, model: Type, role: UserRole) -> Dict[str, Any]:
        """Retrieve permissions for a given model and user role."""
        model_name = model.__name__
        return cls._registry.get(model_name, {}).get(role, {})

    @classmethod
    def has_access(cls, model: Type, role: UserRole, attribute: str) -> bool:
        """Check if a role has access to a specific attribute."""
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

def Permissions(role: UserRole, mode: PermissionsMode = PermissionsMode.WHITELIST, attributes: List[str] = []):
    """Decorator to register model attribute permissions for a given user role."""
    def decorator(cls):
        PermissionsRegister.register(cls, role, mode, attributes)
        return cls
    return decorator