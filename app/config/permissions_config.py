# permissions.py
from enum import Enum
from typing import List, Type
from pydantic import BaseModel

class PermissionsMode(Enum):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"

class UserRole(Enum):
    PUBLIC = "public"
    USERS = "users"
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class PermissionsConfig:
    def __init__(self):
        self.configs = {}

    def register(self, model: Type[BaseModel], role: UserRole, mode: PermissionsMode, fields: List[str]):
        model_fields = set(model.model_fields.keys())
        for f in fields:
            if f not in model_fields:
                raise ValueError(f"Field '{f}' does not exist in {model.__name__}")
        model_config = self.configs.setdefault(model, {})
        field_set = model_config.setdefault((role, mode), set())
        field_set.update(fields)

    def get(self, model: Type[BaseModel], role: UserRole, mode: PermissionsMode) -> List[str]:
        return sorted(self.configs.get(model, {}).get((role, mode), []))

permissions_config = PermissionsConfig()

def Permissions(role: UserRole, mode: PermissionsMode, fields: List[str]):
    def decorator(cls: Type[BaseModel]):
        permissions_config.register(cls, role, mode, fields)
        return cls
    return decorator
