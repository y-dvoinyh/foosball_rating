from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.auth.tokens import decode_access_token


@pytest.fixture
def email_prefix() -> str:
    return f"auth_it_{uuid4().hex}"


def test_register_returns_access_token(
    client: TestClient,
    email_prefix: str,
) -> None:
    response = client.post(
        "/auth/register",
        json={"email": f"{email_prefix}@example.com", "password": "correct-password"},
    )

    assert response.status_code == 201
    response_body = response.json()
    assert response_body["token_type"] == "bearer"

    token_payload = decode_access_token(response_body["access_token"])
    assert token_payload.subject.isdigit()


def test_register_normalizes_email_for_later_login(
    client: TestClient,
    email_prefix: str,
) -> None:
    email = f"{email_prefix}@example.com"
    password = "correct-password"

    register_response = client.post(
        "/auth/register",
        json={"email": f"  {email.upper()}  ", "password": password},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert register_response.status_code == 201
    assert login_response.status_code == 200
    assert decode_access_token(login_response.json()["access_token"]).subject == (
        decode_access_token(register_response.json()["access_token"]).subject
    )


def test_register_rejects_duplicate_email(
    client: TestClient,
    email_prefix: str,
) -> None:
    email = f"{email_prefix}@example.com"
    payload = {"email": email, "password": "correct-password"}

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {"detail": "Email is already registered"}


def test_login_returns_access_token_for_valid_credentials(
    client: TestClient,
    email_prefix: str,
) -> None:
    email = f"{email_prefix}@example.com"
    password = "correct-password"
    register_response = client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )

    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert register_response.status_code == 201
    assert response.status_code == 200
    assert decode_access_token(response.json()["access_token"]).subject == (
        decode_access_token(register_response.json()["access_token"]).subject
    )


def test_login_rejects_invalid_password(
    client: TestClient,
    email_prefix: str,
) -> None:
    email = f"{email_prefix}@example.com"
    register_response = client.post(
        "/auth/register",
        json={"email": email, "password": "correct-password"},
    )

    response = client.post(
        "/auth/login",
        json={"email": email, "password": "wrong-password"},
    )

    assert register_response.status_code == 201
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Invalid email or password"}


def test_login_rejects_unknown_email(
    client: TestClient,
    email_prefix: str,
) -> None:
    response = client.post(
        "/auth/login",
        json={"email": f"{email_prefix}@example.com", "password": "correct-password"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Invalid email or password"}
