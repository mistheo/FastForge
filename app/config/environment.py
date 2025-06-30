"""
Gestion des variables d'environnement
"""

import os
from typing import Dict, Any, Optional
from functools import lru_cache
from .settings import Settings


def load_env_vars() -> Dict[str, Any]:
    """Charge et valide les variables d'environnement"""
    
    pass


@lru_cache()
def get_settings() -> Settings:
    """Retourne une instance cachée des settings"""
    
    pass