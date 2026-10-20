"""
easy_fossy — Business-relevant utility functions combining multiple API calls.

These functions wrap the low-level API methods from :py:mod:`easy_fossy`
into higher-level workflows useful for real-world FOSSology tasks. Every
function here calls only methods that exist on a resource; the interface is
tested in ``tests/test_usecases.py``.
"""

from __future__ import annotations

import time
from typing import Any, Optional

from .client import FossyClient
from .exceptions import FossyAPIError
from .models import ReportFormat, Status


# ───────────────────────────────────────────────────────────────
# shared helpers
# ───────────────────────────────────────────────────────────────

def _short_name(item: Any) -> Optional[str]:
    """Read a license short name from a model or from a raw payload.

    The server spells it ``shortName`` or ``shortname`` depending on endpoint;
    that variance is absorbed here so workflows read one name.
    """
    if isinstance(item, dict):
        return item.get("shortName") or item.get("shortname")
    return getattr(item, "shortName", None)


def _upload_id(item: Any) -> Optional[int]:
    """Read an upload id from a folder-content dict (``uploadId`` / ``upload_id``)."""
    if isinstance(item, dict):
        return item.get("uploadId") or item.get("upload_id")
    return getattr(item, "id", None)


def _job_id(info: Any) -> Optional[int]:
    """Read the scheduled job id out of an Info payload's ``message``."""
    msg = info.get("message") if isinstance(info, dict) else info
    try:
        return int(msg) if msg is not None else None
    except (TypeError, ValueError):
        return None


def _wait_for_jobs(
    client: FossyClient,
    upload_id: int,
    job_ids: set[int],
    poll_interval: float = 2.0,
    timeout: float = 300.0,
) -> list:
    """Poll until every job in ``job_ids`` is completed; raise on timeout."""
    deadline = time.time() + timeout
    last = []
    while time.time() < deadline:
        last = client.jobs.get_all(upload_id=upload_id)
        states = {
            job.id: job.status
            for job in last
            if job.id in job_ids
        }
        if states and all(s == Status.Completed for s in states.values()):
            return last
        if any(s == Status.Failed for s in states.values()):
            raise FossyAPIError(f"Analysis jobs failed for upload {upload_id}: {states}")
        time.sleep(poll_interval)
    raise FossyAPIError(f"Jobs {sorted(job_ids)} did not complete within {timeout}s (last states: {last})")


# ───────────────────────────────────────────────────────────────
# 1. Full Package Scan Workflow
# ───────────────────────────────────────────────────────────────

def full_package_scan_workflow(
    client: FossyClient,
    file_path: str,
    folder_id: int,
    scan_types: list[str] | None = None,
    poll_interval: float = 2.0,
    timeout: float = 300.0,
) -> dict[str, Any]:
    """
    Upload a package, schedule scans (nomos, monk, copyright), wait for
    completion, and return the consolidated results.
    """
    if scan_types is None:
        scan_types = ["nomos", "monk", "copyright_email_author"]

    upload = client.uploads.upload_file(file_path=file_path, folder_id=folder_id)
    if upload is None:
        raise FossyAPIError(f"Upload failed for {file_path}")

    upload_id = upload.id
    scheduled = client.jobs.schedule_agent(upload_id=upload_id, agents=scan_types, folder_id=folder_id)
    job_ids = {jid for jid in (_job_id(info) for info in scheduled.values()) if jid is not None}
    jobs = _wait_for_jobs(client, upload_id, job_ids, poll_interval, timeout)

    return {
        "upload": upload,
        "jobs": jobs,
        "licenses": {
            "edited": client.uploads.get_all_edited(upload_id=upload_id),
            "scanned": client.uploads.get_all_scanned(upload_id=upload_id),
        },
        "copyrights": client.uploads.get_copyrights(upload_id=upload_id),
    }


# ───────────────────────────────────────────────────────────────
# 2. License Audit Report
# ───────────────────────────────────────────────────────────────

def license_audit_report(
    client: FossyClient,
    upload_id: int,
    item_id: int = 0,
) -> dict[str, Any]:
    """
    For a completed upload, gather edited + scanned licenses, compare them,
    and identify unmatched / pending decisions.
    """
    upload = client.uploads.get_upload_by_id(upload_id=upload_id)
    edited = client.uploads.get_all_edited(upload_id=upload_id)
    scanned = client.uploads.get_all_scanned(upload_id=upload_id)
    progress = client.uploads.get_clearing_progress_info(upload_id=upload_id)
    history = client.uploads.get_clearing_history(upload_id=upload_id, item_id=item_id)

    edited_shortnames = {n for n in (_short_name(l) for l in edited) if n}
    unmatched = [l for l in scanned if _short_name(l) not in edited_shortnames]

    return {
        "upload": upload,
        "edited": edited,
        "scanned": scanned,
        "unmatched": unmatched,
        "clearing_progress": progress,
        "clearing_history": history,
    }


# ───────────────────────────────────────────────────────────────
# 3. Clearing Status Dashboard
# ───────────────────────────────────────────────────────────────

