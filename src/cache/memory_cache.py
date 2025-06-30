class MemoryCache:
    def __init__(self):
        self._cache = {}
    def get(self, key):
        return self._cache.get(key)
    def set(self, key, value):
        self._cache[key] = value 