"""
Gestionnaire global des erreurs
"""

from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from ..exceptions import FastForgeException


class ErrorHandlerMiddleware:
    """Middleware de gestion d'erreurs pour FastAPI"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Gère les erreurs globalement"""
        pass
    
    def handle_fastforge_exception(self, request: Request, exc: FastForgeException) -> JSONResponse:
        """Gère les exceptions FastForge"""
        pass
    
    def handle_http_exception(self, request: Request, exc: HTTPException) -> JSONResponse:
        """Gère les exceptions HTTP standard"""
        pass
    
    def handle_generic_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Gère les exceptions génériques"""
        pass