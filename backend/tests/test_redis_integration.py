import pytest

from app.repositories import url_repository


@pytest.mark.asyncio
async def test_sequence_increments_monotonically(test_redis):
    first = await url_repository.next_id(test_redis)
    second = await url_repository.next_id(test_redis)
    assert second == first + 1


@pytest.mark.asyncio
async def test_url_storage_and_retrieval(test_redis):
    await url_repository.save_url(test_redis, "tSt0re1", "https://example.com/saved")
    assert await url_repository.get_url(test_redis, "tSt0re1") == "https://example.com/saved"


@pytest.mark.asyncio
async def test_missing_key_returns_none(test_redis):
    assert await url_repository.get_url(test_redis, "doesNotExist1") is None
    assert await url_repository.get_clicks(test_redis, "doesNotExist1") is None


@pytest.mark.asyncio
async def test_analytics_counter_increments(test_redis):
    await url_repository.save_url(test_redis, "tCl1ck1", "https://example.com/c")
    assert await url_repository.get_clicks(test_redis, "tCl1ck1") == 0
    assert await url_repository.incr_clicks(test_redis, "tCl1ck1") == 1
    assert await url_repository.incr_clicks(test_redis, "tCl1ck1") == 2
