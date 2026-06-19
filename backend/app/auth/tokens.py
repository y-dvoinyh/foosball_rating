import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
from jwt import InvalidTokenError

from app.core.config import settings

ACCESS_TOKEN_TYPE = "access"
JWT_ALGORITHM = "HS256"
REFRESH_TOKEN_BYTES = 64


class AccessTokenError(ValueError):
    pass


@dataclass(frozen=True)
class AccessTokenPayload:
    subject: str
    expires_at: datetime
    issued_at: datetime
    token_id: str


@dataclass(frozen=True)
class RefreshTokenData:
    token: str
    token_hash: str
    token_id: str
    expires_at: datetime


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(UTC)
    token_lifetime = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    expires_at = now + token_lifetime
    payload = {
        "sub": subject,
        "type": ACCESS_TOKEN_TYPE,
        "iat": now,
        "exp": expires_at,
        "jti": str(uuid4()),
    }

    return jwt.encode(payload, settings.auth_secret_key, algorithm=JWT_ALGORITHM)


def create_refresh_token() -> RefreshTokenData:
    token = secrets.token_urlsafe(REFRESH_TOKEN_BYTES)
    return RefreshTokenData(
        token=token,
        token_hash=hash_refresh_token(token),
        token_id=str(uuid4()),
        expires_at=datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days),
    )


def hash_refresh_token(token: str) -> str:
    return hmac.new(
        key=settings.auth_secret_key.encode(),
        msg=token.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()


def decode_access_token(token: str) -> AccessTokenPayload:
    try:
        payload = jwt.decode(token, settings.auth_secret_key, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError as exc:
        raise AccessTokenError("Invalid access token") from exc

    if payload.get("type") != ACCESS_TOKEN_TYPE:
        raise AccessTokenError("Invalid token type")

    subject = _get_required_string(payload, "sub")
    token_id = _get_required_string(payload, "jti")
    issued_at = _get_required_timestamp(payload, "iat")
    expires_at = _get_required_timestamp(payload, "exp")

    return AccessTokenPayload(
        subject=subject,
        expires_at=expires_at,
        issued_at=issued_at,
        token_id=token_id,
    )


def _get_required_string(payload: dict[str, Any], claim: str) -> str:
    value = payload.get(claim)
    if not isinstance(value, str) or not value:
        raise AccessTokenError(f"Missing or invalid {claim} claim")
    return value


def _get_required_timestamp(payload: dict[str, Any], claim: str) -> datetime:
    value = payload.get(claim)
    if not isinstance(value, int | float):
        raise AccessTokenError(f"Missing or invalid {claim} claim")
    return datetime.fromtimestamp(value, UTC)
