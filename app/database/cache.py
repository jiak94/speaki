import aioredis

from app import config

redis = aioredis.from_url(f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}")


async def set(key, value, ex=None):
    await redis.set(key, value, ex=ex)


async def get(key):
    return await redis.get(key)
