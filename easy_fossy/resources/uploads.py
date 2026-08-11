import time
from typing import List, Optional, Any
from .base import Resource
from ..models import Upload, UploadSummary, Info, Copyright, LicenseCount
from ..exceptions import FossyAPIError

class UploadsResource(Resource):
    @property
    def base_path(self) -> str:
        return "uploads"

    def _wait_for_upload(self, upload_id: int, timeout: float = 90.0, poll_interval: float = 3.0) -> Optional[Upload]:
        """The POST /uploads endpoint returns the upload id immediately, but the
        ununpack job may not have started yet (GET /uploads/{id} returns 503 until
        it does). Poll until the upload becomes readable or we hit the timeout.
        """
        deadline = time.time() + timeout
        last_err = None
        while time.time() < deadline:
            try:
                return self.get_upload_by_id(upload_id=upload_id)
            except FossyAPIError as e:
                last_err = e
                if e.status_code != 503:
                    raise
            time.sleep(poll_interval)
        raise FossyAPIError(
            f"Upload {upload_id} never became available before timeout",
            status_code=None, response_text=str(last_err),
        )

    def upload_file(self, file_path: str, folder_id: int) -> Optional[Upload]:
        """Upload a local file.
        FOSSology contract: POST /uploads (multipart), folderId + uploadType=file headers,
        file field named ``fileInput``. Response is an Info payload: {code, message=<upload_id>}.
        """
        import requests
        from requests_toolbelt.multipart.encoder import MultipartEncoder

        file_name = file_path.split("/")[-1]
        fields = {
            "fileInput": (file_name, open(file_path, "rb"), None)
        }
        m = MultipartEncoder(fields=fields)

        headers = {
            "Content-Type": m.content_type,
            "folderId": str(folder_id),
            "uploadType": "file",
        }
        response = self.session.post(
            f"{self.client.url}{self.base_path}",
            data=m,
            headers=headers
        )

        if response.status_code in (200, 201):
            data = response.json()
            upload_id = data.get("message") if isinstance(data, dict) else None
            if upload_id is not None:
                return self._wait_for_upload(upload_id=int(upload_id))
        return None

    def upload_by_url(self, url: str, folder_id: int, scan_options: Optional[dict] = None) -> Optional[Upload]:
        """Upload a package from a URL.
        FOSSology contract: folderId + uploadType headers are required, and the
        JSON body must wrap the URL in a ``location`` object. If ``scan_options``
        is provided, the analysis agents are scheduled at upload time.
        """
        headers = {
            "folderId": str(folder_id),
            "uploadType": "url",
        }
        payload = {"location": {"url": url}}
        if scan_options:
            payload["scanOptions"] = scan_options
        data = self._request("POST", path="", headers=headers, json=payload)
        # POST /uploads returns an Info payload: {"code": 201, "message": <upload_id>, "type": "INFO"}
        upload_id = data.get("message") if isinstance(data, dict) else None
        if upload_id is None:
            return None
        return self._wait_for_upload(upload_id=int(upload_id))

    def upload_by_giturl(self, giturl: str, folder_id: int, branch: Optional[str] = None) -> Optional[Upload]:
        """Upload a package from a Git URL.
        FOSSology contract: POST /uploads with folderId + uploadType=vcs headers and a
        ``location`` body containing a VcsUpload (vcsType=git, vcsUrl=...).
        """
        headers = {
            "folderId": str(folder_id),
            "uploadType": "vcs",
        }
        location = {"vcsType": "git", "vcsUrl": giturl}
        if branch:
            location["vcsBranch"] = branch
        payload = {"location": location}
        data = self._request("POST", path="", headers=headers, json=payload)
        upload_id = data.get("message") if isinstance(data, dict) else None
        if upload_id is None:
            return None
        return self._wait_for_upload(upload_id=int(upload_id))

    def get_upload_by_id(self, upload_id: int) -> Optional[Upload]:
        """Get upload details by ID"""
        data = self._request("GET", path=f"/{upload_id}")
        return Upload(**data) if data else None

    def get_all_uploads(self, folder_id: Optional[int] = None, page: int = 1, limit: int = 100) -> List[Upload]:
        """List all uploads. FOSSology contract: GET /uploads.
        ``folder_id`` limits uploads to a folder; page/limit are sent as headers.
        """
        headers = {"page": str(page), "limit": str(limit)}
        params = {}
        if folder_id is not None:
            params["folderId"] = str(folder_id)
        data = self._request("GET", params=params, headers=headers)
        return [Upload(**u) for u in data] if isinstance(data, list) else []

    def trigger_analysis_for_upload_id(self, upload_id: int, folder_id: int):
        """Schedule a full analysis for an upload.
        FOSSology contract: POST /jobs with folderId + uploadId headers and a
        ScanOptions body (analysis agents). Returns the Info payload holding the
        scheduled job id in ``message``.
        """
        headers = {
            "folderId": str(folder_id),
            "uploadId": str(upload_id),
        }
        payload = {
            "analysis": {
                "nomos": True,
                "monk": True,
                "copyright_email_author": True,
                "mime": True,
                "keyword": True,
                "bucket": True,
            }
        }
        # POST /jobs is relative to the API root, not the uploads base_path.
        return self._request("POST", path="jobs", headers=headers, json=payload, absolute_path=True)

    def delete_uploads_by_upload_id(self, upload_id: int):
        """Delete upload"""
        return self._request("DELETE", path=f"/{upload_id}")

    def get_upload_tree_id_by_upload_id(self, upload_id: int) -> Info:
        """Get the upload_tree_id for an upload"""
        data = self._request("GET", path=f"/{upload_id}/topitem")
        return Info(**data) if data else None

    def get_copyrights_by_upload_id_uploadtree_id(self, upload_id: int, upload_tree_id: int) -> List[Copyright]:
        """Get copyrights for a specific item in upload.
        FOSSology contract: GET /uploads/{id}/item/{itemId}/copyrights?status=active
        """
        params = {"status": "active"}
        data = self._request("GET", path=f"/{upload_id}/item/{upload_tree_id}/copyrights", params=params)
        return [Copyright(**c) for c in data] if isinstance(data, list) else []
