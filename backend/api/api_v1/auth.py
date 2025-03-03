from fastapi import APIRouter


from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.auth.backend import auth_backend
from core.schemas.user import UserRead, UserCreate


router = APIRouter(tags=["Auth"])

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(
        auth_backend,
        # requires_verification=True
    )
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

router.include_router(
    router=fastapi_users.get_verify_router(UserRead)
)

router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
