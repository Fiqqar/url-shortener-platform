import pytest
from redis.exceptions import ResponseError

from app.core.exceptions import (
    AnalyticsNotFoundError,
    URLCreationError,
    URLNotFoundError,
)
from app.repositories import url_repository
from app.services import url_service


class FakeRedis:
    def __init__(self):
        self.store: dict = {}

    async def incr(self, key):
        self.store[key] = int(self.store.get(key, 0)) + 1
        return self.store[key]

    async def set(self, key, value):
        self.store[key] = value

    def pipeline(self, transaction=True):
        return FakePipeline(self)

    async def get(self, key):
        return self.store.get(key)

    async def delete(self, *keys):
        for key in keys:
            self.store.pop(key, None)


class FakePipeline:
    def __init__(self, client):
        self.client = client
        self.pending = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return None

    def set(self, key, value):
        self.pending.append((key, value))
        return self

    async def execute(self):
        for key, value in self.pending:
            self.client.store[key] = value


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
async def test_save_url_cleans_partial_transaction_after_command_error():
    db = FakeRedis()

    class PartiallyCommittedPipeline(FakePipeline):
        async def execute(self):
            key, value = self.pending[0]
            self.client.store[key] = value
            raise ResponseError("simulated command error")

    def partial_pipeline(transaction=True):
        return PartiallyCommittedPipeline(db)

    db.pipeline = partial_pipeline
    with pytest.raises(ResponseError):
        await url_repository.save_url(db, "a1B2c3", "https://example.com")
    assert db.store == {}


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