def clearing_status_dashboard(
    client: FossyClient,
    upload_id: int,
) -> dict[str, Any]:
    """
    For an upload, fetch clearing progress, history, agent info, and current
    status in one consolidated payload.
    """
    upload = client.uploads.get_upload_by_id(upload_id=upload_id)
    progress = client.uploads.get_clearing_progress_info(upload_id=upload_id)
    agents = client.uploads.get_agents_by_upload_id(upload_id=upload_id)
    revisions = client.uploads.get_revisions_for_agents(upload_id=upload_id)
    reuse = client.uploads.get_reuse_summary(upload_id=upload_id)

    return {
        "upload": upload,
        "clearing_progress": progress,
        "agents": agents,
        "agent_revisions": revisions,
        "license_reuse_summary": reuse,
    }


# ───────────────────────────────────────────────────────────────
# 4. Compliance Report Generation
# ───────────────────────────────────────────────────────────────

def compliance_report_generation(
    client: FossyClient,
    upload_id: int,
    report_format: str = "dep5",
    save_to: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a compliance report for an upload and download it. Combines
    license reuse summary data with report generation.

    ``report_format`` is a ``ReportFormat`` member name (e.g. ``"dep5"``).
    """
    reuse = client.uploads.get_reuse_summary(upload_id=upload_id)
    if isinstance(report_format, str):
        try:
            fmt = ReportFormat[report_format]
        except KeyError:
            raise ValueError(
                f"unknown report format {report_format!r}; expected one of "
                f"{[m.name for m in ReportFormat]}"
            )
    else:
        fmt = report_format
    body = client.reports.generate_and_get_desired_report_for_uploadid(
        upload_id=upload_id, report_format=fmt, save_to=save_to
    )
    return {
        "upload_id": upload_id,
        "license_reuse_summary": reuse,
        "report_format": fmt.name,
        "report": body,
    }


# ───────────────────────────────────────────────────────────────
# 5. User Audit Trail
# ───────────────────────────────────────────────────────────────

def user_audit_trail(
    client: FossyClient,
    user_id: int | None = None,
) -> dict[str, Any]:
    """
    Get details about the current (or a specific) user, their jobs, and group
    memberships.
    """
    user = client.users.get_by_id(user_id) if user_id else client.users.get_self()
    jobs = client.jobs.get_all()
    groups = client.groups.get_all()

    return {
        "user": user,
        "jobs": jobs,
        "groups": groups,
    }


# ───────────────────────────────────────────────────────────────
# 6. Folder Inventory
# ───────────────────────────────────────────────────────────────

def folder_inventory(
    client: FossyClient,
    folder_id: int,
    include_licenses: bool = False,
) -> dict[str, Any]:
    """
    Get folder contents with all uploads, their licenses, and status.
    """
    folder = client.folders.get_by_id(folder_id=folder_id)
    contents = client.folders.get_contents(folder_id=folder_id)

    uploads_detail = []
    if include_licenses:
        for item in contents:
            uid = _upload_id(item)
            if uid:
                uploads_detail.append({
                    "upload_id": uid,
                    "edited": client.uploads.get_all_edited(upload_id=uid),
                    "scanned": client.uploads.get_all_scanned(upload_id=uid),
                })

    return {
        "folder": folder,
        "contents": contents,
        "uploads_detail": uploads_detail,
    }


# ───────────────────────────────────────────────────────────────
# 7. Package Analysis Summary (One-Shot)
# ───────────────────────────────────────────────────────────────

def package_analysis_summary(
    client: FossyClient,
    file_path: str,
) -> dict[str, Any]:
    """
    Run one-shot analysis on a package without uploading. Runs nomos, monk,
    and CEU (copyright / email / URL) analyses.
    """
    return {
        "nomos": client.uploads.run_one_shot_nomos(file_path=file_path),
        "monk": client.uploads.run_one_shot_monk(file_path=file_path),
        "ceu": client.uploads.run_one_shot_ceu(file_path=file_path),
    }


# ───────────────────────────────────────────────────────────────
# 8. License Candidate Review (Admin)
# ───────────────────────────────────────────────────────────────

def license_candidate_review(
    client: FossyClient,
    acknowledge: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Admin review of pending license candidates with acknowledgement
    management.
    """
    result = {
        "candidates": client.licenses.get_admin_candidates(),
        "acknowledgements": client.licenses.get_admin_acknowledgements(),
        "standard_comments": client.licenses.get_standard_comments(),
    }

    if acknowledge is not None:
        result["acknowledgement_update"] = client.licenses.mutate_acknowledgement(acknowledge)

    return result


# ───────────────────────────────────────────────────────────────
# 9. Job Dashboard Monitor
# ───────────────────────────────────────────────────────────────

def job_dashboard_monitor(
    client: FossyClient,
    status_filter: str | None = None,
) -> dict[str, Any]:
    """
    Monitor all jobs, get statistics, filter by status.
    """
    return {
        "jobs": client.jobs.get_all(status=status_filter),
        "statistics": client.jobs.get_statistics(),
        "server_jobs": client.jobs.get_all_server_jobs(),
    }


# ───────────────────────────────────────────────────────────────
# 10. Group Membership Audit
# ───────────────────────────────────────────────────────────────

def group_membership_audit(
    client: FossyClient,
) -> list[dict[str, Any]]:
    """
    List all groups with their members and permissions.
    """
    return [
        {"group": group, "members": client.groups.get_users_with_roles(group_id=group.id)}
        for group in client.groups.get_all()
    ]
