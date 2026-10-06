from uuid import uuid4

import pytest
import redis.asyncio as redis

TEST_REDIS_DB = 15


class _NamespacedPipeline:
    def __init__(self, pipeline, prefix: str):
        self._pipeline = pipeline
        self._prefix = prefix

    async def __aenter__(self):
        await self._pipeline.__aenter__()
        return self

    async def __aexit__(self, *exc_info):
        return await self._pipeline.__aexit__(*exc_info)

    def set(self, key: str, value):
        self._pipeline.set(self._prefix + key, value)
        return self

    async def execute(self):
        return await self._pipeline.execute()


class _NamespacedRedis:
    def __init__(self, client, prefix: str):
        self._client = client
        self._prefix = prefix

    async def ping(self):
        return await self._client.ping()

    async def incr(self, key: str):
        return await self._client.incr(self._prefix + key)

    async def get(self, key: str):
        return await self._client.get(self._prefix + key)

    async def delete(self, *keys: str):
        return await self._client.delete(*(self._prefix + key for key in keys))

    def pipeline(self, transaction: bool = True):
        return _NamespacedPipeline(self._client.pipeline(transaction=transaction), self._prefix)

    async def delete_test_keys(self):
        keys = [key async for key in self._client.scan_iter(match=f"{self._prefix}*")]
        if keys:
            await self._client.delete(*keys)


@pytest.fixture
async def test_redis():
    raw_client = redis.Redis(host="localhost", port=6379, db=TEST_REDIS_DB, decode_responses=True)
    await raw_client.ping()
    client = _NamespacedRedis(raw_client, f"pytest:{uuid4().hex}:")
    try:
        yield client
    finally:
        await client.delete_test_keys()
        await raw_client.aclose()
