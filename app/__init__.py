"""
Application principale FastForge
"""

from fastapi import FastAPI
from .config.settings import Settings
from .core.routing import RouterGenerator
from .core.auth import JWTAuth, PermissionManager
from .core.cache import CacheManager
from .core.security import RateLimiter
from .utils.hooks import HookRegistry
from .utils.mock_data import MockDataGenerator


class FastForgeApp:
    """Application principale FastForge"""
    
    def __init__(self, settings: Settings):
        self.app: FastAPI = FastAPI()
        self.settings: Settings = settings
        self.router_generator: RouterGenerator = RouterGenerator()
        self.cache_manager: CacheManager = None
        self.auth_manager: JWTAuth = None
        self.permission_manager: PermissionManager = PermissionManager()
        self.rate_limiter: RateLimiter = RateLimiter()
        self.hook_registry: HookRegistry = HookRegistry()
        self.mock_generator: MockDataGenerator = MockDataGenerator()
    
    def initialize(self):
        """Initialise tous les composants"""
        pass
    
    def setup_middleware(self):
        """Configure les middlewares"""
        pass
    
    def setup_exception_handlers(self):
        """Configure les gestionnaires d'exceptions"""
        pass
    
    def run(self, host: str = "127.0.0.1", port: int = 8000):
        """Lance l'application"""
        pass