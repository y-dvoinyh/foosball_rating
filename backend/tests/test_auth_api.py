from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.modules.auth.tokens import create_access_token, decode_access_token


@pytest.fixture
def email_prefix() -> str:
    return f"auth_it_{uuid4().hex}"


@pytest.fixture(autouse=True)
def clear_client_cookies(client: TestClient) -> None:
    client.cookies.clear()


def test_register_returns_access_token_and_sets_refresh_cookie(
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
    assert "refresh_token" not in response_body
    assert response.cookies.get("refresh_token")
    assert response.cookies.get("auth_session") == "1"
    assert "HttpOnly" in response.headers["set-cookie"]
    assert "SameSite=lax" in response.headers["set-cookie"]

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
    assert "refresh_token" not in response.json()
    assert response.cookies.get("refresh_token")
    assert response.cookies.get("auth_session") == "1"
    assert decode_access_token(response.json()["access_token"]).subject == (
        decode_access_token(register_response.json()["access_token"]).subject
    )


def test_oauth_token_endpoint_returns_token_pair_for_swagger_authorize(
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
        "/auth/token",
        data={"username": email, "password": password},
    )

    assert register_response.status_code == 201
    assert response.status_code == 200
    assert "refresh_token" not in response.json()
    assert response.cookies.get("refresh_token")
    assert response.cookies.get("auth_session") == "1"
    assert decode_access_token(response.json()["access_token"]).subject == (
        decode_access_token(register_response.json()["access_token"]).subject
    )


def test_openapi_oauth_token_url_is_relative_for_nginx_root_path(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert (
        response.json()["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"][
            "password"
        ]["tokenUrl"]
        == "auth/token"
    )


def test_refresh_rotates_refresh_token(
    client: TestClient,
    email_prefix: str,
) -> None:
    email = f"{email_prefix}@example.com"
    register_response = client.post(
        "/auth/register",
        json={"email": email, "password": "correct-password"},
    )
    old_refresh_token = register_response.cookies.get("refresh_token")

    refresh_response = client.post("/auth/refresh")

    assert refresh_response.status_code == 200
    assert refresh_response.cookies.get("refresh_token") != old_refresh_token
    assert refresh_response.cookies.get("auth_session") == "1"
    assert decode_access_token(refresh_response.json()["access_token"]).subject == (
        decode_access_token(register_response.json()["access_token"]).subject
    )

    assert old_refresh_token is not None
    client.cookies.set("refresh_token", old_refresh_token)
    old_token_response = client.post("/auth/refresh")
    assert old_token_response.status_code == 401
    assert old_token_response.json() == {"detail": "Invalid refresh token"}


def test_refresh_rejects_missing_refresh_cookie(client: TestClient) -> None:
    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Invalid refresh token"}


def test_refresh_rejects_unknown_refresh_cookie(client: TestClient) -> None:
    client.cookies.set(
        "refresh_token",
        "unknown-refresh-token-value-that-is-long-enough",
    )

    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Invalid refresh token"}


def test_refresh_ignores_refresh_token_body_without_cookie(client: TestClient) -> None:
    old_token_response = client.post(
        "/auth/refresh",
        json={"refresh_token": "unknown-refresh-token-value-that-is-long-enough"},
    )

    assert old_token_response.status_code == 401
    assert old_token_response.json() == {"detail": "Invalid refresh token"}


def test_logout_revokes_refresh_cookie(
    client: TestClient,
    email_prefix: str,
) -> None:
    client.post(
        "/auth/register",
        json={
            "email": f"{email_prefix}@example.com",
            "password": "correct-password",
        },
    )

    logout_response = client.post("/auth/logout")
    refresh_response = client.post("/auth/refresh")

    assert logout_response.status_code == 204
    assert logout_response.content == b""
    assert "refresh_token=" in logout_response.headers["set-cookie"]
    assert "auth_session=" in logout_response.headers["set-cookie"]
    assert refresh_response.status_code == 401
    assert refresh_response.json() == {"detail": "Invalid refresh token"}


def test_logout_rejects_missing_refresh_cookie(client: TestClient) -> None:
    response = client.post("/auth/logout")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Invalid refresh token"}


def test_me_returns_current_user(
    client: TestClient,
    email_prefix: str,
) -> None:
    email = f"{email_prefix}@example.com"
    register_response = client.post(
        "/auth/register",
        json={"email": email, "password": "correct-password"},
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {register_response.json()['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": int(decode_access_token(register_response.json()["access_token"]).subject),
        "email": email,
        "is_active": True,
        "is_superuser": False,
    }


def test_me_rejects_missing_access_token(client: TestClient) -> None:
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Not authenticated"}


def test_me_rejects_invalid_access_token(client: TestClient) -> None:
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Could not validate credentials"}


def test_me_rejects_token_for_unknown_user(client: TestClient) -> None:
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {create_access_token(subject='999999999')}"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Could not validate credentials"}


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
