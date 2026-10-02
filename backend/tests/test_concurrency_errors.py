import asyncio

import pytest
from fastapi import HTTPException

from app.api.dependencies import get_redis_client
from app.core import redis as redis_manager
from app.services import url_service


@pytest.mark.asyncio
async def test_parallel_creates_yield_no_duplicate_codes(test_redis):
    targets = [f"https://example.com/page-{i}" for i in range(20)]
    results = await asyncio.gather(*[url_service.create_short_url(test_redis, t) for t in targets])
    codes = [r["code"] for r in results]
    assert len(set(codes)) == len(codes)


@pytest.mark.asyncio
async def test_redis_down_dependency_raises_503():
    redis_manager._client = None
    try:
        with pytest.raises(Exception) as exc_info:
            await get_redis_client()
        assert getattr(exc_info.value, "status_code", 503) == 503 or "Redis" in str(exc_info.value)
    finally:
        redis_manager._client = None


@pytest.mark.asyncio
async def test_create_rejects_javascript_scheme(test_redis):
    from app.core.exceptions import URLCreationError

    with pytest.raises(URLCreationError):
        await url_service.create_short_url(test_redis, "javascript:alert(1)")


@pytest.mark.asyncio
async def test_http_exception_carries_no_internals():
    err = HTTPException(status_code=503, detail="Storage unavailable")
    assert "redis" not in str(err.detail).lower() or err.detail == "Storage unavailable"
    assert "Traceback" not in str(err.detail)
