from fastapi import APIRouter

from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.auth.backend import auth_backend

router = APIRouter(tags=["Auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend))
