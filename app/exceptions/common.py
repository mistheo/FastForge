"""
Common exceptions
"""

from .base import FastForgeException
import traceback


class PermissionDenied(FastForgeException):
    """Exception pour permissions insuffisantes"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


class ResourceNotFound(FastForgeException):
    """Exception pour ressource non trouvée"""
    
    def __init__(self, resource: str, id: str):
        message = f"{resource} with id {id} not found"
        super().__init__(message, 404)

class ServerError(FastForgeException):
    """Exception pour erreur interne du serveur"""

    def __init__(self, message: str = "Internal server error", include_traceback: bool = False):
        if include_traceback:
            tb = traceback.format_exc()
            message = f"{message}\nTraceback:\n{tb}"
        super().__init__(message, 500)

class BadRequest(FastForgeException):
    """Exception pour requête invalide"""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message, 400)