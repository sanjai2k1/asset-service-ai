import time
from core.logging  import logging

logger = logging.getLogger(__name__)

class CacheProvider:
    def __init__(self):
        self._cache = {}

    def set(self, key, value):
        self._cache[key] = value

    def get(self, key):
        return self._cache.get(key)

    def invalidate(self, key):
        self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()

    # 👉 Allow cache["key"]
    def __getitem__(self, key):
        return self._cache.get(key, [])