"""Offline test doubles: a stub session and a client wired to it.

The transport seam is the only thing tests need to swap: resources read
``client.transport``, so replacing ``transport.session`` and clearing
``transport.auth`` makes the whole library run with zero network.
"""

import json as _json

from easy_fossy.client import FossyClient
from easy_fossy.config import FossyConfig
from easy_fossy.exceptions import FossyAPIError


class StubResponse:
    def __init__(self, status=200, body=None, text="", content=b"", headers=None):
        self.status_code = status
        self._body = body
        self.text = text if text else (_json.dumps(body) if body is not None else "")
        self.content = content if content else self.text.encode()
        self.headers = headers or {}

    def json(self):
        return self._body


class StubSession:
    """Answers by ``(METHOD, path)``; a list value is consumed call by call."""

    def __init__(self, routes=None, base="http://stub/api/v1"):
        self.routes = routes or {}
        self.base = base
        self.calls = []
        self.headers = {}

    def request(self, method, url, params=None, headers=None, json=None, data=None, timeout=None):
        path = url[len(self.base):].lstrip("/")
        self.calls.append({"method": method, "path": path, "params": params, "headers": headers, "json": json, "data": data})
        entry = self.routes.get((method, path), self.routes.get((method, "*")))
        if entry is None:
            raise AssertionError(f"unstubbed route {method} {path}; stubbed: {sorted(self.routes)}")
        if isinstance(entry, list):
            return entry.pop(0) if len(entry) > 1 else entry[0]
        return entry

    def get(self, url, headers=None, **kw):
        return self.request("GET", url, headers=headers, **kw)

    def post(self, url, data=None, json=None, headers=None, **kw):
        return self.request("POST", url, headers=headers, data=data, json=json, **kw)


def make_client(routes=None):
    """A FossyClient with no auth module and a stub session (no network)."""
    client = FossyClient(None, config_override=FossyConfig(url="http://stub/api/v1/"))
    session = StubSession(routes, base="http://stub/api/v1")
    client.transport.session = session
    client.transport.auth = None
    return client, session

def reaches_server(fn):
    """Run fn; a returned value or any FossyAPIError (domain response) proves the
    endpoint is wired. Network-level errors (FossyConnectionError) still fail."""
    try:
        return fn() is not None
    except FossyAPIError:
        return True
