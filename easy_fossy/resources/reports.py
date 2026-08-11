"""Reports resource for the easy_fossy FOSSology REST API wrapper.

FOSSology contract:
  GET /report        -> generate/schedule a report for an upload (headers:
                        uploadId, reportFormat, groupName). Response is an
                        Info payload whose ``message`` holds a download URL
                        ending with the report id.
  GET /report/{id}   -> download the generated report. Returns 503 with a
                        Retry-After header until the report is ready, then
                        200 with the report body (text or binary depending on
                        the requested format).

The download endpoint returns a non-JSON body, so it bypasses the generic
``_request`` helper (which calls ``.json()``) and uses the raw session with its
own polling loop, mirroring ``UploadsResource.upload_file``.
"""

import time
from typing import Optional

from .base import Resource
from ..models import Info
from ..exceptions import FossyAPIError


class ReportsResource(Resource):
    @property
    def base_path(self) -> str:
        return "report"

    def _extract_report_id(self, info: dict) -> Optional[int]:
        """The Info ``message`` is a download URL like ``.../report/123``;
        pull the trailing report id out of it."""
        msg = info.get("message") if isinstance(info, dict) else info
        if not msg:
            return None
        return int(str(msg).rsplit("/", 1).pop())

    def get_reports_by_upload(
        self,
        upload_id: int,
        report_format,
        group_name: Optional[str] = None,
    ) -> Optional[int]:
        """Generate (schedule) a report for ``upload_id`` and return the report id.

        FOSSology contract: GET /report with ``uploadId``, ``reportFormat`` and
        ``groupName`` headers. The server returns an Info payload whose
        ``message`` is a download URL; the report id is its trailing segment.
        ``report_format`` is any ``ReportFormat`` enum member.
        """
        headers = {
            "accept": "application/json",
            "uploadId": str(upload_id),
            "reportFormat": str(report_format.name),
            "groupName": group_name or self.config.group_name,
        }
        data = self._request("GET", headers=headers)
        return self._extract_report_id(data)

    def download_report(
        self,
        report_id: int,
        group_name: Optional[str] = None,
        accept: str = "text/plain",
        timeout: float = 20.0,
        poll_interval: float = 0.2,
    ) -> bytes:
        """Download the report with ``report_id``, polling until it is ready.

        FOSSology contract: GET /report/{id}. While the report is still being
        generated the server returns 503 with a ``Retry-After`` header; this
        polls until it returns 200 and then returns the raw report body.
        """
        headers = {
            "accept": accept,
            "groupName": group_name or self.config.group_name,
        }
        url = f"{self.client.url.rstrip('/')}/{self.base_path}/{report_id}"
        deadline = time.time() + timeout
        while True:
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                return response.content
            if response.status_code == 503:
                retry = response.headers.get("Retry-After")
                if retry:
                    try:
                        time.sleep(float(retry))
                    except ValueError:
                        pass
                elif time.time() < deadline:
                    time.sleep(poll_interval)
                if time.time() >= deadline:
                    break
                continue
            # Any other status is a domain error (e.g. 404 "no report scheduled
            # with given job id") — surface it as FossyAPIError like the rest of
            # the library.
            raise FossyAPIError(
                f"Failed to download report {report_id}: {response.text}",
                status_code=response.status_code,
                response_text=response.text,
            )
        raise FossyAPIError(
            f"Report {report_id} not ready before timeout "
            f"(last status {response.status_code})",
            status_code=response.status_code,
            response_text=response.text,
        )

    def generate_and_get_desired_report_for_uploadid(
        self,
        upload_id: int,
        report_format,
        group_name: Optional[str] = None,
        save_to: Optional[str] = None,
    ) -> bytes:
        """Generate a report for ``upload_id`` then download it.

        Convenience wrapper matching the legacy method: schedules the report via
        ``get_reports_by_upload`` and downloads it via ``download_report``. If
        ``save_to`` is given, the report body is written to that file (binary);
        the bytes are always returned.
        """
        report_id = self.get_reports_by_upload(upload_id, report_format, group_name)
        if report_id is None:
            raise RuntimeError(
                f"Could not schedule report for upload {upload_id}: no report id returned"
            )
        body = self.download_report(report_id, group_name)
        if save_to:
            with open(save_to, "wb") as f:
                f.write(body)
        return body
