from typing import List, Optional, Any
from .base import Resource
from ..models import Folder

class FoldersResource(Resource):
    @property
    def base_path(self) -> str:
        return "folders"

    def get_all(self) -> List[Folder]:
        """List all folders"""
        data = self._request("GET")
        return [Folder(**f) for f in data] if isinstance(data, list) else []

    def get_by_id(self, folder_id: int) -> Folder:
        """Get folder info by ID"""
        data = self._request("GET", path=f"/{folder_id}")
        return Folder(**data) if data else None

    def create(self, parent_folder_id: int, folder_name: str):
        """Create a folder under parent"""
        payload = {"parent_folder_id": parent_folder_id, "folder_name": folder_name}
        return self._request("POST", json=payload)

    def delete(self, folder_id: int):
        """Delete a folder by ID"""
        return self._request("DELETE", path=f"/{folder_id}")
