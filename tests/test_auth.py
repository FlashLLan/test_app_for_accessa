import pytest

from app import auth


@pytest.fixture(autouse=True)
def token_env(monkeypatch):
    monkeypatch.setenv("INVENTORY_API_TOKEN", "test-token")


def test_admin_can_delete():
    auth.authorize_delete("test-token", "admin")


def test_viewer_can_delete():
    auth.authorize_delete("test-token", "viewer")


def test_bad_token_rejected():
    with pytest.raises(auth.AuthError):
        auth.authorize_delete("wrong", "admin")
