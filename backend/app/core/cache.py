from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

async def setup_cache():
    redis = aioredis.from_url("redis://redis:6379", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache") 