from fastapi import APIRouter

from api.api_v1.fastapi_users import fastapi_users
from core.schemas.user import UserRead, UserUpdate

router = APIRouter(tags=["Users"])

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
