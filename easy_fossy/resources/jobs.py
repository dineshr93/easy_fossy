from typing import List, Optional, Any
from .base import Resource
from ..models import Job

class JobsResource(Resource):
    @property
    def base_path(self) -> str:
        return "jobs"

    def get_all(self, upload_id: Optional[int] = None, status: Optional[str] = None, limit: int = 1000, page: int = 1) -> List[Job]:
        """List of jobs present in the instance"""
        params = {
            "limit": str(limit),
            "page": str(page),
            "groupName": self.config.group_name,
        }
        if upload_id:
            params["upload"] = str(upload_id)
        if status:
            params["status"] = status

        data = self._request("GET", params=params)
        return [Job(**job) for job in data] if isinstance(data, list) else []

    def get_by_id(self, job_id: int) -> Job:
        """Get job info by ID"""
        data = self._request("GET", path=f"/{job_id}")
        return Job(**data) if data else None

    def delete(self, job_id: int, queue_id: int = 1):
        """Delete a job. FOSSology contract: DELETE /jobs/{id}/{queue}"""
        return self._request("DELETE", path=f"/{job_id}/{queue_id}")

    def get_all_admin(self) -> List[Job]:
        """Get all jobs for admin"""
        data = self._request("GET", path="/all")
        return [Job(**job) for job in data] if isinstance(data, list) else []

    def schedule_analysis(self, upload_id: int, folder_id: int, analysis: Optional[dict] = None):
        """Schedule an analysis run for an upload.
        FOSSology contract: POST /jobs with folderId + uploadId headers and a
        ScanOptions body. Returns the Info payload whose ``message`` is the job id.
        """
        headers = {"folderId": str(folder_id), "uploadId": str(upload_id)}
        return self._request("POST", path="", headers=headers, json={"analysis": analysis or {}})

    def schedule_agent(self, upload_id: int, agents: List[str], folder_id: Optional[int] = None):
        """Schedule one job per named agent for an upload.

        ``folder_id`` is looked up from the upload when omitted (POST /jobs
        requires both headers). Returns a mapping of agent -> Info payload.
        """
        if folder_id is None:
            upload = self.client.uploads.get_upload_by_id(upload_id)
            if upload is None or upload.folderid is None:
                raise ValueError(f"Could not resolve folder for upload {upload_id}")
            folder_id = upload.folderid
        scheduled = {}
        for agent in agents:
            scheduled[agent] = self.schedule_analysis(upload_id, folder_id, {agent: True})
        return scheduled

    def get_scheduler_options(self, operation_name: str):
        """Get scheduler options by operation"""
        return self._request("GET", path=f"/scheduler/operation/{operation_name}")

    def handle_scheduler_run(self, payload: dict):
        """Handle scheduler run"""
        return self._request("POST", path="/scheduler/operation/run", json=payload)

    def get_statistics(self):
        """Get job statistics"""
        return self._request("GET", path="/dashboard/statistics")

    def get_all_server_jobs(self):
        """Get all server jobs"""
        return self._request("GET", path="/dashboard")
