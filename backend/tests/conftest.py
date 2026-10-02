import pytest
import redis.asyncio as redis

TEST_REDIS_DB = 15


@pytest.fixture
async def test_redis():
    client = redis.Redis(host="localhost", port=6379, db=TEST_REDIS_DB, decode_responses=True)
    await client.ping()
    yield client
    await client.flushdb()
    await client.aclose()
