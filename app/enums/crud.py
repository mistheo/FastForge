"""
./app/enums/crud.py
CRUD Operations enumeration
"""

from enum import Enum


class CRUDOperation(str, Enum):
    """Enumération des opérations CRUD"""
    LIST = "list"
    GET = "get"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"