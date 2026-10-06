from redis.exceptions import RedisError

SEQUENCE_KEY = "meta:urls:sequence"


def url_key(code: str) -> str:
    return f"url:{code}"


def clicks_key(code: str) -> str:
    return f"analytics:{code}:clicks"


async def next_id(client) -> int:
    return int(await client.incr(SEQUENCE_KEY))


async def save_url(client, code: str, target: str) -> None:
    try:
        async with client.pipeline(transaction=True) as pipeline:
            pipeline.set(url_key(code), target)
            pipeline.set(clicks_key(code), 0)
            await pipeline.execute()
    except RedisError:
        # Redis transactions do not roll back individual command errors, so
        # remove either key if EXEC failed after only one write took effect.
        try:
            await client.delete(url_key(code), clicks_key(code))
        except RedisError:
            pass
        raise


async def get_url(client, code: str) -> str | None:
    return await client.get(url_key(code))


async def incr_clicks(client, code: str) -> int:
    return int(await client.incr(clicks_key(code)))


async def get_clicks(client, code: str) -> int | None:
    value = await client.get(clicks_key(code))
    return None if value is None else int(value)
