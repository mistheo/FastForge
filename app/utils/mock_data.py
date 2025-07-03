"""
./app/utils/mock_data.py
MockDataGenerator pour le développement
"""

from typing import Dict, List, Callable, Any


class MockDataGenerator:
    """Générateur de données fictives pour le développement"""
    
    def __init__(self):
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.generators: Dict[str, Dict[str, Callable]] = {}
    
    def generate_mock_data(self, model_name: str, count: int = 10) -> List[Dict[str, Any]]:
        """Génère des données fictives pour un modèle"""
        pass
    
    def create_from_template(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une instance depuis un template"""
        pass
    
    def populate_dev_database(self):
        """Peuple la base de données de développement"""
        pass
    
    def register_template(self, model_name: str, template: Dict[str, Any]):
        """Enregistre un template pour un modèle"""
        pass
    
    def register_generator(self, model_name: str, field: str, generator: Callable):
        """Enregistre un générateur pour un champ"""
        pass