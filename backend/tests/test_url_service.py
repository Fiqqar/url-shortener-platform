import pytest

from app.core.exceptions import (
    AnalyticsNotFoundError,
    URLCreationError,
    URLNotFoundError,
)
from app.services import url_service


class FakeRedis:
    def __init__(self):
        self.store: dict = {}

    async def incr(self, key):
        self.store[key] = int(self.store.get(key, 0)) + 1
        return self.store[key]

    async def set(self, key, value):
        self.store[key] = value

    async def get(self, key):
        return self.store.get(key)


@pytest.mark.asyncio
async def test_create_then_redirect_counts_click():
    db = FakeRedis()
    created = await url_service.create_short_url(db, "https://example.com/a")
    assert created["code"]
    target = await url_service.resolve_redirect(db, created["code"])
    assert target == "https://example.com/a"
    stats = await url_service.get_analytics(db, created["code"])
    assert stats["clicks"] == 1


@pytest.mark.asyncio
async def test_create_rejects_bad_url():
    with pytest.raises(URLCreationError):
        await url_service.create_short_url(FakeRedis(), "ftp://example.com/x")


@pytest.mark.asyncio
async def test_redirect_unknown_code():
    with pytest.raises(URLNotFoundError):
        await url_service.resolve_redirect(FakeRedis(), "nope123")


@pytest.mark.asyncio
async def test_analytics_unknown_code():
    with pytest.raises(AnalyticsNotFoundError):
        await url_service.get_analytics(FakeRedis(), "nope123")
