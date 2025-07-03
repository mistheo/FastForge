"""
Middlewares de sécurité
"""

from typing import Callable
from fastapi import Request, Response


class SecurityMiddleware:
    """Middleware de sécurité pour FastAPI"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Traite les requêtes avec les middlewares de sécurité"""
        pass
    
    def add_security_headers(self, response: Response):
        """Ajoute les headers de sécurité"""
        pass
    
    def validate_request(self, request: Request) -> bool:
        """Valide la requête entrante"""
        pass