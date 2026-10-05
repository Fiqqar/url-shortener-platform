import logging

from app.core.base62 import encode_base62
from app.core.exceptions import (
    AnalyticsNotFoundError,
    URLCreationError,
    URLNotFoundError,
)
from app.observability import metrics
from app.repositories import url_repository
from app.services.validation import validate_code, validate_url

logger = logging.getLogger(__name__)


async def create_short_url(client, target_url: str) -> dict:
    try:
        target = validate_url(target_url)
    except ValueError as exc:
        metrics.ERRORS.labels(error_type="creation").inc()
        raise URLCreationError(str(exc)) from exc
    try:
        seq_id = await url_repository.next_id(client)
        code = encode_base62(seq_id)
        await url_repository.save_url(client, code, target)
    except Exception:
        metrics.REDIS_ERRORS.labels(operation="create").inc()
        raise
    metrics.URLS_CREATED.inc()
    return {"code": code, "target": target}


async def resolve_redirect(client, code: str) -> str:
    validate_code(code)
    try:
        target = await url_repository.get_url(client, code)
    except Exception:
        metrics.REDIS_ERRORS.labels(operation="redirect_read").inc()
        raise
    if target is None:
        raise URLNotFoundError(f"Unknown code: {code}")
    # Availability first: redirect works even if analytics increment fails.
    try:
        await url_repository.incr_clicks(client, code)
    except Exception:
        metrics.REDIS_ERRORS.labels(operation="incr_clicks").inc()
        logger.exception("analytics increment failed", extra={"code": code})
    metrics.REDIRECTS.inc()
    return target


async def get_analytics(client, code: str) -> dict:
    validate_code(code)
    try:
        target = await url_repository.get_url(client, code)
    except Exception:
        metrics.REDIS_ERRORS.labels(operation="analytics_read").inc()
        raise
    if target is None:
        raise AnalyticsNotFoundError(f"Unknown code: {code}")
    try:
        clicks = await url_repository.get_clicks(client, code)
    except Exception:
        metrics.REDIS_ERRORS.labels(operation="analytics_read").inc()
        raise
    metrics.ANALYTICS_REQUESTS.inc()
    return {"code": code, "target": target, "clicks": clicks or 0}
