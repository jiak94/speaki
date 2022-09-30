from aioredis import Redis

from app import config


class Cache(Redis):
    def init(self, host=config.REDIS_HOST, port=config.REDIS_PORT):
        super().from_url(f"redis://{host}:{port}")


cache_client = Cache()
