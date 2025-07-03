"""
./app/middleware/logging.py
Middleware de logging des requêtes
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response


logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Middleware de logging pour FastAPI"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Log les requêtes et réponses"""
        pass
    
    def log_request(self, request: Request):
        """Log les détails de la requête"""
        pass
    
    def log_response(self, request: Request, response: Response, process_time: float):
        """Log les détails de la réponse"""
        pass