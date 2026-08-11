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

    def create(self, parent_folder_id: int, folder_name: str, folder_description: Optional[str] = None):
        """Create a folder under parent.
        FOSSology passes parentFolder/folderName/folderDescription as custom headers.
        """
        headers = {
            "parentFolder": str(parent_folder_id),
            "folderName": folder_name,
        }
        if folder_description:
            headers["folderDescription"] = folder_description
        return self._request("POST", headers=headers)

    def delete(self, folder_id: int):
        """Delete a folder by ID"""
        return self._request("DELETE", path=f"/{folder_id}")

    def update(self, folder_id: int, folder_name: str, folder_desc: str):
        """Update folder name or description.
        FOSSology contract: PATCH /folders/{id} with name/description headers.
        """
        headers = {"name": folder_name, "description": folder_desc}
        return self._request("PATCH", path=f"/{folder_id}", headers=headers)

    def move(self, folder_id: int, target_folder_id: int):
        """Move folder to target parent.
        FOSSology contract: PUT /folders/{id} with parent + action headers.
        """
        headers = {"parent": str(target_folder_id), "action": "move"}
        return self._request("PUT", path=f"/{folder_id}", headers=headers)

    def unlink_content(self, content_id: int):
        """Unlink content from folder"""
        return self._request("PUT", path=f"/contents/{content_id}/unlink")

    def get_contents(self, folder_id: int) -> List[Any]:
        """Get all folder contents"""
        data = self._request("GET", path=f"/{folder_id}/contents")
        return data if isinstance(data, list) else []

    def get_unlinkable_contents(self, folder_id: int) -> List[Any]:
        """Get unlinkable contents"""
        data = self._request("GET", path=f"/{folder_id}/contents/unlinkable")
        return data if isinstance(data, list) else []
