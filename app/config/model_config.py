from endpoint_config import EndpointConfig
from ownership_config import OwnershipConfig
from permissions_config import PermissionsRegister


class ModelConfig:
    def __init__(self):
        self.table_name: str
        self.description: str
        self.schema_name: str
        self.endpoints: dict[str, EndpointConfig] = {
            "get_one": EndpointConfig(),
            "get_all": EndpointConfig(),
            "create": EndpointConfig(),
            "update": EndpointConfig(),
            "delete": EndpointConfig()
        }
        self.ownership: OwnershipConfig = OwnershipConfig()
        self.permissions: PermissionsRegister = PermissionsRegister()

        def validate_model_config(self):
            if not isinstance(self.table_name, str) or not self.table_name:
                raise ValueError("Table name must be a non-empty string.")
            if not isinstance(self.description, str):
                raise ValueError("Description must be a string.")
            if not isinstance(self.schema_name, str) or not self.schema_name:
                raise ValueError("Schema name must be a non-empty string.")
            if not isinstance(self.endpoints, dict):
                raise ValueError("Endpoints must be a dictionary.")
            for key, config in self.endpoints.items():
                if key not in [
                    "get_one",
                    "get_all",
                    "create",
                    "update",
                        "delete"]:
                    raise ValueError(
                        f"Invalid endpoint key: {key}. Must be one of 'get_one', 'get_all', 'create', 'update', 'delete'.")
                if not isinstance(config, EndpointConfig):
                    raise ValueError(
                        f"Endpoint config for {key} must be an instance of EndpointConfig.")
            if not isinstance(self.ownership, OwnershipConfig):
                raise ValueError(
                    "Ownership must be an instance of OwnershipConfig.")
            if not isinstance(self.permissions, PermissionsRegister):
                raise ValueError(
                    "Permissions must be an instance of PermissionsConfig.")

            return True
