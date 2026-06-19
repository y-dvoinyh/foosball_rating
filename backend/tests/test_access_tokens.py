from datetime import timedelta

import jwt
import pytest

from app.auth.tokens import (
    ACCESS_TOKEN_TYPE,
    JWT_ALGORITHM,
    AccessTokenError,
    create_access_token,
    decode_access_token,
)
from app.core.config import settings


def test_create_access_token_can_be_decoded() -> None:
    token = create_access_token(subject="42")

    payload = decode_access_token(token)

    assert payload.subject == "42"
    assert payload.token_id
    assert payload.expires_at > payload.issued_at


def test_access_token_contains_expected_jwt_claims() -> None:
    token = create_access_token(subject="42")

    raw_payload = jwt.decode(token, settings.auth_secret_key, algorithms=[JWT_ALGORITHM])

    assert raw_payload["sub"] == "42"
    assert raw_payload["type"] == ACCESS_TOKEN_TYPE
    assert raw_payload["jti"]
    assert raw_payload["exp"] > raw_payload["iat"]


def test_create_access_token_uses_unique_token_id() -> None:
    first_token = create_access_token(subject="42")
    second_token = create_access_token(subject="42")

    first_payload = decode_access_token(first_token)
    second_payload = decode_access_token(second_token)

    assert first_payload.token_id != second_payload.token_id


def test_decode_access_token_rejects_expired_token() -> None:
    token = create_access_token(subject="42", expires_delta=timedelta(seconds=-1))

    with pytest.raises(AccessTokenError):
        decode_access_token(token)


def test_decode_access_token_rejects_refresh_token_type() -> None:
    token = jwt.encode(
        {
            "sub": "42",
            "type": "refresh",
            "iat": 1,
            "exp": 2_000_000_000,
            "jti": "token-id",
        },
        settings.auth_secret_key,
        algorithm=JWT_ALGORITHM,
    )

    with pytest.raises(AccessTokenError, match="Invalid token type"):
        decode_access_token(token)


def test_decode_access_token_rejects_wrong_secret() -> None:
    token = jwt.encode(
        {
            "sub": "42",
            "type": ACCESS_TOKEN_TYPE,
            "iat": 1,
            "exp": 2_000_000_000,
            "jti": "token-id",
        },
        "wrong-secret",
        algorithm=JWT_ALGORITHM,
    )

    with pytest.raises(AccessTokenError):
        decode_access_token(token)
