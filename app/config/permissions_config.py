from enum import Enum
from collections import defaultdict
from user_roles import UserRole


class PermissionsMode(Enum):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"

class PermissionsConfig:
    def __init__(self):
        self.configs: dict[UserRole, dict[PermissionsMode, list[str]]] = {
            role: defaultdict(list) for role in UserRole
        }

    def add_field(self, role: UserRole, mode: PermissionsMode, field: str):
        """Ajoute un champ pour un rôle/mode donné"""
        if not isinstance(role, UserRole):
            raise ValueError(f"Invalid role: {role}")
        if not isinstance(mode, PermissionsMode):
            raise ValueError(f"Invalid mode: {mode}")
        if not isinstance(field, str):
            raise ValueError("Field must be a string")

        self.configs[role][mode].append(field)

    def get_fields(self, role: UserRole, mode: PermissionsMode) -> List[str]:
        """Récupère les champs d'un rôle/mode donné"""
        return self.configs[role][mode]

    def validate(self) -> bool:
        """Valide la configuration complète"""
        for role, config_dict in self.configs.items():
            if not isinstance(config_dict, dict):
                raise ValueError(f"Config for {role} must be a dictionary.")
            for mode, fields in config_dict.items():
                if not isinstance(mode, PermissionsMode):
                    raise ValueError(f"Invalid mode in {role}: {mode}")
                if not isinstance(fields, list) or not all(isinstance(f, str) for f in fields):
                    raise ValueError(f"Fields for {role}/{mode} must be a list of strings")
        return True