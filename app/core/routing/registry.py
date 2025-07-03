"""
Registre des modèles et endpoints
"""

from typing import Dict, List, Any


class RouterRegistry:
    """Registre pour les modèles et endpoints"""
    
    def __init__(self):
        self.crud_models: Dict[str, Any] = {}
        self.custom_endpoints: List[Any] = []
    
    def register_crud_model(self, name: str, model_config: Dict[str, Any]):
        """Enregistre un modèle CRUD"""
        pass
    
    def register_custom_endpoint(self, endpoint_config: Dict[str, Any]):
        """Enregistre un endpoint personnalisé"""
        pass
    
    def get_crud_models(self) -> Dict[str, Any]:
        """Retourne tous les modèles CRUD enregistrés"""
        pass
    
    def get_custom_endpoints(self) -> List[Any]:
        """Retourne tous les endpoints personnalisés"""
        pass