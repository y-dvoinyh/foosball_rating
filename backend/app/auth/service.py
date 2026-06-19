from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.repository import create_user, get_user_by_email
from app.auth.security import hash_password, verify_password


class EmailAlreadyRegisteredError(ValueError):
    pass


class InvalidCredentialsError(ValueError):
    pass


async def register_user(session: AsyncSession, email: str, password: str) -> User:
    existing_user = await get_user_by_email(session, email)
    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    try:
        user = await create_user(
            session=session,
            email=email,
            password_hash=hash_password(password),
        )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise EmailAlreadyRegisteredError from exc

    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(session, email)
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError

    return user
