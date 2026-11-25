import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.mark.asyncio
async def test_valid_request_id_is_echoed():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health", headers={"X-Request-ID": "trace_abc-123"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "trace_abc-123"


@pytest.mark.asyncio
@pytest.mark.parametrize("supplied", ["bad id!", "a" * 65, "<script>alert(1)</script>"])
async def test_unsafe_request_id_is_replaced(supplied):
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health", headers={"X-Request-ID": supplied})
    assert response.status_code == 200
    value = response.headers["x-request-id"]
    assert value != supplied
    assert len(value) == 12
    assert all(c in "0123456789abcdef" for c in value)
