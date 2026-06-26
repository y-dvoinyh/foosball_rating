from app.modules.auth.router import router


def test_auth_router_has_stable_prefix_and_tag() -> None:
    assert router.prefix == "/auth"
    assert router.tags == ["auth"]
