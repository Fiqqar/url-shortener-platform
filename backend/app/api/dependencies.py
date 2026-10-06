from fastapi import HTTPException

from app.core import redis as redis_manager
from app.core.exceptions import RedisUnavailableError
from app.observability import metrics


async def get_redis_client():
    client = redis_manager.get_client()
    if client is None:
        raise RedisUnavailableError("Redis not initialized")
    try:
        await client.ping()
    except Exception as exc:
        # Count here: this is the dominant Redis failure path (every request
        # pings first), and the RedisDown alert is driven by this counter.
        metrics.REDIS_ERRORS.labels(operation="dependency_ping").inc()
        raise HTTPException(status_code=503, detail="Storage unavailable") from exc
    return client
