"""
easy_fossy — Business-relevant utility functions combining multiple API calls.

These functions wrap the low-level API methods from :py:mod:`easy_fossy`
into higher-level workflows useful for real-world FOSSology tasks.
"""

from __future__ import annotations

import time
from typing import Any

from easy_fossy import EasyFossy


# ───────────────────────────────────────────────────────────────
# 1. Full Package Scan Workflow
# ───────────────────────────────────────────────────────────────

def full_package_scan_workflow(
    client: EasyFossy,
    file_path: str,
    folder_id: int,
    scan_types: list[str] | None = None,
    poll_interval: float = 2.0,
    timeout: float = 300.0,
) -> dict[str, Any]:
    """
    Upload a package, schedule scans (nomos, monk, copyright), wait for
    completion, and return the consolidated results.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    file_path : str
        Path to the file to upload.
    folder_id : int
        Destination folder ID.
    scan_types : list[str] | None
        Which agents to schedule. Defaults to ``["nomos", "monk", "copyright"]``.
    poll_interval : float
        Seconds between job-status polls.
    timeout : float
        Maximum seconds to wait for jobs to finish.

    Returns
    -------
    dict
        ``{"upload": …, "jobs": …, "licenses": …, "copyrights": …}``
    """
    if scan_types is None:
        scan_types = ["nomos", "monk", "copyright"]

    # 1. Upload the file
    upload = client.upload_file(file_path=file_path, folder_id=folder_id)
    if not upload:
        return {"error": "Upload failed"}

    upload_id = upload.id  # type: ignore[union-attr]

    # 2. Schedule scans
    agent_map: dict[str, int] = {}
    for agent in scan_types:
        job = client.schedule_agent(upload_id=upload_id, agents=[agent])
        if job and len(job) > 0:
            agent_map[agent] = job[0].id  # type: ignore[union-attr]

    # 3. Poll until all jobs are done
    deadline = time.time() + timeout
    while time.time() < deadline:
        jobs = client.get_all_jobs(upload_id=upload_id)
        completed = all(
            j.status == "completed" or j.status == "done"
            for j in jobs
            if j.id in agent_map.values()
        )
        if completed:
            break
        time.sleep(poll_interval)

    # 4. Gather results
    result: dict[str, Any] = {
        "upload": upload,
        "jobs": jobs if "jobs" in dir() else [],
    }

    # 4a. Edited / scanned licenses
    edited = client.get_all_edited_licenses(upload_id=upload_id)
    scanned = client.get_all_scanned_licenses(upload_id=upload_id)
    result["licenses"] = {"edited": edited, "scanned": scanned}

    # 4b. Copyright findings (default item = 0 – root tree)
    copyrights = client.get_file_copyrights(upload_id=upload_id, item_id=0)
    result["copyrights"] = copyrights

    return result


# ───────────────────────────────────────────────────────────────
# 2. License Audit Report
# ───────────────────────────────────────────────────────────────

def license_audit_report(
    client: EasyFossy,
    upload_id: int,
    item_id: int = 0,
) -> dict[str, Any]:
    """
    For a completed upload, gather edited + scanned licenses, compare them,
    and identify unmatched / pending decisions.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    upload_id : int
        Upload to audit.
    item_id : int
        Tree item to inspect. Defaults to 0 (root).

    Returns
    -------
    dict
        ``{"upload": …, "edited": …, "scanned": …, "unmatched": …}``
    """
    upload = client.get_upload_by_id(upload_id=upload_id)
    edited = client.get_all_edited_licenses(upload_id=upload_id)
    scanned = client.get_all_scanned_licenses(upload_id=upload_id)
    progress = client.get_clearing_progress_info(upload_id=upload_id)
    history = client.get_clearing_history(upload_id=upload_id, item_id=item_id)

    # Build a simple diff: edited vs scanned
    edited_shortnames = {l.get("shortName", l.get("shortname")) for l in edited}
    scanned_shortnames = {l.get("shortName", l.get("shortname")) for l in scanned}

    unmatched = [
        l for l in scanned
        if l.get("shortName", l.get("shortname")) not in edited_shortnames
    ]

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
    client: EasyFossy,
    upload_id: int,
) -> dict[str, Any]:
    """
    For an upload, fetch clearing progress, history, agent info, and current
    status in one consolidated payload.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    upload_id : int
        Upload to inspect.

    Returns
    -------
    dict
        Dashboard data.
    """
    upload = client.get_upload_by_id(upload_id=upload_id)
    progress = client.get_clearing_progress_info(upload_id=upload_id)
    agents = client.get_agents_by_upload_id(upload_id=upload_id)
    revisions = client.get_revisions_for_agents(upload_id=upload_id)
    reuse = client.get_licenses_reuse_summary(upload_id=upload_id)

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
    client: EasyFossy,
    upload_id: int,
    report_format: str = "PDF",
) -> dict[str, Any]:
    """
    Generate a compliance report for an upload. Combines license reuse
    summary data with report generation.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    upload_id : int
        Upload to report on.
    report_format : str
        Format of the report (e.g. "PDF", "HTML").

    Returns
    -------
    dict
        Compliance report data.
    """
    reuse = client.get_licenses_reuse_summary(upload_id=upload_id)
    # Note: actual report download endpoint is not covered in the existing
    # client methods — this provides the data needed to construct one.
    return {
        "upload_id": upload_id,
        "license_reuse_summary": reuse,
        "report_format": report_format,
    }


