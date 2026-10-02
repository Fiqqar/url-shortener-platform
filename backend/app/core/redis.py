import redis.asyncio as redis

_client: redis.Redis | None = None


def get_client() -> redis.Redis | None:
    return _client


async def init_redis(host: str, port: int, db: int) -> redis.Redis:
    global _client
    _client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    await _client.ping()
    return _client


async def close_redis() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def ping_redis() -> bool:
    if _client is None:
        return False
    try:
        await _client.ping()
        return True
    except Exception:
        return False
