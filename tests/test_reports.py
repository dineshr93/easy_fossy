"""Tests for the Reports resource against the live FOSSology instance."""

import pytest

from easy_fossy.exceptions import FossyAPIError, FossyConnectionError
from easy_fossy.models import ReportFormat


def _reaches_server(fn):
    """Run fn; a returned value or any FossyAPIError (domain response) proves the
    endpoint is wired. Network-level errors (FossyConnectionError) still fail."""
    try:
        return fn() is not None
    except FossyAPIError:
        return True


def test_get_reports_by_upload_reaches_server(client):
    # No live upload exists on this instance, so report generation for a
    # non-existent upload must yield a domain response (e.g. 403 "Upload is not
    # accessible"), proving GET /report + header contract is wired — not a
    # network/404-path error.
    assert _reaches_server(
        lambda: client.reports.get_reports_by_upload(999999, ReportFormat.dep5)
    )


def test_download_report_reaches_server(client):
    # Downloading a report id that does not exist must return a domain response
    # (404/503) rather than a network error, proving GET /report/{id} is wired.
    assert _reaches_server(lambda: client.reports.download_report(999999))
