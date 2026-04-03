import time
from core.logging  import logging

logger = logging.getLogger(__name__)

class CacheProvider:
    _cache = {}   
    @classmethod
    def set(cls, key, value):
        cls._cache[key] = value

    @classmethod
    def get(cls, key):
        return cls._cache.get(key)

    @classmethod
    def invalidate(cls, key):
        cls._cache.pop(key, None)

    @classmethod
    def clear(cls):
        cls._cache.clear()

    @classmethod
    def __getitem__(cls, key):
        return cls._cache.get(key, [])
    @classmethod
    def __class_getitem__(cls, key):
        return cls._cache.get(key, [])
    @classmethod
    def cache_health(cls):
        return {"status": bool(cls._cache)}