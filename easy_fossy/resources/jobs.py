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
        """Delete a job"""
        params = {"queue_id": str(queue_id)}
        return self._request("DELETE", path=f"/{job_id}", params=params)

    def get_all_admin(self) -> List[Job]:
        """Get all jobs for admin"""
        data = self._request("GET", path="/all")
        return [Job(**job) for job in data] if isinstance(data, list) else []

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
        """Get all server jobs」"""
        return self._request("GET", path="/dashboard")
