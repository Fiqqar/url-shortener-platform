from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core import redis as redis_manager

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    if await redis_manager.ping_redis():
        return {"status": "ready"}
    return JSONResponse(status_code=503, content={"detail": "Storage unavailable"})
