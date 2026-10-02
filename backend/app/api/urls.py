from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.api.dependencies import get_redis_client
from app.core.config import settings
from app.core.exceptions import (
    AnalyticsNotFoundError,
    InvalidShortCodeError,
    URLCreationError,
    URLNotFoundError,
)
from app.schemas.urls import (
    AnalyticsResponse,
    CreateURLRequest,
    CreateURLResponse,
    URLInfoResponse,
)
from app.services import url_service
from app.services.validation import validate_code

router = APIRouter(prefix="/api/v1/urls", tags=["urls"])
redirect_router = APIRouter(tags=["redirect"])


def short_url_for(code: str) -> str:
    return f"{settings.base_url.rstrip('/')}/{code}"


@router.post("", response_model=CreateURLResponse, status_code=201)
async def create_url(payload: CreateURLRequest, client=Depends(get_redis_client)):
    try:
        result = await url_service.create_short_url(client, payload.url)
    except URLCreationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CreateURLResponse(
        code=result["code"],
        short_url=short_url_for(result["code"]),
        target_url=result["target"],
    )


@router.get("/{code}", response_model=URLInfoResponse)
async def get_url_info(code: str, client=Depends(get_redis_client)):
    try:
        validate_code(code)
    except InvalidShortCodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid short code") from exc
    try:
        stats = await url_service.get_analytics(client, code)
    except AnalyticsNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Short URL not found") from exc
    return URLInfoResponse(
        code=code,
        short_url=short_url_for(code),
        target_url=stats["target"],
        clicks=stats["clicks"],
    )


@router.get("/{code}/analytics", response_model=AnalyticsResponse)
async def get_analytics(code: str, client=Depends(get_redis_client)):
    try:
        validate_code(code)
    except InvalidShortCodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid short code") from exc
    try:
        stats = await url_service.get_analytics(client, code)
    except AnalyticsNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Short URL not found") from exc
    return AnalyticsResponse(code=code, clicks=stats["clicks"])


@redirect_router.get("/{code}", include_in_schema=False)
async def redirect(code: str, client=Depends(get_redis_client)):
    try:
        validate_code(code)
    except InvalidShortCodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid short code") from exc
    try:
        target = await url_service.resolve_redirect(client, code)
    except URLNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Short URL not found") from exc
    return RedirectResponse(url=target, status_code=307)
