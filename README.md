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

## Requirements

- **Python 3.9+** (uses structural pattern matching)
- A running FOSSology instance with REST API enabled
- Configuration file (`config.ini`) with server credentials

---

## Quick Start

### 1. Configure `config.ini`

```ini
[test]
url = http://fossology-test.com:port/repo/api/v1/
uname =
pwd =
access = write
bearer_token = Bearer YOUR_TOKEN_HERE
token_valdity_days = 365
token_expire = 2026-09-09
reports_location = reports/
group_name = fossy

[prod]
url = http://fossology.com:port/repo/api/v1/
uname =
pwd =
access = write
bearer_token = Bearer YOUR_TOKEN_HERE
token_valdity_days = 365
token_expire = 2026-09-09
reports_location = reports/
group_name = fossy
```

### 2. Kickstart

```python
from easy_fossy import easy_fossy as fossy

# Load config and get authenticated client
client = fossy('path/to/config.ini', 'test')

# Or with SSL verification
client = fossy('path/to/config.ini', 'prod', verify=True)
```

---

## API Coverage

`easy_fossy` now provides **184 methods** covering **148 endpoints** from the FOSSology REST API OpenAPI specification (~100% coverage). 

### Modular Architecture
The client is now organized into **Resource** modules for better discoverability and maintainability. You access API methods through these resource objects:

- `client.uploads` - Upload management
- `client.folders` - Folder management
- `client.jobs` - Job monitoring
- `client.licenses` - License management
- `client.users` - User management
- `client.groups` - Group management

### Usage Examples

#### Uploads
```python
# Upload a local file
upload = client.uploads.upload_file(file_path='package.zip', folder_id=1)

# Upload from Git URL
client.uploads.get_upload_id_by_giturl_package_upload(
    git_url='https://github.com/user/repo.git',
    branch_name='main',
    folder_id=1
)

# Trigger full analysis
client.jobs.trigger_analysis_for_upload_id(upload_id=4, folder_id=1)
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
licenses = client.licenses.get_all_license_based_on(is_active='true')

# Get license by short name
license_info = client.licenses.get_license_by_short_name(short_name='MIT')
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
