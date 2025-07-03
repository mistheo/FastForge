"""
./app/config/settings.py
Configuration Pydantic
"""

from pydantic_settings import BaseSettings
from typing import Optional
from ..enums.cache import CacheType


class Settings(BaseSettings):
    """Configuration de l'application avec Pydantic"""
    
    # Configuration générale
    DEBUG: bool = True
    DEV_MODE: bool = True
    
    # Base de données
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "fastforge"
    MOCK_DATABASE: bool = False
    
    # Sécurité
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuration globale
    GLOBAL_AUTH_REQUIRED: bool = True
    GLOBAL_CACHE_TYPE: CacheType = CacheType.DATABASE
    GLOBAL_CACHE_DURATION: int = 300
    GLOBAL_RATE_LIMIT: int = 100
    GLOBAL_RATE_WINDOW: str = "1hour"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"