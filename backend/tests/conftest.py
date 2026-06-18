from collections.abc import Generator

from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
