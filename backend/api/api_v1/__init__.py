from fastapi import APIRouter
from core.config import settings
from .players import router as players_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)
router.include_router(
    players_router,
    prefix=settings.api.v1.players
)