from enum import Enum

class UserRole(Enum):
    PUBLIC = 'public'
    USERS = 'users'
    USER = 'user'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'