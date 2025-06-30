"""
HTTP Methods enumeration
"""

from enum import Enum


class HTTPMethod(str, Enum):
    """Enumération des méthodes HTTP"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"