from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenPairResponse,
)
from app.auth.service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    authenticate_user,
    issue_refresh_token,
    register_user,
    rotate_refresh_token,
)
from app.auth.tokens import create_access_token
from app.db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    "/register",
    response_model=TokenPairResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    session: SessionDep,
) -> TokenPairResponse:
    try:
        user = await register_user(session, email=payload.email, password=payload.password)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from exc

    refresh_token = await issue_refresh_token(session, user_id=user.id)
    return TokenPairResponse(
        access_token=create_access_token(subject=str(user.id)),
        refresh_token=refresh_token.token,
    )


@router.post("/login", response_model=TokenPairResponse)
async def login(
    payload: LoginRequest,
    session: SessionDep,
) -> TokenPairResponse:
    try:
        user = await authenticate_user(session, email=payload.email, password=payload.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    refresh_token = await issue_refresh_token(session, user_id=user.id)
    return TokenPairResponse(
        access_token=create_access_token(subject=str(user.id)),
        refresh_token=refresh_token.token,
    )


@router.post("/refresh", response_model=TokenPairResponse)
async def refresh(
    payload: RefreshTokenRequest,
    session: SessionDep,
) -> TokenPairResponse:
    try:
        user, refresh_token = await rotate_refresh_token(session, token=payload.refresh_token)
    except InvalidRefreshTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenPairResponse(
        access_token=create_access_token(subject=str(user.id)),
        refresh_token=refresh_token.token,
    )
