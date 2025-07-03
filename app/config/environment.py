"""
./app/config/environment.py
Gestion des variables d'environnement
"""

import os
from typing import Dict, Any, Optional
from functools import lru_cache
from .settings import Settings


def load_env_vars() -> Dict[str, Any]:
    """Charge et valide les variables d'environnement"""
    return {
        "database_url": os.getenv("DATABASE_URL"),
        "secret_key": os.getenv("SECRET_KEY"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "dev_mode": os.getenv("DEV_MODE", "false").lower() == "true",
    }


@lru_cache()
def get_settings() -> Settings:
    """Retourne une instance cachée des settings"""
    return Settings()