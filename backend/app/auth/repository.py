from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import RefreshToken, User


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, email: str, password_hash: str) -> User:
    user = User(email=email, password_hash=password_hash)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_refresh_token_record(
    session: AsyncSession,
    user_id: int,
    token_hash: str,
    token_id: str,
    expires_at: datetime,
) -> RefreshToken:
    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        jti=token_id,
        expires_at=expires_at,
    )
    session.add(refresh_token)
    await session.flush()
    await session.refresh(refresh_token)
    return refresh_token


async def get_refresh_token_by_hash(
    session: AsyncSession,
    token_hash: str,
) -> RefreshToken | None:
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    )
    return result.scalar_one_or_none()


async def revoke_refresh_token(
    session: AsyncSession,
    refresh_token: RefreshToken,
    replaced_by_token_id: int | None = None,
) -> None:
    refresh_token.revoked_at = datetime.now(UTC)
    refresh_token.replaced_by_token_id = replaced_by_token_id
    session.add(refresh_token)
