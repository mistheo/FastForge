"""
./app/core/decorators/crud.py
@crud_model - Génération CRUD automatique
"""

from typing import List, Dict, Any, Callable, Type
from fastapi import FastAPI
from ...enums.crud import CRUDOperation
from ...enums.permissions import FieldVisibility
from ...enums.cache import CacheDuration

class CRUDDecorator:
    """Décorateur pour la génération automatique des routes CRUD"""
    
    def __init__(
        self,
        collection: str,
        operations: List[CRUDOperation],
        permissions: Dict[CRUDOperation, Any],
        field_visibility: Dict[FieldVisibility, List[str]],
        cache_enabled: bool = True,
        cache_duration: CacheDuration = CacheDuration.MEDIUM
    ):
        self.collection = collection
        self.operations = operations
        self.permissions = permissions
        self.field_visibility = field_visibility
        self.cache_enabled = cache_enabled
        self.cache_duration = cache_duration
    
    def __call__(self, cls: Type) -> Type:
        """Applique le décorateur à la classe"""
        pass
    
    def generate_routes(self, app: FastAPI):
        """Génère les routes CRUD pour FastAPI"""
        pass


def crud_model(
    collection: str,
    operations: List[CRUDOperation],
    permissions: Dict[CRUDOperation, Any] = None,
    field_visibility: Dict[FieldVisibility, List[str]] = None,
    cache_enabled: bool = True,
    cache_duration: int = 300
) -> Callable:
    """Décorateur principal pour générer les endpoints CRUD"""
    
    def decorator(cls: Type) -> Type:
        # Stocke la config dans la classe
        cls._fastforge_crud_config = {
            'collection': collection,
            'operations': operations,
            'permissions': permissions or {},
            'field_visibility': field_visibility or {},
            'cache_enabled': cache_enabled,
            'cache_duration': cache_duration
        }
        return cls
    
    return decorator