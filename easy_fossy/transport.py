"""The one module that owns URL building, status mapping and the auth hook.

Resources ask it for a ``requests.Response`` and decide how to read the body
(json, text, bytes); ``check`` is the single place that turns a status code
into a domain exception.
"""

from __future__ import annotations

from typing import Any, Optional

import requests

from .exceptions import FossyAPIError, FossyAuthError, FossyConnectionError


class Transport:
    def __init__(self, base_url: str, session: requests.Session, auth=None):
        self.base_url = base_url.rstrip("/")
        self.session = session
        # Set to an AuthModule to fetch/set the bearer token lazily; None means
        # the session already carries its Authorization header (tests).
        self.auth = auth

    def request(
        self,
        method: str,
        path: str = "",
        *,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        json: Any = None,
        data: Any = None,
        timeout: Optional[float] = None,
    ) -> requests.Response:
        """Send one request. Raises only FossyConnectionError (network-level)."""
        if self.auth is not None:
            self.auth.ensure_token()
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        try:
            return self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json,
                data=data,
                timeout=timeout,
            )
        except requests.exceptions.RequestException as e:
            raise FossyConnectionError(f"Connection error: {e}") from e


def check(response: requests.Response) -> requests.Response:
    """Return the response when it is a success, else raise the domain exception."""
    status = response.status_code
    if status < 400:
        return response
    text = response.text
    if status in (401, 403):
        raise FossyAuthError(f"Authentication failed: {text}", status, text)
    raise FossyAPIError(f"API request failed: {text}", status, text)
