from fastapi import APIRouter
from core.config import settings
from .auth import router as auth_router
from .players import router as players_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)
router.include_router(
    auth_router,
    prefix=settings.api.v1.auth
)
router.include_router(
    players_router,
    prefix=settings.api.v1.players
)