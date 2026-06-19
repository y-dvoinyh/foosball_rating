import pytest
from fastapi.testclient import TestClient

from app.api import health as health_module


@pytest.mark.parametrize(
    ("database_available", "expected_database_status"),
    [
        (True, "ok"),
        (False, "unavailable"),
    ],
)
def test_health_returns_api_and_database_status(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    database_available: bool,
    expected_database_status: str,
) -> None:
    async def check_database_stub() -> bool:
        return database_available

    monkeypatch.setattr(health_module, "check_database", check_database_stub)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": expected_database_status,
    }
