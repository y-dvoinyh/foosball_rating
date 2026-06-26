from app.models.base import Base
from app.modules.auth.models import RefreshToken, User


def test_user_model_is_registered_in_metadata() -> None:
    assert User.__table__ is Base.metadata.tables["users"]


def test_user_model_has_minimal_auth_columns() -> None:
    columns = User.__table__.columns

    assert set(columns.keys()) == {
        "id",
        "email",
        "password_hash",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    }
    assert columns["email"].unique is True
    assert columns["email"].nullable is False
    assert columns["password_hash"].nullable is False


def test_refresh_token_model_is_registered_in_metadata() -> None:
    assert RefreshToken.__table__ is Base.metadata.tables["refresh_tokens"]


def test_refresh_token_model_has_rotation_columns() -> None:
    columns = RefreshToken.__table__.columns

    assert set(columns.keys()) == {
        "id",
        "user_id",
        "token_hash",
        "jti",
        "expires_at",
        "revoked_at",
        "replaced_by_token_id",
        "created_at",
    }
    assert columns["token_hash"].unique is True
    assert columns["jti"].unique is True
    assert columns["revoked_at"].nullable is True
    assert columns["replaced_by_token_id"].nullable is True
