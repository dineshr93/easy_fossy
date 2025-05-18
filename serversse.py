from mcp.server.fastmcp import FastMCP
from easy_fossy import easy_fossy
from easy_fossy.models import (
    Action,
    Agent,
    ClearingStatus,
    Public,
    ReportFormat,
    SearchType,
    Kind,
    License,
    User,
    Job,
    Info,
    Folder,
    Upload,
    UploadSummary,
    SearchResults,
    File,
    UploadLicense,
    LicenseShortnameGetResponse,
    Copyright
)
from typing import List, Optional, Union, Any, Dict, Tuple
import os
import datetime
from pathlib import Path
import asyncio
from pydantic import BaseModel, Field

# Create an MCP server with description
mcp = FastMCP(
    "EasyFossy", 
    description="Model Context Protocol server for Fossology license scanning and management, port localhost:8050",
    host="0.0.0.0",  # only used for SSE transport
    port=8050,  # only used for SSE transport (set this to any port)
)

# Initialize easy_fossy instance
fossy = None

# Validate that fossy is initialized
def ensure_fossy():
    if not fossy:
        raise ValueError("Please initialize fossy first using initialize_fossy")
    return fossy

# Helper function to convert RootModel output to list for Pydantic v2 compatibility
def convert_root_model(obj: Any) -> Any:
    """Convert pydantic v2 RootModel to appropriate type for MCP"""
    if hasattr(obj, "root") and hasattr(obj, "model_dump"):
        return obj.root
    if isinstance(obj, list):
        return [convert_root_model(item) for item in obj]
    if isinstance(obj, dict):
        return {k: convert_root_model(v) for k, v in obj.items()}
    return obj

@mcp.tool()
def initialize_fossy(config_file: str, server_to_use: str = "test", verify: bool = False) -> Dict[str, Any]:
    """Initialize the easy_fossy instance with configuration

    Args:
        config_file: Path to the config.ini file
        server_to_use: Server to use (test or prod)
        verify: Whether to verify SSL certificates
    
    Returns:
        Dictionary with initialization status and connection details
    """
    global fossy
    
    if not Path(config_file).exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    fossy = easy_fossy(config_file=config_file, server_to_use=server_to_use, verify=verify)
    
    return {
        "status": "success",
        "message": "Successfully initialized easy_fossy instance",
        "server": server_to_use,
        "url": fossy.url,
        "group_name": fossy.group_name
    }

# ==== User Management ====

@mcp.tool()
def get_all_users() -> List[User]:
    """List all users present in the given Fossology instance"""
    return convert_root_model(ensure_fossy().get_all_users())

@mcp.tool()
def get_user_by_id(user_id: int) -> User:
    """Get user details by ID
    
    Args:
        user_id: The ID of the user to retrieve
    """
    return convert_root_model(ensure_fossy().get_user_by_id(user_id))

# ==== Job Management ====

@mcp.tool()
def get_all_jobs() -> List[Job]:
    """List all jobs present in the given Fossology instance"""
    return convert_root_model(ensure_fossy().get_all_jobs())

@mcp.tool()
def get_job_info_by_id(job_id: int) -> Job:
    """Get job information by job ID
    
    Args:
        job_id: The ID of the job to retrieve
    """
    return convert_root_model(ensure_fossy().get_job_info_by_id(job_id))

@mcp.tool()
def get_job_info_by_upload_id(upload_id: int) -> Job:
    """Get job information by upload ID
    
    Args:
        upload_id: The ID of the upload to get job information for
    """
    return convert_root_model(ensure_fossy().get_job_info_by_upload_id(upload_id))

# ==== Folder Management ====

@mcp.tool()
def get_all_folders() -> List[Folder]:
    """Get all folders in the Fossology instance"""
    return convert_root_model(ensure_fossy().get_all_folders())

@mcp.tool()
def get_folder_info_by_id(folder_id: int) -> Folder:
    """Get folder information by ID
    
    Args:
        folder_id: The ID of the folder to retrieve
    """
    return convert_root_model(ensure_fossy().get_folder_info_by_id(folder_id))

@mcp.tool()
def create_folder(parent_folder_id: int, folder_name: str) -> Info:
    """Create a new folder under a parent folder
    
    Args:
        parent_folder_id: ID of the parent folder
        folder_name: Name for the new folder
    """
    return convert_root_model(ensure_fossy().create_folder_under_parent_folder_id(parent_folder_id, folder_name))

