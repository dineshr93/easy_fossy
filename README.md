# easy_fossy

[![Snake fonts](https://see.fontimg.com/api/renderfont4/mLZ3a/eyJyIj...oxfQ/ZWFzeV9mb3NzeQ/terasong.png)](https://www.fontspace.com/category/snake) For Font credit Refer <1>

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

The repo ships a standalone Hermes skill at `skills/fossy/` — a self-contained reference for driving the FOSSology REST API through `easy_fossy`, covering all 63 resource functions plus secure token management for AI subagents. It works even where `easy_fossy` is not installed (you can replicate any call with `curl`/`requests`).

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

The test suite (`tests/`) exercises **every public API function** against a **live FOSSology instance**. It is driven entirely by environment variables — the same ones the client reads — and is skipped (not failed) in CI when those variables are absent.

### 1. Set the environment variables

```bash
export FOSSY_URL="http://fossology.com:port/repo/api/v1/"
export FOSSY_BEARER_TOKEN="Bearer YOUR_TOKEN_HERE"
export FOSSY_TOKEN_EXPIRE="2026-09-09"
export FOSSY_ACCESS="write"
export FOSSY_VERIFY="false"
```

Required: `FOSSY_URL`, `FOSSY_BEARER_TOKEN`, `FOSSY_TOKEN_EXPIRE`. Optional: `FOSSY_ACCESS`, `FOSSY_VERIFY`. If the required ones are missing, the suite is skipped rather than failing, so it is safe to run in CI where a live instance may not exist.

### 2. Install dependencies

```bash
poetry install
```

### 3. Run the suite

```bash
poetry run pytest
```

Run a single test file:

```bash
poetry run pytest tests/test_uploads.py
```

Run a single test by name:

```bash
poetry run pytest tests/test_uploads.py -k "trigger"
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
token_valdity_days = 365
token_expire = 2026-09-09
reports_location = reports/
group_name = fossy
```

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

`easy_fossy` provides **61 public API functions** across 6 resource modules, covering the core FOSSology REST API operations (uploads, folders, groups, jobs, licenses, users).

### Modular Architecture
The client is organized into **Resource** modules for better discoverability. You access API methods through these resource objects:

- `client.uploads` - Upload management
- `client.folders` - Folder management
- `client.jobs` - Job monitoring
- `client.licenses` - License management
- `client.users` - User management
- `client.groups` - Group management

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

**Licenses (`client.licenses`)**
- `get_all(is_active="true", license_kind="main", page=1, limit=100)`: List licenses based on criteria.
- `get_by_short_name(short_name)`: Get license by short name.
- `add(unique_short_name, new_full_name, new_license_text, new_url, new_risk, isCandidate=True)`: Add a new license.
- `get_histogram(upload_id)`: Get license histogram for an upload.
- `import_csv(file_path)`: Import licenses from CSV.
- `export_csv()`: Export licenses to CSV.
- `import_json(payload)`: Import licenses from JSON.
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

The `easy_fossy/usecases.py` module provides 10 high-level workflows that combine multiple API calls into single, business-relevant operations.

```python
from easy_fossy.usecases import full_package_scan_workflow

client = fossy('config.ini', 'test')
result = full_package_scan_workflow(client, file_path='package.zip', folder_id=1)
```
