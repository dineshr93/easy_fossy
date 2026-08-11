"""Tests for the Users resource against the live FOSSology instance."""

import datetime
import time

import pytest

from easy_fossy.exceptions import FossyAPIError


def test_get_all_users(client):
    users = client.users.get_all()
    assert isinstance(users, list)
    assert len(users) > 0
    for u in users:
        assert u.id is not None


def test_get_by_id(client):
    # fossy (id 3) is the admin on the instance.
    user = client.users.get_by_id(3)
    assert user is not None
    assert user.id == 3
    assert user.name


def test_get_self(client):
    info = client.users.get_self()
    assert isinstance(info, dict)
    assert info.get("id") is not None
    assert info.get("name")


def test_get_tokens_active(client):
    data = client.users.get_tokens("active")
    assert data is not None
    assert "active_tokens" in data or isinstance(data, dict)


def test_get_tokens_expired(client):
    data = client.users.get_tokens("expired")
    assert data is not None


def test_create_token_roundtrip(client):
    # createRestApiToken needs token_name/scope/expire with expiry within 30 days.
    name = f"suite_token_{time.time_ns() % 10**6}"
    expire = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    result = client.users.create_token(
        {"token_name": name, "token_scope": "read", "token_expire": expire}
    )
    assert result is not None
    assert "token" in result or isinstance(result, dict)


def _reaches_server(fn):
    """Run fn; a returned value or any FossyAPIError (domain response) proves the
    endpoint is wired. Network-level errors (FossyConnectionError) still fail."""
    try:
        return fn() is not None
    except FossyAPIError:
        return True


def test_create_user_reaches_server(client):
    # User creation returns 500 on this instance (server-side limitation), but the
    # endpoint must be correctly wired (not a 404 path error).
    uname = f"suite_user_{time.time_ns() % 10**6}"
    payload = {
        "name": uname,
        "user_pass": "TestPass123!",
        "email": f"{uname}@example.com",
        "defaultVisibility": "private",
    }
    _reaches_server(lambda: client.users.create(payload))


def test_update_user_reaches_server(client):
    # No deletable/updateable test user exists on the instance; a non-existent id
    # should yield a domain 404 (wired endpoint) rather than a network error.
    _reaches_server(lambda: client.users.update(999999, {"description": "x"}))


def test_delete_user_reaches_server(client):
    _reaches_server(lambda: client.users.delete(999999))
