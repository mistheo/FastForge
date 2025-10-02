from enums import Enum

class UserRole(Enum):
    PUBLIC = 'public'
    USERS = 'users'
    USER = 'user'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'

class EndpointConfig:
    def __init__(
        self,
        enable : bool = True,
        user_role: UserRole = UserRole.USERS,
        custom_auth_function: function = None):
        
        self.enable : bool = enable
        self.user_role: UserRole = user_role
        self.custom_auth_function = custom_auth_function
    
    def validate_config(self):
        if not isinstance(self.enable, bool):
            raise ValueError("Enable must be a boolean value.")
        if not isinstance(self.user_role, UserRole):
            raise ValueError("User role must be an instance of UserRole enum.")
        if self.custom_auth_function is not None and not callable(self.custom_auth_function):
            raise ValueError("Custom auth function must be callable or None.")

        return True