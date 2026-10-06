import pytest
from httpx import ASGITransport, AsyncClient
from redis.exceptions import ConnectionError as RedisConnectionError

from app.api.dependencies import get_redis_client
from app.core import redis as redis_manager
from app.main import create_app


@pytest.fixture
async def api_client(test_redis):
    app = create_app()

    async def override():
        return test_redis

    app.dependency_overrides[get_redis_client] = override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client, test_redis
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_url_returns_201_with_short_code(api_client):
    client, _ = api_client
    resp = await client.post("/api/v1/urls", json={"url": "https://example.com/some/long/path"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["code"]
    assert body["short_url"].endswith(f"/{body['code']}")
    assert body["target_url"] == "https://example.com/some/long/path"


@pytest.mark.asyncio
async def test_create_url_rejects_unsupported_scheme_with_400(api_client):
    client, _ = api_client
    resp = await client.post("/api/v1/urls", json={"url": "ftp://example.com/file"})
    assert resp.status_code == 400
    assert "detail" in resp.json()


@pytest.mark.asyncio
async def test_create_url_returns_422_for_missing_field(api_client):
    client, _ = api_client
    resp = await client.post("/api/v1/urls", json={})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_url_metadata_returns_info(api_client):
    client, _ = api_client
    created = (await client.post("/api/v1/urls", json={"url": "https://example.com/meta"})).json()
    resp = await client.get(f"/api/v1/urls/{created['code']}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["code"] == created["code"]
    assert body["target_url"] == "https://example.com/meta"
    assert body["clicks"] == 0


@pytest.mark.asyncio
async def test_get_url_metadata_returns_404_for_unknown_code(api_client):
    client, _ = api_client
    resp = await client.get("/api/v1/urls/ZZZ999nope")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_redirect_returns_307_with_location(api_client):
    client, _ = api_client
    created = (await client.post("/api/v1/urls", json={"url": "https://example.com/go"})).json()
    resp = await client.get(f"/{created['code']}", follow_redirects=False)
    assert resp.status_code in (301, 302, 303, 307, 308)
    assert resp.headers["location"] == "https://example.com/go"


@pytest.mark.asyncio
async def test_redirect_returns_404_for_unknown_code(api_client):
    client, _ = api_client
    resp = await client.get("/ZZZ999nope", follow_redirects=False)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_redirect_returns_400_for_invalid_code(api_client):
    client, _ = api_client
    resp = await client.get("/not valid!", follow_redirects=False)
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_analytics_returns_clicks(api_client):
    client, _ = api_client
    created = (await client.post("/api/v1/urls", json={"url": "https://example.com/stats"})).json()
    await client.get(f"/{created['code']}", follow_redirects=False)
    resp = await client.get(f"/api/v1/urls/{created['code']}/analytics")
    assert resp.status_code == 200
    assert resp.json() == {"code": created["code"], "clicks": 1}


@pytest.mark.asyncio
async def test_analytics_returns_404_for_unknown_code(api_client):
    client, _ = api_client
    resp = await client.get("/api/v1/urls/ZZZ999nope/analytics")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_health_returns_ok(api_client):
    client, _ = api_client
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_readiness_returns_ready_when_redis_up(api_client):
    client, test_redis = api_client
    redis_manager._client = test_redis
    try:
        resp = await client.get("/ready")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ready"}
    finally:
        redis_manager._client = None


@pytest.mark.asyncio
async def test_readiness_returns_503_when_redis_down(api_client):
    client, _ = api_client
    redis_manager._client = None
    resp = await client.get("/ready")
    assert resp.status_code == 503


@pytest.mark.asyncio
async def test_create_rejects_oversized_body_before_redis_access():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/urls",
            content=b"x" * 32769,
            headers={"content-type": "application/json"},
        )
    assert response.status_code == 413


@pytest.mark.asyncio
async def test_chunked_oversized_body_is_bounded():
    app = create_app()

    async def body_chunks():
        yield b"x" * 20000
        yield b"x" * 20000

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/urls",
            content=body_chunks(),
            headers={"content-type": "application/json"},
        )
    assert response.status_code == 413


@pytest.mark.asyncio
async def test_redis_operation_error_returns_sanitized_503():
    app = create_app()

    class BrokenRedis:
        async def get(self, key):
            raise RedisConnectionError("private redis host details")

    async def override():
        return BrokenRedis()

    app.dependency_overrides[get_redis_client] = override
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/Abc123")
    assert response.status_code == 503
    assert response.json() == {"detail": "Storage unavailable"}
    assert "private redis host details" not in response.text
