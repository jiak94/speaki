import redis
from app import config
import typing


class Redis(redis.Redis):
    redis_client = None

    def init(self, host=config.REDIS_HOST, port=config.REDIS_PORT):
        self.redis_client = redis.Redis(host=host, port=port)

    def set(self, key: str, value: bytes, expiration=0):
        self.redis_client.set(key, value)
        if expiration > 0:
            self.redis_client.expire(key, expiration)

    def get(self, key: str) -> bytes:
        return self.redis_client.get(key)


redis_client = Redis()
