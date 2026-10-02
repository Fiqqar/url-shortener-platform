from fastapi import HTTPException

from app.core import redis as redis_manager
from app.core.exceptions import RedisUnavailableError


async def get_redis_client():
    client = redis_manager.get_client()
    if client is None:
        raise RedisUnavailableError("Redis not initialized")
    try:
        await client.ping()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Storage unavailable") from exc
    return client
