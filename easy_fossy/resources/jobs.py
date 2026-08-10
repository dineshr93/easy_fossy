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
