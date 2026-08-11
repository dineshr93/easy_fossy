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

    def import_csv(self, file_path: str):
        """Import licenses from CSV"""
        # CSV import usually requires multipart
        import requests
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        
        fields = {"file": (None, open(file_path, "rb"), None)}
        m = MultipartEncoder(fields=fields)
        
        response = self.session.post(
            f"{self.client.url}{self.base_path}/import-csv",
            data=m,
            headers={"Content-Type": m.content_type}
        )
        return response.json() if response.status_code == 200 else None

    def export_csv(self):
        """Export licenses to CSV"""
        return self._request("GET", path="/export-csv")

    def import_json(self, payload: dict):
        """Import licenses from JSON"""
        return self._request("POST", path="/import-json", json=payload)

    def export_json(self):
        """Export licenses to JSON"""
        return self._request("GET", path="/export-json")

    def update(self, short_name: str, payload: dict):
        """Update license info by short name"""
        return self._request("PATCH", path=f"/{short_name}", json=payload)

    def get_admin_candidates(self) -> List[License]:
        """Get admin license candidates"""
        data = self._request("GET", path="/admincandidates")
        return [License(**l) for l in data] if isinstance(data, list) else []

    def delete_candidate(self, candidate_id: int):
        """Delete license candidate by ID"""
        return self._request("DELETE", path=f"/admincandidates/{candidate_id}")

    def get_admin_acknowledgements(self):
        """Get admin license acknowledgements"""
        return self._request("GET", path="/adminacknowledgements")

    def mutate_acknowledgement(self, payload: dict):
        """Mutate admin license acknowledgement"""
        return self._request("PUT", path="/adminacknowledgements", json=payload)

    def get_standard_comments(self):
        """Get all standard license comments"""
        return self._request("GET", path="/stdcomments")

    def mutate_std_comments(self, payload: dict):
        """Mutate standard comments"""
        return self._request("PUT", path="/stdcomments", json=payload)

    def verify(self, short_name: str):
        """Verify license"""
        return self._request("PUT", path=f"/verify/{short_name}")

    def merge(self, short_name: str):
        """Merge license"""
        return self._request("PUT", path=f"/merge/{short_name}")

    def suggest(self, payload: dict):
        """Get suggested license"""
        return self._request("POST", path="/suggest", json=payload)
