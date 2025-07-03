"""
./app/models/user.py
UserModel avec authentification
"""

from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from .base import BaseModel
from ..enums.permissions import UserRole


class UserModel(BaseModel):
    """Modèle utilisateur avec authentification"""
    
    def __init__(self):
        super().__init__()
        self.username: str
        self.addremail: EmailStr = ""
        self.password_hash: str = ""
        self.role: UserRole = UserRole.USER
        self.last_login: Optional[datetime] = None
        self.is_verified: bool = False
    
    def verify_password(self, password: str) -> bool:
        """Vérifie si le mot de passe correspond"""
        pass
    
    def hash_password(self, password: str) -> str:
        """Hash le mot de passe"""
        pass