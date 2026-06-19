from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.repository import (
    create_refresh_token_record,
    create_user,
    get_refresh_token_by_hash,
    get_user_by_email,
    get_user_by_id,
    revoke_refresh_token,
)
from app.auth.security import hash_password, verify_password
from app.auth.tokens import RefreshTokenData, create_refresh_token, hash_refresh_token


class EmailAlreadyRegisteredError(ValueError):
    pass


class InvalidCredentialsError(ValueError):
    pass


class InvalidRefreshTokenError(ValueError):
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


async def issue_refresh_token(session: AsyncSession, user_id: int) -> RefreshTokenData:
    refresh_token = create_refresh_token()
    await create_refresh_token_record(
        session=session,
        user_id=user_id,
        token_hash=refresh_token.token_hash,
        token_id=refresh_token.token_id,
        expires_at=refresh_token.expires_at,
    )
    await session.commit()
    return refresh_token


async def rotate_refresh_token(
    session: AsyncSession,
    token: str,
) -> tuple[User, RefreshTokenData]:
    current_token = await get_refresh_token_by_hash(session, hash_refresh_token(token))
    if (
        current_token is None
        or current_token.revoked_at is not None
        or current_token.expires_at <= datetime.now(UTC)
    ):
        raise InvalidRefreshTokenError

    user = await get_user_by_id(session, current_token.user_id)
    if user is None or not user.is_active:
        raise InvalidRefreshTokenError

    new_token = create_refresh_token()
    new_token_record = await create_refresh_token_record(
        session=session,
        user_id=user.id,
        token_hash=new_token.token_hash,
        token_id=new_token.token_id,
        expires_at=new_token.expires_at,
    )
    await revoke_refresh_token(
        session=session,
        refresh_token=current_token,
        replaced_by_token_id=new_token_record.id,
    )
    await session.commit()

    return user, new_token
