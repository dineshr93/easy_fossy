"""The transport seam: URL rule, status mapping, lazy auth, pure construction."""

import pytest
import requests

from easy_fossy.client import FossyClient
from easy_fossy.config import FossyConfig
from easy_fossy.exceptions import FossyAPIError, FossyAuthError, FossyConnectionError

from stub import StubResponse, make_client


def test_url_join_has_no_double_or_trailing_slash():
    client, session = make_client({("GET", "folders/3"): StubResponse(200, {"id": 3, "name": "root"})})
    client.folders.get_by_id(3)
    assert session.calls[0]["path"] == "folders/3"
    assert session.calls[0]["path"].count("//") == 0


def test_empty_path_hits_the_resource_root_once():
    client, session = make_client({("GET", "users"): StubResponse(200, [])})
    client.users.get_all()
    assert session.calls[0]["path"] == "users"


def test_check_maps_403_to_auth_error():
    client, _ = make_client({("GET", "users/1"): StubResponse(403, {"message": "nope"}, text="nope")})
    with pytest.raises(FossyAuthError) as e:
        client.users.get_by_id(1)
    assert e.value.status_code == 403


def test_check_maps_500_to_api_error():
    client, _ = make_client({("GET", "users/1"): StubResponse(500, text="boom")})
    with pytest.raises(FossyAPIError) as e:
        client.users.get_by_id(1)
    assert e.value.status_code == 500


def test_network_failure_is_a_connection_error():
    class DeadSession:
        headers = {}

        def request(self, **kw):
            raise requests.ConnectionError("refused")

    client = FossyClient(None, config_override=FossyConfig(url="http://stub/api/v1/"))
    client.transport.session = DeadSession()
    client.transport.auth = None
    with pytest.raises(FossyConnectionError):
        client.users.get_all()


def test_construction_performs_no_request(monkeypatch):
    def bomb(*a, **kw):
        raise AssertionError("constructor must not touch the network")

    monkeypatch.setattr(requests.Session, "request", bomb)
    client = FossyClient(None, config_override=FossyConfig(url="http://stub/api/v1/"))
    assert client.transport.auth is not None          # auth wired, not run
    assert "Authorization" not in client.session.headers


def test_auth_is_ensured_once_on_first_request():
    calls = []

    class CountingAuth:
        def ensure_token(self):
            calls.append(1)

    client, session = make_client({("GET", "users"): StubResponse(200, [])})
    client.transport.auth = CountingAuth()
    client.users.get_all()
    client.users.get_all()
    assert len(calls) == 2      # hook called per request, token work is idempotent inside it
    assert len(session.calls) == 2
