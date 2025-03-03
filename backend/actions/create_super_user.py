from typing import TYPE_CHECKING
import asyncio
import contextlib


from core.models import db_helper, User
from core.schemas.user import UserCreate
from core.auth.user_manager import UserManager
from api.dependencies.auth.users import get_user_db
from api.dependencies.auth.user_manager import get_user_manager

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

default_email = 'admin@admin.com'
default_password = 'password'
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(user_manager: "UserManager", user_create: UserCreate) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False
    )
    return user


async def create_super_user(
    email: str = default_email,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified
):
    user_create = UserCreate(
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified
    )
    async with db_helper.session_factory() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create
                )


if __name__ == '__main__':
    asyncio.run(create_super_user())
