"""Base resource: one URL rule, one request helper, no escape hatches.

A resource owns exactly the endpoints under its ``base_path``. When it needs an
endpoint owned by another resource, it calls that resource's interface.
"""

from typing import Any, Optional

from ..config import FossyConfig
from ..transport import check


class Resource:
    def __init__(self, client):
        self.client = client
        self.config: FossyConfig = client.config

    @property
    def transport(self):
        """Read through the client so a swapped transport (tests) takes effect."""
        return self.client.transport

    @property
    def base_path(self) -> str:
        """Override this in subclasses to define the resource endpoint"""
        return ""

    def _send(self, method: str, path: str = "", **kwargs):
        """Send a request owned by this resource and return the raw response."""
        relative = f"{self.base_path}/{path.lstrip('/')}" if path else self.base_path
        return self.transport.request(method, relative, **kwargs)

    def _request(self, method: str, path: str = "", params: Optional[dict] = None, json: Any = None, headers: Optional[dict] = None) -> Any:
        """Send a request and decode a JSON body; raises the domain exception on failure.

        An empty body (204, or a 200 with no content) decodes to ``None`` rather
        than raising a JSON error.
        """
        response = check(self._send(method, path, params=params, json=json, headers=headers))
        return response.json() if response.content else None
