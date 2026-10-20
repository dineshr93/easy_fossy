# easy_fossy



Accessing the FOSSology REST API made easy (requires Python 3.10+).

[Production Index Registry](https://pypi.org/project/easy-fossy/)

[Test Index Registry](https://test.pypi.org/project/easy-fossy/)

---

## Installation

### From PyPI (Recommended)

```bash
pip install easy-fossy
```

### From GitHub Releases

1. Go to the [Releases](https://github.com/dineshr93/easy_fossy/releases) page
2. Download the appropriate wheel file (`.whl`) for your platform
3. Install using pip:

```bash
pip install path/to/downloaded/file.whl
```

### Manual Installation from Source

1. Clone the repository:

```bash
git clone https://github.com/dineshr93/easy_fossy.git
cd easy_fossy
```

2. Install using Poetry (recommended):

```bash
pip install poetry
poetry install
```

3. Or install using pip:

```bash
pip install .
```

---

## Hermes Agent Skill (reusable)

The repo ships a standalone Hermes skill at `skills/fossy/` — a self-contained reference for driving the FOSSology REST API through `easy_fossy`, covering all 78 resource functions plus secure token management for AI subagents. It works even where `easy_fossy` is not installed (you can replicate any call with `curl`/`requests`).

### Install from this repo (Hermes CLI)

```bash
# 1. Add this repo as a skill source (tap)
hermes skills tap add dineshr93/easy_fossy

# 2. Install the skill
hermes skills install dineshr93/easy_fossy/fossy
```

### Install directly from a SKILL.md URL

```bash
hermes skills install https://raw.githubusercontent.com/dineshr93/easy_fossy/master/skills/fossy/SKILL.md --name fossy
```

### Install from the GitHub Releases wheel (client only)

If you want the `easy_fossy` Python client without the skill:

```bash
pip install path/to/easy_fossy-2.5.0-py3-none-any.whl
```

---

## Requirements

- **Python 3.9+** (uses structural pattern matching)
- A running FOSSology instance with REST API enabled
- Credentials (either via `config.ini` or Environment Variables)

---

## Running the Test Suite

The suite has two layers:

- **Offline suite (default)** — every resource and workflow runs through the transport seam against an in-memory stub session: no instance, no network, ~0.1 s. This is what CI runs.
- **Live suite (`pytest -m live`)** — the same methods against a real FOSSology instance, driven by the `FOSSY_*` environment variables. Skipped (not failed) when they are absent.

### 1. Offline suite

```bash
poetry install
poetry run pytest
```

### 2. Live suite

Set the environment variables (the same ones the client reads):

```bash
export FOSSY_URL="http://fossology.com:port/repo/api/v1/"
export FOSSY_BEARER_TOKEN="Bearer YOUR_TOKEN_HERE"
export FOSSY_TOKEN_EXPIRE="2026-09-09"
export FOSSY_ACCESS="write"
export FOSSY_VERIFY="false"
```

Required: `FOSSY_URL`, `FOSSY_BEARER_TOKEN`, `FOSSY_TOKEN_EXPIRE`. Optional: `FOSSY_ACCESS`, `FOSSY_VERIFY`. If the required ones are missing, the live tests skip rather than fail.

```bash
poetry run pytest -m live
```

Run a single live test file, or a single test by name:

```bash
poetry run pytest -m live tests/test_uploads.py
poetry run pytest -m live tests/test_uploads.py -k "trigger"
```

> **Note:** Prefer `poetry run pytest` over `make test`. The `make test` target uninstalls/reinstalls the package via `pip3` against the system Python, which fails with a PEP 668 "externally-managed-environment" error on most modern distros.

> **Note:** The suite creates and cleans up temporary folders and uploads on the live instance. `temp_folder` removes its folder via per-test teardown, and an autouse session fixture sweeps any leftover `suite_*` folders at the end of the run — so even if a test fails mid-way, orphans are cleaned up automatically. If you ever see leftover `suite_folder_*` folders anyway (e.g. the instance was unreachable at teardown), they are test artifacts and safe to delete.

---

## Quick Start

You can configure the client in two ways: using a configuration file or environment variables.

### Option 1: Using `config.ini` (File-based)

**1. Configure `config.ini`**

```ini
[test]
url = http://fossology-test.com:port/repo/api/v1/
uname = your_username
pwd = your_password
access = write
bearer_token = Bearer YOUR_TOKEN_HERE
token_validity_days = 365
token_expire = 2026-09-09
reports_location = reports/
group_name = fossy
```

> `token_valdity_days` (the historical typo) is still accepted from existing ini files and env vars, but new writes use `token_validity_days`.

**2. Kickstart**

```python
from easy_fossy import easy_fossy as fossy

# Load config and get authenticated client
client = fossy('path/to/config.ini', 'test')

# Or with SSL verification
client = fossy('path/to/config.ini', 'prod', verify=True)
```

---

### Option 2: Using Environment Variables (Cloud/Docker)

This method is ideal for CI/CD pipelines, Docker containers, or cloud deployments where you prefer not to store credentials in files.

**1. Set Environment Variables**

```bash
export FOSSY_URL="http://fossology.com:port/repo/api/v1/"
export FOSSY_BEARER_TOKEN="Bearer YOUR_TOKEN_HERE"
export FOSSY_TOKEN_EXPIRE="2026-09-09"
export FOSSY_ACCESS="write"
export FOSSY_VERIFY="false"
```

**2. Kickstart**

```python
from easy_fossy.client import FossyClient

# Initialize the client directly from environment variables
client = FossyClient.from_env(verify=False)
```

---

## API Coverage

`easy_fossy` provides **78 public API functions** across 6 resource modules, covering the core FOSSology REST API operations (uploads, folders, groups, jobs, licenses, users).

### Modular Architecture
The client is organized into **Resource** modules for better discoverability. You access API methods through these resource objects:

- `client.uploads` - Upload management
- `client.folders` - Folder management
- `client.jobs` - Job monitoring
- `client.licenses` - License management
- `client.users` - User management
- `client.groups` - Group management

One `Transport` module (`easy_fossy/transport.py`) builds every URL, maps status codes onto the exception hierarchy, and fetches the bearer token lazily on the first request. Constructing a client performs no I/O; tests swap the transport's session for an in-memory stub.

#### Available Functions

**Uploads (`client.uploads`)**
- `upload_file(file_path, folder_id)`: Upload a local file.
- `upload_by_url(url, folder_id)`: Upload a file from a URL.
- `upload_by_giturl(giturl, folder_id)`: Upload a package from a Git URL.
- `get_upload_by_id(upload_id)`: Get upload details by ID.
- `trigger_analysis_for_upload_id(upload_id, folder_id)`: Trigger full analysis.
- `delete_uploads_by_upload_id(upload_id)`: Delete an upload.
- `get_upload_tree_id_by_upload_id(upload_id)`: Get the top-level item ID for an upload.
- `get_copyrights_by_upload_id_uploadtree_id(upload_id, upload_tree_id)`: Get copyrights for a specific item.
- `get_all_uploads(folder_id=None, page=1, limit=100)`: List uploads, optionally by folder.
- `get_copyrights(upload_id)`: Get every copyright finding for an upload.
- `get_clearing_progress_info(upload_id)`: Clearing progress for an upload.
- `get_clearing_history(upload_id, item_id)`: Clearing history for one upload item.
- `get_agents_by_upload_id(upload_id)`: Agents that ran on an upload.
- `get_revisions_for_agents(upload_id)`: Agent revisions for an upload.
- `get_all_edited(upload_id)`: Licenses with a clearing decision.
- `get_all_scanned(upload_id)`: Licenses found by scanners.
- `get_reuse_summary(upload_id)`: License reuse summary.
- `get_license_histogram(upload_id, agent_id=None)`: License histogram (owned here, `client.licenses.get_histogram` delegates).
- `run_one_shot_nomos(file_path)` / `run_one_shot_monk(file_path)` / `run_one_shot_ceu(file_path)`: Scan a local file without uploading.

**Folders (`client.folders`)**
- `get_all()`: List all folders.
- `get_by_id(folder_id)`: Get folder info by ID.
- `create(parent_folder_id, folder_name)`: Create a folder under a parent.
- `delete(folder_id)`: Delete a folder.
- `update(folder_id, folder_name, folder_desc)`: Update folder name or description.
- `move(folder_id, target_folder_id)`: Move folder to a target parent.
- `unlink_content(content_id)`: Unlink content from a folder.
- `get_contents(folder_id)`: Get all folder contents.
- `get_unlinkable_contents(folder_id)`: Get unlinkable contents.

**Groups (`client.groups`)**
- `get_all()`: List all groups.
- `delete(group_id)`: Delete a group by ID.
- `get_users_with_roles(group_id)`: Get group users and their roles.
- `create(group_name, group_desc=None)`: Create a new user group.
- `add_member(group_id, user_id)`: Add a member to a group.
- `delete_member(group_id, user_id)`: Remove a member from a group.
- `update_permission(group_id, user_id, permission)`: Update group permission for a user.
- `get_deletable()`: Get list of deletable groups.

**Jobs (`client.jobs`)**
- `get_all(upload_id=None, status=None, limit=1000, page=1)`: List jobs (filterable by upload/status).
- `get_by_id(job_id)`: Get job info by ID.
- `delete(job_id, queue_id=1)`: Delete a job.
- `get_all_admin()`: Get all jobs (admin view).
- `get_scheduler_options(operation_name)`: Get scheduler options by operation.
- `handle_scheduler_run(payload)`: Handle scheduler run.
- `get_statistics()`: Get job statistics.
- `get_all_server_jobs()`: Get all server jobs.
- `schedule_analysis(upload_id, folder_id, analysis=None)`: Schedule an analysis run for an upload.
- `schedule_agent(upload_id, agents, folder_id=None)`: Schedule one job per named agent (folder looked up when omitted).

**Licenses (`client.licenses`)**
- `get_all(is_active="true", license_kind="main", page=1, limit=100)`: List licenses based on criteria.
- `get_by_short_name(short_name)`: Get license by short name.
- `add(unique_short_name, new_full_name, new_license_text, new_url, new_risk, isCandidate=True)`: Add a new license.
- `get_histogram(upload_id, agent_id=None)`: Get license histogram for an upload (delegates to `client.uploads`).
- `import_csv(file_path)`: Import licenses from CSV.
- `export_csv()`: Export licenses to CSV.
- `import_json(file_path)`: Import licenses from a JSON file.
- `export_json()`: Export licenses to JSON.
- `update(short_name, payload)`: Update license info.
- `get_admin_candidates()`: Get admin license candidates.
- `delete_candidate(candidate_id)`: Delete license candidate by ID.
- `get_admin_acknowledgements()`: Get admin acknowledgements.
- `mutate_acknowledgement(payload)`: Mutate admin acknowledgement.
- `get_standard_comments()`: Get all standard license comments.
- `mutate_std_comments(payload)`: Mutate standard comments.
- `verify(short_name)`: Verify a license.
- `merge(short_name)`: Merge a license.
- `suggest(payload)`: Get suggested license.

**Users (`client.users`)**
- `get_all(limit=1000, page=1)`: List all users.
- `get_by_id(user_id)`: Get user details by ID.
- `create(payload)`: Create a new user.
- `update(user_id, payload)`: Modify user by ID.
- `delete(user_id)`: Delete user by ID.
- `get_self()`: Get current user info.
- `create_token(payload)`: Create a REST API token.
- `get_tokens(token_type)`: Get tokens by type.

### Usage Examples

#### Uploads
```python
# Upload a local file
upload = client.uploads.upload_file(file_path='package.zip', folder_id=1)

# Upload from Git URL
client.uploads.upload_by_giturl(giturl='https://github.com/user/repo.git', folder_id=1, branch='main')

# Trigger full analysis
client.uploads.trigger_analysis_for_upload_id(upload_id=upload.id, folder_id=1)
```

#### Folders
```python
# List all folders
folders = client.folders.get_all()

# Create folder
client.folders.create(parent_folder_id=1, folder_name='new-folder')
```

#### Licenses
```python
# Search licenses
licenses = client.licenses.get_all(is_active='true')

# Get license by short name
license_info = client.licenses.get_by_short_name(short_name='MIT')
```

*(Note: Backward compatibility methods are still available directly on the `client` object for common operations.)*

---

## Business-Relevant Utility Functions

The `easy_fossy/usecases.py` module provides 10 high-level workflows that combine multiple API calls into single, business-relevant operations. They call only documented resource methods, and a failure raises `FossyAPIError` instead of returning a half-filled payload.

- `full_package_scan_workflow(client, file_path, folder_id)` — upload, schedule scans, wait, return licenses + copyrights.
- `license_audit_report(client, upload_id)` — edited vs scanned licenses, unmatched set, clearing progress.
- `clearing_status_dashboard(client, upload_id)` — progress, agents, revisions, reuse in one payload.
- `compliance_report_generation(client, upload_id, report_format="dep5")` — reuse summary plus the downloaded report bytes.
- `user_audit_trail(client, user_id=None)` — user, jobs, groups.
- `folder_inventory(client, folder_id, include_licenses=False)` — folder contents with per-upload licenses.
- `package_analysis_summary(client, file_path)` — nomos, monk and CEU one-shot scans, no upload.
- `license_candidate_review(client, acknowledge=None)` — admin candidates, acknowledgements, standard comments.
- `job_dashboard_monitor(client, status_filter=None)` — jobs, statistics, server jobs.
- `group_membership_audit(client)` — every group with its members.

```python
from easy_fossy.client import FossyClient
from easy_fossy.usecases import full_package_scan_workflow

client = FossyClient.from_env()
result = full_package_scan_workflow(client, file_path='package.zip', folder_id=1)
```
