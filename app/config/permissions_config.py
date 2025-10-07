from typing import List, Type, Dict, Any
from .user_roles import UserRole


class PermissionsRegister:
    """Central registry managing model attribute permissions per user role."""
    
    _registry: Dict[str, Dict[UserRole, set]] = {}

    @classmethod
    def register(cls, model: Type, role: UserRole, attributes: List[str]) -> None:
        """Register accessible attributes for a given model and user role."""
        model_name = model.__name__.split('.')[0]

        if model_name not in cls._registry:
            cls._registry[model_name] = {}

        if role not in cls._registry[model_name]:
            cls._registry[model_name][role] = set()

        # Merge attributes with existing ones
        cls._registry[model_name][role].update(attributes)

    @classmethod
    def get_permissions(cls, model: Type, role: UserRole) -> set:
        """Return merged attributes from the inheritance chain for the given model and role."""
        merged_attributes: set = set()

        # Traverse inheritance chain (from base to derived)
        for base in reversed(model.__mro__):
            base_name = base.__name__.split('.')[0]
            if base_name not in cls._registry:
                continue

            role_attributes = cls._registry[base_name].get(role)
            if role_attributes:
                merged_attributes.update(role_attributes)

        return merged_attributes

    @classmethod
    def has_access(cls, model: Type, role: UserRole, attribute: str) -> bool:
        """Check if a user role can access a specific attribute."""
        allowed_attrs = cls.get_permissions(model, role)
        return attribute in allowed_attrs


def Permissions(role: UserRole, attributes: List[str]):
    """Decorator to register model attribute permissions for a given user role."""
    def decorator(cls):
        PermissionsRegister.register(cls, role, attributes)
        return cls
    return decorator


def AllUserRolePermissions(attributes: List[str], exclude_roles: List[UserRole] = []):
    """Decorator registering the same attributes for all roles, except the excluded ones."""
    def decorator(cls):
        for role in list(UserRole):
            if role not in exclude_roles:
                PermissionsRegister.register(cls, role, attributes)
        return cls
    return decorator
