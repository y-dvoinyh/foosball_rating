from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router
from .players import router as players_router
from .users import router as users_router

http_bearer = HTTPBearer(auto_error=False)


router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)]
)
routers = [
    (auth_router, settings.api.v1.auth),
    (users_router, settings.api.v1.users),
    (players_router, settings.api.v1.players)
]
for route, prefix in routers:
    router.include_router(route, prefix=prefix)
