import redis

class RedisCache:
    def __init__(self, url='redis://localhost:6379/0'):
        self.client = redis.Redis.from_url(url)
    def get(self, key):
        return self.client.get(key)
    def set(self, key, value):
        self.client.set(key, value) 