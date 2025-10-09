from typing import List, Type, Dict, Any
from .user_roles import UserRole


class PermissionsRegister:
    """Central registry managing model attribute permissions per user role."""

    # _registry maps: { model_name: { role: {"attributes": set(), "overwrite":
    # bool } } }
    _registry: Dict[str, Dict[UserRole, Dict[str, Any]]] = {}

    @classmethod
    def register(
            cls,
            model: Type,
            role: UserRole,
            attributes: List[str],
            overwrite: bool = False) -> None:
        """Register accessible attributes for a given model and user role."""
        model_name = model.__name__.split('.')[0]

        if model_name not in cls._registry:
            cls._registry[model_name] = {}

        if role not in cls._registry[model_name] or overwrite:
            # Overwrite existing attributes if overwrite is True
            cls._registry[model_name][role] = {
                "attributes": set(attributes), "overwrite": overwrite}
        else:
            # Merge attributes if overwrite is False
            cls._registry[model_name][role]["attributes"].update(attributes)
            # Ensure overwrite flag remains consistent
            cls._registry[model_name][role]["overwrite"] = cls._registry[model_name][role]["overwrite"] or overwrite

    @classmethod
    def get_permissions(cls, model: Type, role: UserRole) -> set:
        """Return attributes for the given model and role, considering overwrite flags."""
        model_name = model.__name__.split('.')[0]

        # If the model has an overwrite=True for this role, only return its
        # attributes
        if model_name in cls._registry and role in cls._registry[model_name]:
            if cls._registry[model_name][role].get("overwrite"):
                return cls._registry[model_name][role]["attributes"]

        # Otherwise, merge attributes from inheritance chain
        merged_attributes: set = set()
        for base in reversed(model.__mro__):
            base_name = base.__name__.split('.')[0]
            if base_name not in cls._registry:
                continue

            role_data = cls._registry[base_name].get(role)
            if role_data:
                merged_attributes.update(role_data["attributes"])

        return merged_attributes

    @classmethod
    def has_access(cls, model: Type, role: UserRole, attribute: str) -> bool:
        """Check if a user role can access a specific attribute."""
        allowed_attrs = cls.get_permissions(model, role)
        return attribute in allowed_attrs


def Permissions(
        role: UserRole,
        attributes: List[str],
        overwrite_attrs: bool = False):
    """Decorator to register model attribute permissions for a given user role."""
    def decorator(cls):
        PermissionsRegister.register(
            cls, role, attributes, overwrite=overwrite_attrs)
        return cls
    return decorator


def AllUserRolePermissions(
        attributes: List[str],
        exclude_roles: List[UserRole] = [],
        overwrite_attrs: bool = False):
    """Decorator registering the same attributes for all roles, except the excluded ones."""
    def decorator(cls):
        for role in list(UserRole):
            if role not in exclude_roles:
                PermissionsRegister.register(
                    cls, role, attributes, overwrite=overwrite_attrs)
        return cls
    return decorator
