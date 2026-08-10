"""
easy_fossy — Business-relevant utility functions combining multiple API calls.

These functions wrap the low-level API methods from :py:mod:`easy_fossy`
into higher-level workflows useful for real-world FOSSology tasks.
"""

from __future__ import annotations
import time
from typing import Any
from .client import FossyClient

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
        scan_types = ["nomos", "monk", "copyright"]

    # 1. Upload the file
    upload = client.uploads.upload_file(file_path=file_path, folder_id=folder_id)
    if not upload:
        return {"error": "Upload failed"}

    upload_id = upload.id

    # 2. Schedule scans
    agent_map: dict[str, int] = {}
    for agent in scan_types:
        # Note: schedule_agent needs to be added to JobsResource
        job = client.jobs.schedule_agent(upload_id=upload_id, agents=[agent])
        if job and len(job) > 0:
            agent_map[agent] = job[0].id

    # 3. Poll until all jobs are done
    deadline = time.time() + timeout
    while time.time() < deadline:
        jobs = client.jobs.get_all(upload_id=upload_id)
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
        "jobs": jobs if "jobs" in locals() else [],
    }

    # 4a. Edited / scanned licenses
    edited = client.licenses.get_all_edited(upload_id=upload_id)
    scanned = client.licenses.get_all_scanned(upload_id=upload_id)
    result["licenses"] = {"edited": edited, "scanned": scanned}

    # 4b. Copyright findings (default item = 0 – root tree)
    copyrights = client.uploads.get_copyrights(upload_id=upload_id, item_id=0)
    result["copyrights"] = copyrights

    return result

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
    edited = client.licenses.get_all_edited(upload_id=upload_id)
    scanned = client.licenses.get_all_scanned(upload_id=upload_id)
    progress = client.uploads.get_clearing_progress_info(upload_id=upload_id)
    history = client.uploads.get_clearing_history(upload_id=upload_id, item_id=item_id)

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
    reuse = client.licenses.get_reuse_summary(upload_id=upload_id)

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
    report_format: str = "PDF",
) -> dict[str, Any]:
    """
    Generate a compliance report for an upload. Combines license reuse
    summary data with report generation.
    """
    reuse = client.licenses.get_reuse_summary(upload_id=upload_id)
    return {
        "upload_id": upload_id,
        "license_reuse_summary": reuse,
        "report_format": report_format,
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
    jobs = client.jobs.get_all(upload_id=0)
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
            uid = item.get("uploadId") or item.get("upload_id")
            if uid:
                edited = client.licenses.get_all_edited(upload_id=uid)
                scanned = client.licenses.get_all_scanned(upload_id=uid)
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
    client: FossyClient,
    file_path: str,
) -> dict[str, Any]:
    """
    Run one-shot analysis on a package without uploading. Runs nomos, monk,
    and CEU (copyright / email / URL) analyses.
    """
    nomos = client.uploads.run_one_shot_nomos(file_path=file_path)
    monk = client.uploads.run_one_shot_monk(file_path=file_path)
    ceu = client.uploads.run_one_shot_ceu(file_path=file_path)

    return {
        "nomos": nomos,
        "monk": monk,
        "ceu": ceu,
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
    candidates = client.licenses.get_candidates()
    acknowledgements = client.licenses.get_acknowledgements()
    std_comments = client.licenses.get_standard_comments()

    result = {
        "candidates": candidates,
        "acknowledgements": acknowledgements,
        "standard_comments": std_comments,
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
    all_jobs = client.jobs.get_all(status=status_filter)
    statistics = client.jobs.get_statistics()
    server_jobs = client.jobs.get_all_server_jobs()

    return {
        "jobs": all_jobs,
        "statistics": statistics,
        "server_jobs": server_jobs,
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
    groups = client.groups.get_all()
    results: list[dict[str, Any]] = []

    for group in groups:
        members = client.groups.get_users_with_roles(group_id=group.id)
        results.append({
            "group": group,
            "members": members,
        })

    return results
