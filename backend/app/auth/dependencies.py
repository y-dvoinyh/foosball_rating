from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.repository import get_user_by_id
from app.auth.tokens import AccessTokenError, decode_access_token
from app.db.session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
    token: TokenDep,
    session: SessionDep,
) -> User:
    unauthorized_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_payload = decode_access_token(token)
        user_id = int(token_payload.subject)
    except (AccessTokenError, ValueError) as exc:
        raise unauthorized_error from exc

    user = await get_user_by_id(session, user_id)
    if user is None or not user.is_active:
        raise unauthorized_error

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
