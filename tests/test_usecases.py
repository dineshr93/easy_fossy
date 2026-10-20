"""usecases.py through the transport seam: every workflow calls real interfaces."""

import pytest

from easy_fossy.usecases import (
    clearing_status_dashboard,
    compliance_report_generation,
    folder_inventory,
    full_package_scan_workflow,
    group_membership_audit,
    job_dashboard_monitor,
    license_audit_report,
    license_candidate_review,
    package_analysis_summary,
    user_audit_trail,
)

from stub import StubResponse, make_client


def test_license_audit_report_computes_unmatched():
    client, _ = make_client({
        ("GET", "uploads/7"): StubResponse(200, {"id": 7, "uploadname": "pkg"}),
        ("GET", "uploads/7/licenses/edited"): StubResponse(200, [{"shortName": "MIT"}]),
        ("GET", "uploads/7/licenses/scanned"): StubResponse(200, [{"shortName": "MIT"}, {"shortname": "GPL-2.0"}]),
        ("GET", "uploads/7/clearing-progress"): StubResponse(200, {"filesToBeCleared": 3}),
        ("GET", "uploads/7/item/0/clearing-history"): StubResponse(200, []),
    })
    r = license_audit_report(client, 7)
    assert [l["shortname"] for l in r["unmatched"]] == ["GPL-2.0"]
    assert r["upload"].id == 7


def test_clearing_status_dashboard_returns_five_slices():
    client, session = make_client({
        ("GET", "uploads/7"): StubResponse(200, {"id": 7}),
        ("GET", "uploads/7/clearing-progress"): StubResponse(200, {}),
        ("GET", "uploads/7/agents"): StubResponse(200, []),
        ("GET", "uploads/7/agents/revision"): StubResponse(200, []),
        ("GET", "uploads/7/licenses/reuse"): StubResponse(200, {}),
    })
    r = clearing_status_dashboard(client, 7)
    assert set(r) == {"upload", "clearing_progress", "agents", "agent_revisions", "license_reuse_summary"}
    assert len(session.calls) == 5


def test_folder_inventory_with_licenses():
    client, _ = make_client({
        ("GET", "folders/1"): StubResponse(200, {"id": 1, "name": "root"}),
        ("GET", "folders/1/contents"): StubResponse(200, [{"uploadId": 3}, {"upload_id": 4}, {"folderId": 9}]),
        ("GET", "uploads/3/licenses/edited"): StubResponse(200, []),
        ("GET", "uploads/3/licenses/scanned"): StubResponse(200, []),
        ("GET", "uploads/4/licenses/edited"): StubResponse(200, []),
        ("GET", "uploads/4/licenses/scanned"): StubResponse(200, []),
    })
    r = folder_inventory(client, 1, include_licenses=True)
    assert r["folder"].name == "root"
    assert [u["upload_id"] for u in r["uploads_detail"]] == [3, 4]


def test_license_candidate_review_uses_admin_endpoints():
    client, _ = make_client({
        ("GET", "license/admincandidates"): StubResponse(200, []),
        ("GET", "license/adminacknowledgements"): StubResponse(200, []),
        ("GET", "license/stdcomments"): StubResponse(200, []),
        ("PUT", "license/adminacknowledgements"): StubResponse(200, {"message": "ok"}),
    })
    r = license_candidate_review(client, acknowledge=[{"id": 1}])
    assert r["acknowledgement_update"] == {"message": "ok"}


def test_user_audit_trail_self():
    client, _ = make_client({
        ("GET", "users/self"): StubResponse(200, {"id": 3, "name": "admin", "description": ""}),
        ("GET", "jobs"): StubResponse(200, []),
        ("GET", "groups"): StubResponse(200, []),
    })
    r = user_audit_trail(client)
    assert r["user"]["id"] == 3


def test_job_dashboard_monitor():
    client, _ = make_client({
        ("GET", "jobs"): StubResponse(200, [{"id": 1, "status": "Completed"}]),
        ("GET", "jobs/dashboard/statistics"): StubResponse(200, []),
        ("GET", "jobs/dashboard"): StubResponse(200, []),
    })
    r = job_dashboard_monitor(client, status_filter="Completed")
    assert r["jobs"][0].id == 1


