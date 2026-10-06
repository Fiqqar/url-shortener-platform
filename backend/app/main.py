import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from redis.exceptions import RedisError

from app.api import health, urls
from app.core import redis as redis_manager
from app.core.body_limit import BodySizeLimitMiddleware
from app.core.config import settings
from app.core.exceptions import (
    AnalyticsNotFoundError,
    InvalidShortCodeError,
    RedisUnavailableError,
    URLCreationError,
    URLNotFoundError,
)
from app.core.logging import configure_logging
from app.core.middleware import RequestIDMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    await redis_manager.init_redis(settings.redis_host, settings.redis_port, settings.redis_db)
    yield
    await redis_manager.close_redis()


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    app = FastAPI(title="url-shortener-platform", lifespan=lifespan)
    app.add_middleware(BodySizeLimitMiddleware, max_bytes=settings.max_body_bytes)
    app.add_middleware(RequestIDMiddleware)
    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["X-Request-ID", "Content-Type"],
    )

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.exception_handler(URLNotFoundError)
    @app.exception_handler(AnalyticsNotFoundError)
    async def not_found_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=404, content={"detail": "Short URL not found"})

    @app.exception_handler(InvalidShortCodeError)
    async def bad_request_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=400, content={"detail": "Invalid short code"})

    @app.exception_handler(URLCreationError)
    async def creation_error_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=400, content={"detail": "Could not create short URL"})

    @app.exception_handler(RedisUnavailableError)
    async def redis_down_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=503, content={"detail": "Storage unavailable"})

    @app.exception_handler(RedisError)
    @app.exception_handler(TimeoutError)
    async def redis_operation_error_handler(request: Request, exc: Exception):
        logger.exception("Redis operation failed")
        return JSONResponse(status_code=503, content={"detail": "Storage unavailable"})

    app.include_router(health.router)
    app.include_router(urls.router)

    # Expose /metrics BEFORE the catch-all /{code} redirect route,
    # otherwise GET /metrics is shadowed by redirect with code="metrics".
    Instrumentator().instrument(app).expose(app, include_in_schema=False)

    app.include_router(urls.redirect_router)

    return app


app = create_app()
