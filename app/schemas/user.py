"""
./app/schemas/user.py
UserSchema + LoginForm
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from .base import BaseSchema
from ..enums.permissions import UserRole


class UserSchema(BaseSchema):
    """Schéma pour les données utilisateur"""
    
    username: str
    email: EmailStr
    role: UserRole
    last_login: Optional[datetime] = None