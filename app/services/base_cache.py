from abc import ABC, abstractmethod

from aioredis import Redis


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass

    @abstractmethod
    async def close(self):
        pass


class BaseRedisStorage(AsyncCacheStorage):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, **kwargs):
        return await self.redis.get(key=key)

    async def set(self, key: str, value: str, expire: int, **kwargs):
        return await self.redis.set(key=key, value=value, expire=expire)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()


class BaseCacheStorage:
    def __init__(self, cache: AsyncCacheStorage, **kwargs):
        super().__init__(**kwargs)

        self.cache = cache

        # Кэшируем на день
        self.CACHE_EXPIRE_IN_SECONDS = 60 * 60 * 24

    async def get_one_item_from_cache(self, cache_key: str, model):
        data = await self.cache.get(key=cache_key)

        if not data:
            return None

        return model.parse_raw(data)

    async def put_one_item_to_cache(self, cache_key: str, item):
        await self.cache.set(
            key=cache_key,
            value=item.json(),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )
