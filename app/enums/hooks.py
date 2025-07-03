"""
./app/enums/hooks.py
Hooks enumeration
"""

from enum import Enum


class HookType(str, Enum):
    """Enumération des types de hooks"""
    BEFORE_REQUEST = "before_request"
    AFTER_REQUEST = "after_request"
    BEFORE_AUTH = "before_auth"
    AFTER_AUTH = "after_auth"
    BEFORE_RESPONSE = "before_response"
    ON_ERROR = "on_error"