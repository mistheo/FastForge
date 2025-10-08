"""
Modèle de base MongoDB avec système d'ownership et traçabilité.

Ce module définit le modèle de base utilisé par tous les modèles de l'API.
Il inclut les champs essentiels pour la traçabilité, l'ownership et le soft delete.
"""
from datetime import datetime, timezone
from typing import Optional, ClassVar, List, Dict
from uuid import uuid4

from bson import ObjectId
from odmantic import Model, Field
from app.config.user_roles import UserRole
from app.config.permissions_config import Permissions

@Permissions(UserRole.SUPERADMIN, ["internal_id","public_id", "created_at", "updated_at", "is_active", "created_by", "owner_id"])
@Permissions(UserRole.ADMIN, ["public_id", "created_at", "updated_at", "is_active", "created_by", "owner_id"])
@Permissions(UserRole.USER, ["public_id", "created_at", "updated_at"])
@Permissions(UserRole.PUBLIC, ["public_id", "created_at", "updated_at"])
# @Permissions(UserRole.PUBLIC, PermissionsMode.WHITELIST, [])
class ModelData(Model):
    """
    Modèle de base pour tous les modèles MongoDB de l'API.
    
    Attributs:
        internal_id: ID interne MongoDB (ObjectId) - utilisé uniquement en interne
        public_id: ID exposé publiquement (UUID) - utilisé dans les APIs
        created_at: Date et heure de création
        updated_at: Date et heure de dernière modification
        is_active: Indicateur de soft delete (True = actif, False = supprimé)
        created_by: ID de l'utilisateur créateur (ObjectId)
        owner_id: ID du propriétaire de l'enregistrement (ObjectId)
    
    Configuration:
        - Collection MongoDB générée automatiquement depuis le nom de la classe
        - Index sur public_id pour des recherches optimisées
        - Index sur owner_id pour les requêtes de propriété
        - Index sur is_active pour filtrer les enregistrements actifs
    """
    
    # ID interne MongoDB - ne jamais exposer publiquement
    internal_id: ObjectId = Field(default_factory=ObjectId, key_name="_id", primary_field=True)
    
    # ID public - exposé via l'API (UUID pour éviter l'énumération)
    public_id: str = Field(
        default_factory=lambda: str(uuid4()),
        unique=True,
        index=True
    )
    
    # Horodatage automatique
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Soft delete - permet de désactiver sans supprimer
    is_active: bool = Field(default=True, index=True)
    
    # Traçabilité des créateurs
    created_by: Optional[ObjectId] = Field(default=None, index=True)
    
    # Système d'ownership
    owner_id: Optional[ObjectId] = Field(default=None, index=True)
    
    def update_timestamp(self) -> None:
        """Met à jour le timestamp de modification."""
        self.updated_at = datetime.now(timezone.utc)
    
    def soft_delete(self) -> None:
        """
        Effectue un soft delete de l'enregistrement.
        L'enregistrement reste en base mais is_active = False.
        """
        self.is_active = False
        self.update_timestamp()
    
    def restore(self) -> None:
        """Restaure un enregistrement soft deleted."""
        self.is_active = True
        self.update_timestamp()
    
    def is_owned_by(self, user_id: ObjectId) -> bool:
        """
        Vérifie si l'enregistrement appartient à un utilisateur donné.
        
        Args:
            user_id: ObjectId de l'utilisateur à vérifier
            
        Returns:
            bool: True si l'utilisateur est le propriétaire, False sinon
        """
        return self.owner_id == user_id
    
    def is_created_by(self, user_id: ObjectId) -> bool:
        """
        Vérifie si l'enregistrement a été créé par un utilisateur donné.
        
        Args:
            user_id: ObjectId de l'utilisateur à vérifier
            
        Returns:
            bool: True si l'utilisateur est le créateur, False sinon
        """
        return self.created_by == user_id
    
    def set_owner(self, user_id: ObjectId) -> None:
        """
        Définit le propriétaire de l'enregistrement.
        
        Args:
            user_id: ObjectId du nouveau propriétaire
        """
        self.owner_id = user_id
        self.update_timestamp()
    
    def transfer_ownership(self, new_owner_id: ObjectId) -> None:
        """
        Transfère la propriété de l'enregistrement à un autre utilisateur.
        
        Args:
            new_owner_id: ObjectId du nouveau propriétaire
            
        Note:
            Cette méthode doit être appelée avec les vérifications appropriées
            selon la configuration du modèle (allow_ownership_transfer).
        
        Exemple:
            @model(ModelConfig(...))
            class ExampleArticle(BaseModel):
                title: str = Field(max_length=200)
                content: str
                is_published: bool = Field(default=False)
                date_published: Optional[datetime] = None
        """
        self.owner_id = new_owner_id
        self.update_timestamp()
    
    def _to_public_dict(self, exclude_fields: Optional[List[str]] = None) -> Dict:
        """
        Retourne un dictionnaire sûr pour l'exposition publique.

        S'assure que les champs sensibles comme hashed_password sont supprimés
        en plus des exclusions du modèle de base.
        """
        exclude_fields += ["hashed_password"]
        
        public = ModelData._to_public_dict(self,exclude_fields=exclude_fields)
        return public
    
    @staticmethod
    def _to_public_dict(obj : "ModelData", exclude_fields: Optional[list[str]] = None) -> dict:
        """
        Convertit le modèle en dictionnaire pour exposition publique.
        
        Args:
            exclude_fields: Liste des champs supplémentaires à exclure
            
        Returns:
            dict: Dictionnaire sans les champs sensibles
        """        
        data = obj.model_dump()
        
        # Supprimer les champs sensibles
        for field in exclude_fields:
            data.pop(field, None)
        
        return data
    
    @staticmethod
    def to_owner_dict(cls) -> dict:
        """
        Convertit le modèle en dictionnaire pour le propriétaire.
        Inclut plus de détails que to_public_dict().
        
        Returns:
            dict: Dictionnaire avec les champs du propriétaire
        """
        data = cls.model_dump()
        
        # Exclure uniquement l'internal_id
        data.pop("internal_id", None)
        data.pop("_id", None)
        
        return data       
    
    def __repr__(self) -> str:
        """Représentation string du modèle."""
        return f"<{self.__class__.__name__}(internal_id={self.internal_id}, public_id={self.public_id}, is_active={self.is_active})>"
    
    def __str__(self) -> str:
        """Représentation string user-friendly."""
        return f"{self.__class__.__name__} {self.public_id}"