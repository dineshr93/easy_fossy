from typing import List, Optional, Any
from .base import Resource
from ..models import License, LicenseCount

class LicensesResource(Resource):
    @property
    def base_path(self) -> str:
        return "license"

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
        """Add a new license.
        FOSSology contract: POST /license with shortName/fullName/text/url/risk.
        """
        payload = {
            "shortName": unique_short_name,
            "fullName": new_full_name,
            "text": new_license_text,
            "url": new_url,
            "risk": new_risk,
            "mergeRequest": not isCandidate,
        }
        return self._request("POST", json=payload)

    def get_histogram(self, upload_id: int, agent_id: Optional[int] = None) -> List[LicenseCount]:
        """Get license histogram for an upload.
        FOSSology contract: GET /uploads/{id}/licenses/histogram
        """
        params = {}
        if agent_id is not None:
            params["agentId"] = str(agent_id)
        data = self._request("GET", path=f"/uploads/{upload_id}/licenses/histogram", params=params, absolute_path=True)
        return [LicenseCount(**lc) for lc in data] if isinstance(data, list) else []

    def import_csv(self, file_path: str, delimiter: str = ",", enclosure: str = '"'):
        """Import licenses from CSV.
        FOSSology contract: POST /license/import-csv (multipart, field ``file_input``).
        """
        import requests
        from requests_toolbelt.multipart.encoder import MultipartEncoder

        fields = {
            "file_input": (file_path.split("/")[-1], open(file_path, "rb"), None),
            "delimiter": delimiter,
            "enclosure": enclosure,
        }
        m = MultipartEncoder(fields=fields)

        response = self.session.post(
            f"{self.client.url}{self.base_path}/import-csv",
            data=m,
            headers={"Content-Type": m.content_type},
        )
        return response.json() if response.status_code in (200, 201) else None

    def export_csv(self):
        """Export licenses to CSV.
        FOSSology contract: GET /license/export-csv returns text/csv (not JSON).
        """
        response = self.session.get(f"{self.client.url}{self.base_path}/export-csv")
        if response.status_code in (200, 201):
            return response.text
        return None

    def import_json(self, file_path: str):
        """Import licenses from a JSON file.
        FOSSology contract: POST /license/import-json (multipart, field ``fileInput``).
        """
        import requests
        from requests_toolbelt.multipart.encoder import MultipartEncoder

        fields = {"fileInput": (file_path.split("/")[-1], open(file_path, "rb"), None)}
        m = MultipartEncoder(fields=fields)

        response = self.session.post(
            f"{self.client.url}{self.base_path}/import-json",
            data=m,
            headers={"Content-Type": m.content_type},
        )
        return response.json() if response.status_code in (200, 201) else None

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

    def verify(self, short_name: str, parent_shortname: Optional[str] = None):
        """Verify a license as new or variant.
        FOSSology contract: PUT /license/verify/{shortname} with body parentShortname.
        """
        payload = {"parentShortname": parent_shortname or short_name}
        return self._request("PUT", path=f"/verify/{short_name}", json=payload)

    def merge(self, short_name: str, parent_shortname: Optional[str] = None):
        """Merge a license into a parent.
        FOSSology contract: PUT /license/merge/{shortname} with body parentShortname.
        """
        payload = {"parentShortname": parent_shortname or short_name}
        return self._request("PUT", path=f"/merge/{short_name}", json=payload)

    def suggest(self, payload: dict):
        """Get suggested license"""
        return self._request("POST", path="/suggest", json=payload)