@mcp.tool()
def delete_folder(folder_id: int) -> None:
    """Delete a folder by ID
    
    Args:
        folder_id: ID of the folder to delete
    """
    return ensure_fossy().delete_folder_by_id(folder_id)

@mcp.tool()
def change_folder_name_or_desc(folder_id: int, new_folder_name: str = "", new_folder_desc: str = "") -> Info:
    """Change folder name or description
    
    Args:
        folder_id: ID of the folder to modify
        new_folder_name: New name for the folder (optional)
        new_folder_desc: New description for the folder (optional)
    """
    return convert_root_model(ensure_fossy().change_folder_name_or_desc(folder_id, new_folder_name, new_folder_desc))

@mcp.tool()
def apply_folder_action(action: str, folder_id: int, parent_folder_id: int) -> Info:
    """Apply an action (copy/move) to a folder
    
    Args:
        action: Action to apply ("copy" or "move")
        folder_id: ID of the folder to apply action to
        parent_folder_id: ID of the destination parent folder
    """
    try:
        action_enum = Action[action]
    except KeyError:
        raise ValueError(f"Invalid action: {action}. Must be one of: {', '.join([a.name for a in Action])}")
    
    return convert_root_model(ensure_fossy().apply_action_to_folderid(action_enum, folder_id, parent_folder_id))

# ==== Upload Management ====

@mcp.tool()
def get_all_uploads(
    folder_id: int,
    recursive: bool = True,
    search_pattern: str = "",
    status: str = "Open",
    assignee: str = "",
    since_date: str = "",
    page: int = 1,
    limit: int = 1000
) -> List[Upload]:
    """Get all uploads based on search criteria
    
    Args:
        folder_id: ID of the folder to search in
        recursive: Whether to search recursively in subfolders
        search_pattern: Pattern to search for in upload names
        status: Status filter (Open, InProgress, Closed, Rejected)
        assignee: Filter by assignee
        since_date: Filter by date (YYYY-MM-DD)
        page: Page number for pagination
        limit: Results per page
    """
    try:
        status_enum = ClearingStatus[status]
    except KeyError:
        raise ValueError(f"Invalid status: {status}. Must be one of: {', '.join([s.name for s in ClearingStatus])}")
    
    return convert_root_model(ensure_fossy().get_all_uploads_based_on(
        folder_id, recursive, search_pattern, status_enum, assignee, since_date, page, limit
    ))

@mcp.tool()
def get_upload_summary(upload_id: int) -> UploadSummary:
    """Get summary for an uploaded package
    
    Args:
        upload_id: ID of the upload to get summary for
    """
    return convert_root_model(ensure_fossy().get_upload_summary_for_uploadid(upload_id))

@mcp.tool()
def delete_upload(upload_id: int) -> Info:
    """Delete an upload by ID
    
    Args:
        upload_id: ID of the upload to delete
    """
    return convert_root_model(ensure_fossy().delete_uploads_by_upload_id(upload_id))

# ==== Package Upload Methods ====

