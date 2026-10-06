import asyncio

import pytest
from fastapi import HTTPException

from app.api.dependencies import get_redis_client
from app.core import redis as redis_manager
from app.core.exceptions import RedisUnavailableError
from app.services import url_service


@pytest.mark.asyncio
async def test_parallel_creates_yield_no_duplicate_codes(test_redis):
    targets = [f"https://example.com/page-{i}" for i in range(20)]
    results = await asyncio.gather(*[url_service.create_short_url(test_redis, t) for t in targets])
    codes = [r["code"] for r in results]
    assert len(set(codes)) == len(codes)


@pytest.mark.asyncio
async def test_redis_unreachable_init_fails_fast():
    try:
        with pytest.raises(Exception):
            await asyncio.wait_for(
                redis_manager.init_redis(
                    "10.255.255.1",
                    6379,
                    0,
                    socket_connect_timeout=1.0,
                    socket_timeout=1.0,
                ),
                timeout=15,
            )
    finally:
        redis_manager._client = None


@pytest.mark.asyncio
async def test_missing_redis_client_raises_unavailable_error():
    redis_manager._client = None
    try:
        with pytest.raises(RedisUnavailableError) as exc_info:
            await get_redis_client()
        assert str(exc_info.value) == "Redis not initialized"
    finally:
        redis_manager._client = None


@pytest.mark.asyncio
async def test_redis_ping_failure_counts_metric_and_raises_503():
    import redis.asyncio as redis

    from app.observability import metrics

    before = metrics.REDIS_ERRORS.labels(operation="dependency_ping")._value.get()
    redis_manager._client = redis.Redis(
        host="10.255.255.1",
        port=6379,
        db=0,
        socket_connect_timeout=1.0,
        socket_timeout=1.0,
    )
    try:
        with pytest.raises(HTTPException) as exc_info:
            await asyncio.wait_for(get_redis_client(), timeout=30)
        assert exc_info.value.status_code == 503
    finally:
        await redis_manager._client.aclose()
        redis_manager._client = None
    after = metrics.REDIS_ERRORS.labels(operation="dependency_ping")._value.get()
    assert after == before + 1


@pytest.mark.asyncio
async def test_create_rejects_javascript_scheme(test_redis):
    from app.core.exceptions import URLCreationError

    with pytest.raises(URLCreationError):
        await url_service.create_short_url(test_redis, "javascript:alert(1)")
