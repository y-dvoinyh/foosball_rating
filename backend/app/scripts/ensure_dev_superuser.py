import asyncio

from sqlalchemy.exc import IntegrityError

from app.auth.models import User
from app.auth.repository import get_user_by_email
from app.auth.security import hash_password
from app.core.config import settings
from app.db.session import async_session_factory, engine


async def ensure_dev_superuser() -> None:
    email = settings.dev_superuser_email.strip().lower()
    password = settings.dev_superuser_password

    if not email or not password:
        raise RuntimeError(
            "DEV_SUPERUSER_EMAIL and DEV_SUPERUSER_PASSWORD must be set",
        )

    async with async_session_factory() as session:
        user = await get_user_by_email(session, email)
        if user is None:
            user = User(
                email=email,
                password_hash=hash_password(password),
                is_active=True,
                is_superuser=True,
            )
            session.add(user)
            action = "created"
        else:
            user.is_superuser = True
            session.add(user)
            action = "updated"

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise

    print(f"Dev superuser {action}: {email}")


async def main() -> None:
    try:
        await ensure_dev_superuser()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