@mcp.tool()
def upload_local_package(file_path: str, folder_id: int, upload_desc: str = "", visibility: str = "public") -> str:
    """Upload a local package file
    
    Args:
        file_path: Path to the local file
        folder_id: ID of the destination folder
        upload_desc: Description for the upload
        visibility: Visibility setting (public, protected, private)
    """
    try:
        visibility_enum = Public[visibility]
    except KeyError:
        raise ValueError(f"Invalid visibility: {visibility}. Must be one of: {', '.join([v.name for v in Public])}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return ensure_fossy().get_upload_id_by_local_package_upload(file_path, folder_id, upload_desc, visibility_enum)

@mcp.tool()
def upload_url_package(file_download_url: str, file_name: str, folder_id: int, upload_desc: str = "", visibility: str = "public") -> str:
    """Upload a package from URL
    
    Args:
        file_download_url: URL to download the file from
        file_name: Name for the file
        folder_id: ID of the destination folder
        upload_desc: Description for the upload
        visibility: Visibility setting (public, protected, private)
    """
    try:
        visibility_enum = Public[visibility]
    except KeyError:
        raise ValueError(f"Invalid visibility: {visibility}. Must be one of: {', '.join([v.name for v in Public])}")
    
    if not ensure_fossy().check_url_exists(file_download_url):
        raise ValueError(f"URL not accessible: {file_download_url}")
    
    return ensure_fossy().get_upload_id_by_download_url_package_upload(file_download_url, file_name, folder_id, upload_desc, visibility_enum)

@mcp.tool()
def upload_git_package(git_url: str, branch_name: str, folder_id: int, upload_name: str = "", upload_desc: str = "", visibility: str = "public") -> str:
    """Upload a package from git repository
    
    Args:
        git_url: URL of the git repository
        branch_name: Branch to clone
        folder_id: ID of the destination folder
        upload_name: Name for the upload (defaults to repository name)
        upload_desc: Description for the upload
        visibility: Visibility setting (public, protected, private)
    """
    try:
        visibility_enum = Public[visibility]
    except KeyError:
        raise ValueError(f"Invalid visibility: {visibility}. Must be one of: {', '.join([v.name for v in Public])}")
    
    if not ensure_fossy().check_url_exists(git_url):
        raise ValueError(f"Git URL not accessible: {git_url}")
    
    return ensure_fossy().get_upload_id_by_giturl_package_upload(git_url, branch_name, upload_name, folder_id, upload_desc, visibility_enum)

# ==== Analysis Methods ====

@mcp.tool()
def trigger_analysis(upload_id: int, folder_id: int) -> Info:
    """Trigger analysis for an uploaded package
    
    Args:
        upload_id: ID of the upload to analyze
        folder_id: ID of the folder containing the upload
    """
    return convert_root_model(ensure_fossy().trigger_analysis_for_upload_id(upload_id, folder_id))

@mcp.tool()
def trigger_analysis_for_package(file_path: str, folder_id: int) -> str:
    """Trigger analysis for a local package file
    
    Args:
        file_path: Path to the local file
        folder_id: ID of the destination folder
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return ensure_fossy().trigger_analysis_for_upload_package(file_path, folder_id)

@mcp.tool()
def trigger_analysis_for_url_package(file_download_url: str, file_name: str, folder_id: int) -> str:
    """Trigger analysis for a package from URL
    
    Args:
        file_download_url: URL to download the file from
        file_name: Name for the file
        folder_id: ID of the destination folder
    """
    return ensure_fossy().trigger_analysis_for_url_upload_package(file_download_url, file_name, "", folder_id)

@mcp.tool()
def trigger_analysis_for_git_package(git_url: str, branch_name: str, folder_id: int) -> str:
    """Trigger analysis for a package from git repository
    
    Args:
        git_url: URL of the git repository
        branch_name: Branch to clone
        folder_id: ID of the destination folder
    """
    return ensure_fossy().trigger_analysis_for_git_upload_package(git_url, branch_name, folder_id)

# ==== License Management ====

@mcp.tool()
def get_licenses_found_by_agents(upload_id: int, show_directories: bool = True, agents: List[str] = None) -> List[UploadLicense]:
    """Get licenses found by scanners for an upload
    
    Args:
        upload_id: ID of the upload to get licenses for
        show_directories: Whether to include directories
        agents: List of agents to include results from (empty for all)
    """
    if agents is None:
        agents = [a.name for a in Agent]
    else:
        for agent in agents:
            if agent not in [a.name for a in Agent]:
                raise ValueError(f"Invalid agent: {agent}. Must be one of: {', '.join([a.name for a in Agent])}")
    
    result = ensure_fossy().get_licenses_found_by_agents_for_uploadid(upload_id, agents, show_directories)
    return convert_root_model(result)

@mcp.tool()
def get_license_by_shortname(short_name: str) -> LicenseShortnameGetResponse:
    """Get license details by short name
    
    Args:
        short_name: Short name of the license to look up
    """
    return convert_root_model(ensure_fossy().get_license_by_short_name(short_name))

@mcp.tool()
def get_all_licenses(active_only: bool = True, license_kind: str = "main", page: int = 1, limit: int = 100) -> List[License]:
    """Get all licenses
    
    Args:
        active_only: Whether to include only active licenses
        license_kind: Kind of licenses (main, candidate, all)
        page: Page number for pagination
        limit: Results per page
    """
    try:
        kind_enum = Kind[license_kind]
    except KeyError:
        raise ValueError(f"Invalid license kind: {license_kind}. Must be one of: {', '.join([k.name for k in Kind])}")
    
    active_str = "true" if active_only else "false"
    return convert_root_model(ensure_fossy().get_all_license_based_on(active_str, kind_enum, page, limit))

@mcp.tool()
def get_license_shortnames(active_only: bool = True, license_kind: str = "main", contains: str = "", page: int = 1, limit: int = 100) -> List[str]:
    """Get license short names
    
    Args:
        active_only: Whether to include only active licenses
        license_kind: Kind of licenses (main, candidate, all)
        contains: Filter by text contained in short name
        page: Page number for pagination
        limit: Results per page
    """
    try:
        kind_enum = Kind[license_kind]
    except KeyError:
        raise ValueError(f"Invalid license kind: {license_kind}. Must be one of: {', '.join([k.name for k in Kind])}")
    
    active_str = "true" if active_only else "false"
    result = ensure_fossy().get_all_license_short_names_based_on(active_str, kind_enum, page, contains, limit)
    return result if result else []

# ==== Report Generation ====

@mcp.tool()
def generate_report(upload_id: int, report_format: str) -> Dict[str, Any]:
    """Generate and download a report for an upload
    
    Args:
        upload_id: ID of the upload to generate report for
        report_format: Format of the report (dep5, spdx2, spdx2tv, readmeoss, unifiedreport)
    """
    try:
        format_enum = ReportFormat[report_format]
    except KeyError:
        raise ValueError(f"Invalid report format: {report_format}. Must be one of: {', '.join([r.name for r in ReportFormat])}")
    
    ensure_fossy().generate_and_get_desired_report_for_uploadid(upload_id, format_enum)
    reports_dir = ensure_fossy().reports_location
    
    return {
        "status": "success",
        "message": f"Report generated in {reports_dir}",
        "location": reports_dir
    }

# ==== Search Methods ====

@mcp.tool()
def search_files(
    filename_wildcard: str,
    search_type: str,
    upload_id: int,
    tag: str = "",
    filesizemin_bytes: int = 0,
    filesizemax_bytes: int = 0,
    license: str = "",
    copyright: str = ""
) -> List[SearchResults]:
    """Search files based on various criteria
    
    Args:
        filename_wildcard: Pattern to search for in filenames (use % as wildcard)
        search_type: Type of search (Directory, File, Container)
        upload_id: ID of the upload to search in
        tag: Filter by tag
        filesizemin_bytes: Minimum file size in bytes
        filesizemax_bytes: Maximum file size in bytes
        license: Filter by license
        copyright: Filter by copyright
    """
    try:
        search_type_enum = SearchType[search_type]
    except KeyError:
        raise ValueError(f"Invalid search type: {search_type}. Must be one of: {', '.join([s.name for s in SearchType])}")
    
    results = ensure_fossy().search_files_based_on(
        filename_wildcard, search_type_enum, upload_id, tag,
        filesizemin_bytes, filesizemax_bytes, license, copyright
    )
    return convert_root_model(results)

@mcp.tool()
def get_file_by_hash(sha1: str = "", md5: str = "", sha256: str = "") -> List[File]:
    """Get file information by hash (SHA1, MD5, or SHA256)
    
    Args:
        sha1: SHA1 hash to search for
        md5: MD5 hash to search for
        sha256: SHA256 hash to search for
    """
    if not (sha1 or md5 or sha256):
        raise ValueError("At least one of sha1, md5, or sha256 must be provided")
    
    results = ensure_fossy().get_file_by_any_one_of_sha1_or_md5_or_sha256(sha1, md5, sha256)
    # This function might return a string or a list of File objects
    if isinstance(results, str):
        return []
    return convert_root_model(results)

@mcp.tool()
def get_copyrights_by_upload_id(upload_id: int) -> List[Copyright]:
    """Get copyrights for an upload
    
    Args:
        upload_id: ID of the upload to get copyrights for
    """
    return convert_root_model(ensure_fossy().get_copyrights_by_upload_id(upload_id))

# Main function to start the server
def main():
    print("Starting EasyFossy MCP Server...")
    mcp.run()

if __name__ == "__main__":
    main()  # Call main() directly instead of using asyncio.run 