def test_group_membership_audit():
    client, _ = make_client({
        ("GET", "groups"): StubResponse(200, [{"id": 1, "name": "g"}]),
        ("GET", "groups/1/members"): StubResponse(200, [{"uid": 3}]),
    })
    r = group_membership_audit(client)
    assert r[0]["group"].id == 1 and r[0]["members"] == [{"uid": 3}]


def test_package_analysis_summary_runs_three_agents(tmp_path):
    client, session = make_client({
        ("POST", "uploads/oneshot/nomos"): StubResponse(200, {"message": "nomos"}),
        ("POST", "uploads/oneshot/monk"): StubResponse(200, {"message": "monk"}),
        ("POST", "uploads/oneshot/ceu"): StubResponse(200, {"message": "ceu"}),
    })
    f = tmp_path / "f.txt"
    f.write_text("MIT")
    r = package_analysis_summary(client, str(f))
    assert r == {"nomos": {"message": "nomos"}, "monk": {"message": "monk"}, "ceu": {"message": "ceu"}}
    assert [c["path"] for c in session.calls] == ["uploads/oneshot/nomos", "uploads/oneshot/monk", "uploads/oneshot/ceu"]


def test_full_package_scan_workflow(tmp_path):
    client, session = make_client({
        ("POST", "uploads"): StubResponse(201, {"message": "42"}),
        ("GET", "uploads/42"): StubResponse(200, {"id": 42, "uploadname": "pkg.zip", "folderid": 9}),
        ("POST", "jobs"): [StubResponse(201, {"message": "1"}), StubResponse(201, {"message": "2"})],
        ("GET", "jobs"): StubResponse(200, [{"id": 1, "status": "Completed"}, {"id": 2, "status": "Completed"}]),
        ("GET", "uploads/42/licenses/edited"): StubResponse(200, []),
        ("GET", "uploads/42/licenses/scanned"): StubResponse(200, []),
        ("GET", "uploads/42/copyrights"): StubResponse(200, []),
    })
    pkg = tmp_path / "pkg.zip"
    pkg.write_bytes(b"PK")
    r = full_package_scan_workflow(client, str(pkg), folder_id=9, poll_interval=0.01)
    assert r["upload"].id == 42
    assert [j.id for j in r["jobs"]] == [1, 2]
    assert r["licenses"] == {"edited": [], "scanned": []}


def test_full_package_scan_raises_when_a_job_fails(tmp_path):
    from easy_fossy.exceptions import FossyAPIError

    client, _ = make_client({
        ("POST", "uploads"): StubResponse(201, {"message": "42"}),
        ("GET", "uploads/42"): StubResponse(200, {"id": 42, "folderid": 9}),
        ("POST", "jobs"): StubResponse(201, {"message": "1"}),
        ("GET", "jobs"): StubResponse(200, [{"id": 1, "status": "Failed"}]),
    })
    pkg = tmp_path / "pkg.zip"
    pkg.write_bytes(b"PK")
    with pytest.raises(FossyAPIError):
        full_package_scan_workflow(client, str(pkg), folder_id=9, scan_types=["nomos"], poll_interval=0.01)


def test_compliance_report_generation_schedules_and_downloads():
    client, session = make_client({
        ("GET", "uploads/7/licenses/reuse"): StubResponse(200, {"reuse": 1}),
        ("GET", "report"): StubResponse(200, {"message": "http://stub/api/v1/report/55"}),
        ("GET", "report/55"): StubResponse(200, text="dep5 body"),
    })
    r = compliance_report_generation(client, 7, report_format="dep5")
    assert r["report"] == b"dep5 body" and r["report_format"] == "dep5"
    assert session.calls[1]["headers"]["reportFormat"] == "dep5"


def test_compliance_report_rejects_unknown_format():
    client, _ = make_client({("GET", "uploads/7/licenses/reuse"): StubResponse(200, {})})
    with pytest.raises(ValueError):
        compliance_report_generation(client, 7, report_format="PDF")
