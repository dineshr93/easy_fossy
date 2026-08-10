from typing import List, Optional, Any
from .base import Resource
from ..models import License, LicenseCount

class LicensesResource(Resource):
    @property
    def base_path(self) -> str:
        return "licenses"

    def get_all(self, is_active: str = "true", license_kind: str = "main", page: int = 1, limit: int = 100) -> List[License]:
        """List all licenses based on criteria"""
        params = {
            "is_active": is_active,
            "license_kind": license_kind,
            "page": str(page),
            "limit": str(limit),
        }
        data = self._request("GET", params=params)
        return [License(**l) for l in data] if isinstance(data, list) else []

    def get_by_short_name(self, short_name: str) -> License:
        """Get license by short name"""
        data = self._request("GET", path=f"/{short_name}")
        return License(**data) if data else None

    def add(self, unique_short_name: str, new_full_name: str, new_license_text: str, new_url: str, new_risk: int, isCandidate: bool = True):
        """Add a new license"""
        payload = {
            "unique_short_name": unique_short_name,
            "new_full_name": new_full_name,
            "new_license_text": new_license_text,
            "new_url": new_url,
            "new_risk": new_risk,
            "isCandidate": isCandidate,
        }
        return self._request("POST", json=payload)

    def get_histogram(self, upload_id: int) -> List[LicenseCount]:
        """Get license histogram for an upload"""
        params = {"upload": str(upload_id)}
        data = self._request("GET", path="/histogram", params=params)
        return [LicenseCount(**lc) for lc in data] if isinstance(data, list) else []