# ───────────────────────────────────────────────────────────────
# 5. User Audit Trail
# ───────────────────────────────────────────────────────────────

def user_audit_trail(
    client: EasyFossy,
    user_id: int | None = None,
) -> dict[str, Any]:
    """
    Get details about the current (or a specific) user, their jobs, and group
    memberships.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    user_id : int | None
        If None, fetches the logged-in user.

    Returns
    -------
    dict
        User audit data.
    """
    user = client.get_self()
    jobs = client.get_all_jobs(upload_id=0)  # all jobs for this user
    groups = client.get_groups()

    return {
        "user": user,
        "jobs": jobs,
        "groups": groups,
    }


# ───────────────────────────────────────────────────────────────
# 6. Folder Inventory
# ───────────────────────────────────────────────────────────────

def folder_inventory(
    client: EasyFossy,
    folder_id: int,
    include_licenses: bool = False,
) -> dict[str, Any]:
    """
    Get folder contents with all uploads, their licenses, and status.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    folder_id : int
        Folder to inspect.
    include_licenses : bool
        Whether to fetch license data for each upload (may be slow).

    Returns
    -------
    dict
        Folder inventory data.
    """
    folder = client.get_folder_by_id(folder_id=folder_id)
    contents = client.get_all_folder_contents(folder_id=folder_id)

    uploads_detail = []
    if include_licenses:
        for item in contents:
            if "uploadId" in item or "upload_id" in item:
                uid = item.get("uploadId") or item.get("upload_id")
                if uid:
                    edited = client.get_all_edited_licenses(upload_id=uid)
                    scanned = client.get_all_scanned_licenses(upload_id=uid)
                    uploads_detail.append({
                        "upload_id": uid,
                        "edited": edited,
                        "scanned": scanned,
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
    client: EasyFossy,
    file_path: str,
) -> dict[str, Any]:
    """
    Run one-shot analysis on a package without uploading. Runs nomos, monk,
    and CEU (copyright / email / URL) analyses.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    file_path : str
        Path to the file to analyse.

    Returns
    -------
    dict
        One-shot analysis results.
    """
    nomos = client.run_one_shot_nomos(file_path=file_path)
    monk = client.run_one_shot_monk(file_path=file_path)
    ceu = client.run_one_shot_ceu(file_path=file_path)

    return {
        "nomos": nomos,
        "monk": monk,
        "ceu": ceu,
    }


# ───────────────────────────────────────────────────────────────
# 8. License Candidate Review (Admin)
# ───────────────────────────────────────────────────────────────

def license_candidate_review(
    client: EasyFossy,
    acknowledge: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Admin review of pending license candidates with acknowledgement
    management.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    acknowledge : list[dict] | None
        Optional list of acknowledgement mutations to apply.

    Returns
    -------
    dict
        Candidates and acknowledgements data.
    """
    candidates = client.get_admin_license_candidates()
    acknowledgements = client.get_admin_license_acknowledgements()
    std_comments = client.get_all_standard_license_comments()

    result = {
        "candidates": candidates,
        "acknowledgements": acknowledgements,
        "standard_comments": std_comments,
    }

    if acknowledge is not None:
        result["acknowledgement_update"] = client.mutate_admin_license_acknowledgement(acknowledge)

    return result


# ───────────────────────────────────────────────────────────────
# 9. Job Dashboard Monitor
# ───────────────────────────────────────────────────────────────

def job_dashboard_monitor(
    client: EasyFossy,
    status_filter: str | None = None,
) -> dict[str, Any]:
    """
    Monitor all jobs, get statistics, filter by status.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.
    status_filter : str | None
        Optional status to filter jobs by.

    Returns
    -------
    dict
        Dashboard data.
    """
    all_jobs = client.get_all_jobs_admin(status=status_filter)
    statistics = client.get_job_statistics()
    server_jobs = client.get_all_server_jobs()

    return {
        "jobs": all_jobs,
        "statistics": statistics,
        "server_jobs": server_jobs,
    }


# ───────────────────────────────────────────────────────────────
# 10. Group Membership Audit
# ───────────────────────────────────────────────────────────────

def group_membership_audit(
    client: EasyFossy,
) -> list[dict[str, Any]]:
    """
    List all groups with their members and permissions.

    Parameters
    ----------
    client : EasyFossy
        An authenticated client instance.

    Returns
    -------
    list[dict]
        Each entry: ``{"group": …, "members": …}``
    """
    groups = client.get_groups()
    results: list[dict[str, Any]] = []

    for group in groups:
        members = client.get_group_users_with_roles(group_id=group.id)  # type: ignore[union-attr]
        results.append({
            "group": group,
            "members": members,
        })

    return results
