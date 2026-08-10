from typing import Any, Optional
import requests
from ..config import FossyConfig
from ..exceptions import FossyAPIError, FossyAuthError, FossyConnectionError

class Resource:
    def __init__(self, client):
        self.client = client
        self.config: FossyConfig = client.config
        self.session = client.session

    @property
    def base_path(self) -> str:
        """Override this in subclasses to define the resource endpoint"""
        return ""

    def _request(self, method: str, path: str = "", params: Optional[dict] = None, data: Any = None, json: Any = None, **kwargs) -> Any:
        url = f"{self.client.url}{self.base_path}/{path}"
        if url.endswith("/"):
            url = url[:-1]

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code in (401, 403):
                raise FossyAuthError(f"Authentication failed: {e.response.text}", status_code, e.response.text)
            raise FossyAPIError(f"API request failed: {e.response.text}", status_code, e.response.text)
        except requests.exceptions.RequestException as e:
            raise FossyConnectionError(f"Connection error: {str(e)}")
