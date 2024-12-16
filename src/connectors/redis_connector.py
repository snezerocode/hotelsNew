import logging

import redis.asyncio as redis
# import redis


class RedisManager:
    _redis: redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        """Устанавливает асинхронное подключение к Редису"""
        logging.info(f"Начинаю подключение к Redis host={self.host} , port={self.port}")
        self._redis = await redis.Redis(host=self.host, port=self.port)
        logging.info("Успешное подключение к Redis")

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
