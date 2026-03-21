import time
from db.services.prompt_key_dependency_service import PromptKeyDependencyService
from db.cache.cache_provider import CacheProvider
from core.enums import PromptkeyDependency

class PromptDependencyCache:
    def __init__(self):
        self.service = PromptKeyDependencyService()
        self.cache = CacheProvider()

    def load(self, start_id: int):
        """
        Store as: cache[prompt_key][start_id] = data
        """
        try:
            data = self.service.get_prompt_dependency_tree(start_id)

            if not data:
                return []

            # 🔑 Extract main key
            cache_key = data[0].get("prompt_key")

            # Get existing group (or empty dict)
            existing = self.cache.get(cache_key) or {}

            # ✅ Store by start_id
            existing[start_id] = data

            # Save back
            self.cache.set(cache_key, existing)

            return data

        except Exception as e:
            print(f"[ERROR] {e}")
            return []

    # 👉 Allow direct usage: cache["SR_C"]
    def __getitem__(self, key):
        return self.cache[key]

    def invalidate(self, key):
        self.cache.invalidate(key)

    def clear(self):
        self.cache.clear()


prompt_cache = PromptDependencyCache()