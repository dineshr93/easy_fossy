"""Token lifecycle, moved out of the client constructor.

``ensure_token`` runs once per client (first request), not at construction.
"""

from __future__ import annotations

import datetime
from typing import Optional

import requests

from .config import FossyConfig
from .exceptions import FossyAuthError
from .transport import check


class AuthModule:
    def __init__(self, config: FossyConfig, session: requests.Session, config_file: Optional[str] = None):
        self.config = config
        self.session = session
        self.config_file = config_file

    def ensure_token(self) -> None:
        """Attach a valid Authorization header to the session (idempotent)."""
        if self.session.headers.get("Authorization"):
            return
        token = self._cached_token()
        if token:
            self._apply(token)
            return
        self._apply(self._fetch_token())

    def _cached_token(self) -> Optional[str]:
        expire = self.config.token_expire
        if not expire or not self.config.bearer_token:
            return None
        try:
            return self.config.bearer_token if datetime.date.today() <= datetime.date.fromisoformat(expire) else None
        except ValueError:
            return None

    def _apply(self, token: str) -> None:
        self.session.headers.update({"Authorization": token})
        if token == self.config.bearer_token:
            return
        # Persist a freshly minted token only for a real ini config file.
        self.config.bearer_token = token
        self.config.token_expire = str(datetime.date.today() + datetime.timedelta(days=self.config.token_validity_days))
        if self.config_file and self.config_file != "env_config":
            self.config.save_to_ini(self.config_file)

    def _fetch_token(self) -> str:
        payload = {
            "username": self.config.uname,
            "password": self.config.pwd,
            "token_name": f"created_viaapi_on_{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
            "token_scope": self.config.access,
            "token_expire": str(datetime.date.today() + datetime.timedelta(days=self.config.token_validity_days)),
        }
        response = self.session.post(f"{self.config.url.rstrip('/')}/tokens", json=payload)
        check(response)
        token = response.json().get("Authorization")
        if not token:
            raise FossyAuthError(f"No Authorization in token response: {response.text}", response.status_code, response.text)
        return token
