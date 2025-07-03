"""
./app/middleware/cors.py
Configuration CORS
"""

from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware


class CORSMiddleware:
    """Middleware CORS pour FastAPI"""
    
    def __init__(
        self,
        allow_origins: List[str] = None,
        allow_credentials: bool = True,
        allow_methods: List[str] = None,
        allow_headers: List[str] = None
    ):
        self.allow_origins = allow_origins or ["*"]
        self.allow_credentials = allow_credentials
        self.allow_methods = allow_methods or ["*"]
        self.allow_headers = allow_headers or ["*"]
    
    def setup(self, app: FastAPI):
        """Configure CORS sur l'application FastAPI"""
        pass