"""
./app/core/auth/jwt_manager.py
Gestion des tokens JWT
"""

from typing import Dict, Optional
from ...models.user import UserModel


class JWTAuth:
    """Gestionnaire d'authentification JWT"""
    
    def __init__(self, secret_key: str, expire_minutes: int = 30):
        self.secret_key = secret_key
        self.expire_minutes = expire_minutes
    
    def create_access_token(self, data: Dict) -> str:
        """Crée un token d'accès"""
        pass
    
    def verify_token(self, token: str) -> Dict:
        """Vérifie et décode un token"""
        pass
    
    def get_current_user(self, token: str) -> UserModel:
        """Récupère l'utilisateur actuel depuis le token"""
        pass
    
    def hash_password(self, password: str) -> str:
        """Hash un mot de passe"""
        pass
    
    def verify_password(self, password: str, hash: str) -> bool:
        """Vérifie un mot de passe contre son hash"""
        pass