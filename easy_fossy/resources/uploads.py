from typing import List, Optional, Any
from .base import Resource
from ..models import Upload, UploadSummary, Info, Copyright, LicenseCount

class UploadsResource(Resource):
    @property
    def base_path(self) -> str:
        return "uploads"

    def upload_file(self, file_path: str, folder_id: int) -> Optional[Upload]:
        """Upload a local file"""
        # Note: multipart upload requires special handling in _request or here
        # For now, we'll implement the logic directly using requests since it's complex
        import requests
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        
        fields = {
            "folder_id": str(folder_id),
            "file": (None, open(file_path, "rb"), None)
        }
        m = MultipartEncoder(fields=fields)
        
        response = self.session.post(
            f"{self.client.url}{self.base_path}/",
            data=m,
            headers={"Content-Type": m.content_type}
        )
        
        if response.status_code == 200:
            return Upload(**response.json())
        return None

    def get_upload_by_id(self, upload_id: int) -> Optional[Upload]:
        """Get upload details by ID"""
        data = self._request("GET", path=f"/{upload_id}")
        return Upload(**data) if data else None

    def trigger_analysis_for_upload_id(self, upload_id: int, folder_id: int):
        """Trigger full analysis"""
        payload = {"upload_id": upload_id, "folder_id": folder_id}
        return self._request("POST", path="/trigger_analysis", json=payload)

    def delete_uploads_by_upload_id(self, upload_id: int):
        """Delete upload"""
        return self._request("DELETE", path=f"/{upload_id}")

    def get_upload_tree_id_by_upload_id(self, upload_id: int) -> Info:
        """Get the upload_tree_id for an upload"""
        data = self._request("GET", path=f"/{upload_id}/topitem")
        return Info(**data) if data else None

    def get_copyrights_by_upload_id_uploadtree_id(self, upload_id: int, upload_tree_id: int) -> List[Copyright]:
        """Get copyrights for a specific item in upload"""
        data = self._request("GET", path=f"/{upload_id}/item/{upload_tree_id}/copyrights")
        return [Copyright(**c) for c in data] if isinstance(data, list) else []
