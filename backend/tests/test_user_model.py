from app.auth.models import User
from app.models.base import Base


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
