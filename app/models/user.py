"""
Modèle User héritant de ModelData.

Ce module définit le modèle User de l'application. Il hérite du comportement
de traçabilité, de propriété et de suppression douce de ModelData et ajoute
des champs et méthodes spécifiques à l'utilisateur (gestion des mots de passe,
rôles, vérification, dernière connexion).

Note: Utilisez un algorithme de hachage de mot de passe sécurisé (argon2 ou bcrypt)
en production. Le simple sha256 utilisé ici est à titre de démonstration uniquement.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List, Dict
import hashlib

from odmantic import Field

from app.models.model_data import ModelData
from app.config.user_roles import UserRole
from app.config.permissions_config import Permissions, PermissionsRegister


# Annotations de permissions définissant quels champs chaque rôle peut accéder
@Permissions(UserRole.SUPERADMIN, [
    "email", "username", "roles", "is_verified", "last_login"
])
@Permissions(UserRole.ADMIN, [
    "email", "username", "roles",
    "is_verified", "last_login"
])
@Permissions(UserRole.USER, [
    "email", "username", "is_verified", "last_login"
])
@Permissions(UserRole.PUBLIC, [],overwrite_attrs=True)
class User(ModelData):
    """
    Modèle User.

    Attributs:
        email: Adresse email de l'utilisateur (unique)
        username: Nom d'utilisateur optionnel / pseudonyme (unique si fourni)
        hashed_password: Hash du mot de passe ; ne pas exposer
        roles: Liste des noms de rôles attribués à l'utilisateur
        is_verified: Indique si l'utilisateur a validé son compte (email, etc.)
        last_login: Horodatage de la dernière authentification réussie
        profile: Métadonnées flexibles pour l'utilisateur (préférences UI, URL avatar...)
        allow_ownership_transfer: Si True, autorise le transfert de propriété des enregistrements
    """

    # Champs d'authentification
    email: str = Field(..., unique=True, index=True, max_length=254)
    username: Optional[str] = Field(default=None, unique=True, index=True, max_length=150)
    hashed_password: Optional[str] = Field(default=None)

    # Autorisation et vérification
    roles: List[UserRole] = Field(default_factory=lambda: [UserRole.USER], index=True)
    groupes : List[str] = Field(default_factory=list, index=True)
    is_verified: bool = Field(default=False, index=True)

    # Activité
    last_login: Optional[datetime] = Field(default=None)

    # Profil flexible
    profile: Dict = Field(default_factory=dict)

    # Flags de fonctionnalités au niveau du modèle
    allow_ownership_transfer: bool = Field(default=False)

    # ----------------------------
    # Méthodes utilitaires
    # ----------------------------
    
    def set_password(self, raw_password: str) -> None:
        """
        Définit le mot de passe de l'utilisateur.

        Commentaire: Cette implémentation utilise sha256 comme placeholder.
        Remplacez par une fonction de hachage de mot de passe sécurisée
        (argon2, bcrypt ou scrypt) via une bibliothèque éprouvée (ex: passlib)
        en production.

        Args:
            raw_password: Mot de passe en clair
        """
        # Hachage simple de démonstration - PAS POUR LA PRODUCTION
        digest = hashlib.sha256(raw_password.encode("utf-8")).hexdigest()
        self.hashed_password = digest
        self.update_timestamp()

    def verify_password(self, raw_password: str) -> bool:
        """
        Vérifie un mot de passe candidat contre le hash stocké.

        Args:
            raw_password: Mot de passe en clair à vérifier

        Returns:
            bool: True si correspond, False sinon
        """
        if not self.hashed_password:
            return False
        candidate = hashlib.sha256(raw_password.encode("utf-8")).hexdigest()
        return candidate == self.hashed_password

    def update_last_login(self) -> None:
        """Met à jour last_login à maintenant (UTC) et rafraîchit updated_at."""
        self.last_login = datetime.now(timezone.utc)
        self.update_timestamp()

    # Gestion des rôles
    def add_role(self, role: str) -> None:
        """Ajoute un rôle à l'utilisateur s'il n'est pas déjà présent."""
        if role not in self.roles:
            self.roles.append(role)
            self.update_timestamp()

    def remove_role(self, role: str) -> None:
        """Retire un rôle de l'utilisateur s'il est présent."""
        if role in self.roles:
            self.roles.remove(role)
            self.update_timestamp()

    def has_role(self, role: str) -> bool:
        """Retourne True si l'utilisateur a le rôle."""
        return role in self.roles

    # Helpers de propriété
    
    def enable_ownership_transfer(self) -> None:
        """Autorise cet utilisateur à transférer la propriété de ses enregistrements."""
        self.allow_ownership_transfer = True
        self.update_timestamp()

    def disable_ownership_transfer(self) -> None:
        """Interdit le transfert de propriété pour cet utilisateur."""
        self.allow_ownership_transfer = False
        self.update_timestamp()

    def __repr__(self) -> str:
        return (
            f"<User(public_id={self.public_id}, email={self.email}, "
            f"is_active={self.is_active})>"
        )

    def __str__(self) -> str:
        return f"User {self.public_id} ({self.email})"