"""Resources through the transport seam — no instance, no network."""

import pytest

from easy_fossy.exceptions import FossyAPIError
from easy_fossy.models import LicenseCount, Upload

from stub import StubResponse, make_client


def test_upload_licenses_endpoints_return_lists():
    client, session = make_client({
        ("GET", "uploads/7/licenses/edited"): StubResponse(200, [{"shortName": "MIT"}]),
        ("GET", "uploads/7/licenses/scanned"): StubResponse(200, [{"shortname": "GPL-2.0"}, {"shortname": "MIT"}]),
        ("GET", "uploads/7/licenses/reuse"): StubResponse(200, {"reuse": 0}),
    })
    assert client.uploads.get_all_edited(7) == [{"shortName": "MIT"}]
    assert [l["shortname"] for l in client.uploads.get_all_scanned(7)] == ["GPL-2.0", "MIT"]
    assert client.uploads.get_reuse_summary(7) == {"reuse": 0}
    assert session.calls[0]["path"] == "uploads/7/licenses/edited"


def test_copyrights_are_models():
    client, _ = make_client({
        ("GET", "uploads/7/copyrights"): StubResponse(200, [{"content": "Copyright X", "hash": "abc", "count": 2}]),
    })
    found = client.uploads.get_copyrights(7)
    assert found and found[0].content == "Copyright X"


def test_clearing_and_agent_endpoints():
    client, session = make_client({
        ("GET", "uploads/7/clearing-progress"): StubResponse(200, {"filesToBeCleared": 0}),
        ("GET", "uploads/7/item/0/clearing-history"): StubResponse(200, []),
        ("GET", "uploads/7/agents"): StubResponse(200, []),
        ("GET", "uploads/7/agents/revision"): StubResponse(200, []),
    })
    assert client.uploads.get_clearing_progress_info(7)["filesToBeCleared"] == 0
    assert client.uploads.get_clearing_history(7, 0) == []
    assert client.uploads.get_agents_by_upload_id(7) == []
    assert client.uploads.get_revisions_for_agents(7) == []
    assert [c["path"] for c in session.calls] == [
        "uploads/7/clearing-progress",
        "uploads/7/item/0/clearing-history",
        "uploads/7/agents",
        "uploads/7/agents/revision",
    ]


def test_export_csv_reads_a_non_json_body():
    client, _ = make_client({("GET", "license/export-csv"): StubResponse(200, text="shortName\nMIT")})
    assert client.licenses.export_csv() == "shortName\nMIT"


def test_import_csv_failure_raises_instead_of_returning_none(tmp_path):
    client, _ = make_client({("POST", "license/import-csv"): StubResponse(400, text="bad csv")})
    csv = tmp_path / "l.csv"
    csv.write_text("shortName\nMIT")
    with pytest.raises(FossyAPIError):
        client.licenses.import_csv(str(csv))


def test_import_json_sends_the_fileinput_field(tmp_path):
    client, session = make_client({("POST", "license/import-json"): StubResponse(201, {"message": "ok"})})
    js = tmp_path / "l.json"
    js.write_text("[]")
    assert client.licenses.import_json(str(js)) == {"message": "ok"}
    assert "fileInput" in session.calls[0]["data"].fields


def test_upload_file_posts_multipart_then_waits(tmp_path):
    client, session = make_client({
        ("POST", "uploads"): StubResponse(201, {"message": "42"}),
        ("GET", "uploads/42"): StubResponse(200, {"id": 42, "uploadname": "pkg.zip", "folderid": 9}),
    })
    pkg = tmp_path / "pkg.zip"
    pkg.write_bytes(b"PK")
    upload = client.uploads.upload_file(str(pkg), folder_id=9)
    assert isinstance(upload, Upload) and upload.id == 42
    assert session.calls[0]["headers"]["folderId"] == "9"
    assert session.calls[0]["headers"]["uploadType"] == "file"


def test_upload_file_raises_on_server_error(tmp_path):
    client, _ = make_client({("POST", "uploads"): StubResponse(500, text="nope")})
    pkg = tmp_path / "pkg.zip"
    pkg.write_bytes(b"PK")
    with pytest.raises(FossyAPIError):
        client.uploads.upload_file(str(pkg), folder_id=9)


def test_histogram_is_owned_by_uploads():
    client, session = make_client({
        ("GET", "uploads/7/licenses/histogram"): StubResponse(200, [{"id": 1, "name": "MIT", "scannerCount": 2, "concludedCount": 1}]),
    })
    hist = client.licenses.get_histogram(7)
    assert isinstance(hist[0], LicenseCount) and hist[0].name == "MIT"
    assert session.calls[0]["path"] == "uploads/7/licenses/histogram"


def test_schedule_agent_resolves_folder_from_the_upload():
    client, session = make_client({
        ("GET", "uploads/42"): StubResponse(200, {"id": 42, "folderid": 9}),
        ("POST", "jobs"): [StubResponse(201, {"message": "1"}), StubResponse(201, {"message": "2"})],
    })
    scheduled = client.jobs.schedule_agent(42, ["nomos", "monk"])
    assert [i["message"] for i in scheduled.values()] == ["1", "2"]
    posts = [c for c in session.calls if c["method"] == "POST"]
    assert posts[0]["headers"] == {"folderId": "9", "uploadId": "42"}
    assert posts[0]["json"] == {"analysis": {"nomos": True}}
    assert posts[1]["json"] == {"analysis": {"monk": True}}


def test_trigger_analysis_delegates_to_jobs():
    client, session = make_client({("POST", "jobs"): StubResponse(201, {"message": "5"})})
    assert client.uploads.trigger_analysis_for_upload_id(42, 9) == {"message": "5"}
    assert session.calls[0]["path"] == "jobs"
    assert session.calls[0]["json"]["analysis"]["nomos"] is True


def test_download_report_polls_until_ready():
    client, session = make_client({
        ("GET", "report/55"): [
            StubResponse(503, text="", headers={"Retry-After": "0"}),
            StubResponse(200, text="report body"),
        ],
    })
    assert client.reports.download_report(55) == b"report body"
    assert len(session.calls) == 2


def test_download_report_raises_on_domain_error():
    client, _ = make_client({("GET", "report/55"): StubResponse(404, text="no report scheduled")})
    with pytest.raises(FossyAPIError):
        client.reports.download_report(55)
