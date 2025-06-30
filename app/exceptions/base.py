"""
Base exception class
"""

from typing import Dict, Optional


class FastForgeException(Exception):
    """Exception de base pour FastForge"""
    
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)