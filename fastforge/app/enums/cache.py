"""
CacheType, CacheDuration, RateWindow, Rate Limit related enumerations
"""

from enum import Enum


class CacheType(str, Enum):
    """Enumération des types de cache"""
    MEMORY = "memory"
    DATABASE = "database"


class CacheDuration(int, Enum):
    """Enumération des durées de cache (en secondes)"""
    SHORT = 60      # 1 minute
    MEDIUM = 300    # 5 minutes
    LONG = 3600     # 1 heure


class RateWindow(str, Enum):
    """Enumération des fenêtres de rate limiting"""
    SECOND = "1sec"
    MINUTE = "1min"
    HOUR = "1hour"
    DAY = "1day"


class RateLimit(int, Enum):
    """Enumération des limites de rate limiting"""
    LOW = 10
    MEDIUM = 100
    HIGH = 1000
    UNLIMITED = -1