from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentUserDep
from app.auth.schemas import (
    AccessTokenResponse,
    CurrentUserResponse,
    LoginRequest,
    RegisterRequest,
)
from app.auth.service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    authenticate_user,
    issue_refresh_token,
    logout_refresh_token,
    register_user,
    rotate_refresh_token,
)
from app.auth.tokens import create_access_token
from app.core.config import settings
from app.db.session import get_session

REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
REFRESH_TOKEN_COOKIE_PATH = "/"

router = APIRouter(prefix="/auth", tags=["auth"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
OAuth2PasswordFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
RefreshTokenCookieDep = Annotated[
    str | None,
    Cookie(alias=REFRESH_TOKEN_COOKIE_NAME),
]


@router.get("/me", response_model=CurrentUserResponse)
async def me(current_user: CurrentUserDep) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
    )


@router.post(
    "/register",
    response_model=AccessTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    response: Response,
    session: SessionDep,
) -> AccessTokenResponse:
    try:
        user = await register_user(session, email=payload.email, password=payload.password)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from exc

    refresh_token = await issue_refresh_token(session, user_id=user.id)
    set_refresh_token_cookie(response, refresh_token.token)
    return AccessTokenResponse(access_token=create_access_token(subject=str(user.id)))


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    session: SessionDep,
) -> AccessTokenResponse:
    return await issue_token_pair(
        response=response,
        session=session,
        email=payload.email,
        password=payload.password,
    )


@router.post("/token", response_model=AccessTokenResponse, include_in_schema=False)
async def token(
    form_data: OAuth2PasswordFormDep,
    response: Response,
    session: SessionDep,
) -> AccessTokenResponse:
    return await issue_token_pair(
        response=response,
        session=session,
        email=form_data.username,
        password=form_data.password,
    )


async def issue_token_pair(
    response: Response,
    session: AsyncSession,
    email: str,
    password: str,
) -> AccessTokenResponse:
    try:
        user = await authenticate_user(session, email=email.strip().lower(), password=password)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    refresh_token = await issue_refresh_token(session, user_id=user.id)
    set_refresh_token_cookie(response, refresh_token.token)
    return AccessTokenResponse(access_token=create_access_token(subject=str(user.id)))


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    response: Response,
    session: SessionDep,
    refresh_token_cookie: RefreshTokenCookieDep = None,
) -> AccessTokenResponse:
    try:
        if refresh_token_cookie is None:
            raise InvalidRefreshTokenError
        user, refresh_token = await rotate_refresh_token(session, token=refresh_token_cookie)
    except InvalidRefreshTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    set_refresh_token_cookie(response, refresh_token.token)
    return AccessTokenResponse(access_token=create_access_token(subject=str(user.id)))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    session: SessionDep,
    refresh_token_cookie: RefreshTokenCookieDep = None,
) -> None:
    try:
        if refresh_token_cookie is None:
            raise InvalidRefreshTokenError
        await logout_refresh_token(session, token=refresh_token_cookie)
    except InvalidRefreshTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    finally:
        clear_refresh_token_cookie(response)


def set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=settings.refresh_token_cookie_secure,
        samesite="lax",
        path=REFRESH_TOKEN_COOKIE_PATH,
    )


def clear_refresh_token_cookie(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        path=REFRESH_TOKEN_COOKIE_PATH,
        httponly=True,
        secure=settings.refresh_token_cookie_secure,
        samesite="lax",
    )
