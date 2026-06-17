# easy_fossy

[![Snake fonts](https://see.fontimg.com/api/renderfont4/mLZ3a/eyJyIjoiZnMiLCJoIjoxNzEsInciOjI2MjUsImZzIjo2NSwiZmdjIjoiIzAwMDAwMCIsImJnYyI6IiNGRkZGRkYiLCJ0IjoxfQ/ZWFzeV9mb3NzeQ/terasong.png)](https://www.fontspace.com/category/snake) For Font credit Refer <1>

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
bearer_token = Bearer OHNSUFaI6OtoFNz
token_valdity_days = 365
token_expire = 2022-10-29
reports_location = reports/
group_name = fossy

[prod]
url = http://fossology.com:port/repo/api/v1/
uname =
pwd =
access = write
bearer_token = Bearer OHNSUFaI6OtoFNz
token_valdity_days = 365
token_expire = 2022-10-29
reports_location = reports/
group_name = fossy
```

### 2. Kickstart

```python
from easy_fossy import easy_fossy as fossy

# Load config and get authenticated client
use_fossy_to = fossy('path/to/config.ini', 'test')

# Or with SSL verification
use_fossy_to = fossy('path/to/config.ini', 'prod', verify=True)
```

---

## API Coverage

`easy_fossy` now provides **184 methods** covering **148 endpoints** from the FOSSology REST API OpenAPI specification (~100% coverage). Methods are grouped by resource:

### Uploads (30+ methods)

Create, inspect, update, move, and delete uploads. Includes one-shot analysis.

```python
# Upload a local file
upload = use_fossy_to.upload_file(file_path='package.zip', folder_id=1)

# Upload from Git URL
use_fossy_to.get_upload_id_by_giturl_package_upload(
    git_url='https://github.com/user/repo.git',
    branch_name='main',
    folder_id=1
)

# Upload from download URL
use_fossy_to.get_upload_id_by_download_url_package_upload(
    file_download_url='https://example.com/package.zip',
    file_name='package.zip',
    folder_id=1
)

# Trigger full analysis
use_fossy_to.trigger_analysis_for_upload_id(upload_id=4, folder_id=1)

# Get upload details
upload = use_fossy_to.get_upload_by_id(upload_id=4)

# Update status/assignee
use_fossy_to.update_upload_by_id(upload_id=4, new_status='Open', new_assignee=2, comment='Reviewed')

# Move/copy upload to another folder
use_fossy_to.move_upload_by_id(upload_id=4, folder_id=2, action='copy')

# Delete upload
use_fossy_to.delete_uploads_by_upload_id(upload_id=7)

# One-shot analysis (no storage)
nomos_result = use_fossy_to.run_one_shot_nomos('sample.txt')
monk_result = use_fossy_to.run_one_shot_monk('sample.txt')
ceu_result  = use_fossy_to.run_one_shot_ceu('sample.txt')
```

### Clearing & Licensing (25+ methods)

```python
# Clearing history & progress
history = use_fossy_to.get_clearing_history(upload_id=4, item_id=0)
progress = use_fossy_to.get_clearing_progress_info(upload_id=4)

# Agents
agents = use_fossy_to.get_agents_by_upload_id(upload_id=4)
revisions = use_fossy_to.get_revisions_for_agents(upload_id=4)

# Edited vs scanned licenses
edited  = use_fossy_to.get_all_edited_licenses(upload_id=4)
scanned = use_fossy_to.get_all_scanned_licenses(upload_id=4)

# License reuse summary
reuse = use_fossy_to.get_licenses_reuse_summary(upload_id=4)

# Tree view
tree = use_fossy_to.get_item_tree_view(upload_id=4, item_id=0, flatten=True)
```

### Copyrights / Emails / URLs / Authors / ECCs / Keywords / IPRAs (50+ methods)

```python
# GET findings (active or deleted)
copyrights = use_fossy_to.get_file_copyrights(upload_id=4, item_id=0, status='active')
emails     = use_fossy_to.get_file_emails(upload_id=4, item_id=0, status='active')
urls       = use_fossy_to.get_file_urls(upload_id=4, item_id=0, status='active')
authors    = use_fossy_to.get_file_authors(upload_id=4, item_id=0, status='active')
eccs       = use_fossy_to.get_file_eccs(upload_id=4, item_id=0, status='active')
keywords   = use_fossy_to.get_file_keywords(upload_id=4, item_id=0, status='active')
ipras      = use_fossy_to.get_file_ipras(upload_id=4, item_id=0, status='active')

# Scancode variants
sc_copyrights = use_fossy_to.get_file_scancode_copyrights(upload_id=4, item_id=0)
sc_emails     = use_fossy_to.get_file_scancode_emails(upload_id=4, item_id=0)
sc_urls       = use_fossy_to.get_file_scancode_urls(upload_id=4, item_id=0)
sc_authors    = use_fossy_to.get_file_scancode_authors(upload_id=4, item_id=0)

# User copyrights
user_copyrights = use_fossy_to.get_file_user_copyrights(upload_id=4, item_id=0)

# Totals
total_copyrights      = use_fossy_to.get_total_file_copyrights(upload_id=4, item_id=0)
total_user_copyrights = use_fossy_to.get_total_file_user_copyrights(upload_id=4, item_id=0)

# DELETE / RESTORE / UPDATE for each type
use_fossy_to.delete_file_copyright(upload_id=4, item_id=0, hash_val='abc123')
use_fossy_to.restore_file_copyright(upload_id=4, item_id=0, hash_val='abc123')
use_fossy_to.update_file_copyright(upload_id=4, item_id=0, hash_val='abc123', new_content={...})

# Same pattern for: emails, urls, authors, eccs, keywords, ipras,
# scancode-copyrights, scancode-emails, scancode-urls, scancode-authors, user-copyrights
```

### License Management (20+ methods)

```python
# Search & list licenses
licenses = use_fossy_to.get_all_license_based_on(is_active='true', license_kind=Kind.main, page=1, limit=100)
short_names = use_fossy_to.get_all_license_short_names_based_on(is_active='true', license_kind=Kind.main, contains_key='gp')

# CRUD by short name
license_info = use_fossy_to.get_license_by_short_name(short_name='MIT')
use_fossy_to.add_new_license(unique_short_name='MIT-1.0', new_full_name='MIT License v1.0',
                             new_license_text='...', new_url='https://opensource.org/license/mit',
                             new_risk=2, isCandidate=True)
use_fossy_to.update_license_info_by_short_name(short_name='MIT', new_full_name='...')

# Import / Export
use_fossy_to.import_license_csv('licenses.csv')
csv_output = use_fossy_to.export_license_csv(license_id=1)
use_fossy_to.import_license_json('licenses.json')
json_output = use_fossy_to.export_license_json(license_id=1)

# Admin license candidates
candidates = use_fossy_to.get_admin_license_candidates()
use_fossy_to.delete_license_candidate_by_id(candidate_id=5)

# Admin acknowledgements
acks = use_fossy_to.get_admin_license_acknowledgements()
use_fossy_to.mutate_admin_license_acknowledgement([
    {"id": 1, "action": "enable"}
])

# Standard comments
comments = use_fossy_to.get_all_standard_license_comments()
use_fossy_to.mutate_std_comments([{"id": 1, "text": "Updated comment"}])

# Verify / Merge / Suggest
use_fossy_to.verify_license(short_name='MyLicense', parent_shortname='MIT')
use_fossy_to.merge_license(short_name='MyLicense', parent_shortname='MIT')
suggestion = use_fossy_to.get_suggested_license(reference_text='...')
```

### Users (6 methods)

```python
# Current user info
me = use_fossy_to.get_self()

# All users
users = use_fossy_to.get_all_users()

# Get by ID
user = use_fossy_to.get_user_by_id(user_id=1)

# Create / Modify / Delete
use_fossy_to.create_user({'name': 'newuser', 'email': 'user@example.com'})
use_fossy_to.modify_user_by_id(user_id=1, user_data={'email': 'new@example.com'})
use_fossy_to.delete_user_by_id(user_id=2)

# API tokens
token = use_fossy_to.create_rest_api_token({'tokenName': 'my-token', 'expiryDate': '2026-12-31'})
tokens = use_fossy_to.get_tokens_by_type(token_type='active')
```

### Jobs (8 methods)

```python
# All jobs for current user
jobs = use_fossy_to.get_all_jobs()

# Job info by ID
job = use_fossy_to.get_job_info_by_id(job_id=3)

# Jobs for a specific upload
upload_jobs = use_fossy_to.get_job_info_by_upload_id(upload_id=4)

# Admin: all jobs
all_jobs = use_fossy_to.get_all_jobs_admin(status='completed', sort='-startTime')

# Scheduler
options = use_fossy_to.get_scheduler_options_by_operation(operation_name='agent')
use_fossy_to.handle_scheduler_run({'agentNames': ['nomos']})

# Delete job
use_fossy_to.delete_job(job_id=5, queue_id=1)

# Statistics & dashboard
stats = use_fossy_to.get_job_statistics()
server_jobs = use_fossy_to.get_all_server_jobs()
```

### Folders (10 methods)

```python
# List folders
folders = use_fossy_to.get_all_folders()

# Create / Modify / Delete
use_fossy_to.create_folder_under_parent_folder_id(parent_folder_id=1, folder_name='new-folder')
use_fossy_to.change_folder_name_or_desc(folder_id=3, new_folder_name='updated', new_folder_desc='...')
use_fossy_to.delete_folder_by_id(folder_id=3)

# Folder info
info = use_fossy_to.get_folder_info_by_id(folder_id=11)

# Actions
use_fossy_to.apply_action_to_folderid(actions=Action.move, folder_id=6, parent_folder_id=2)

# Contents
contents = use_fossy_to.get_all_folder_contents(folder_id=11)
unlinkable = use_fossy_to.get_unlinkable_contents(folder_id=11)
use_fossy_to.unlink_content(content_id=5)
```

### Groups (7 methods)

```python
# List groups
groups = use_fossy_to.get_groups()

# Deletable groups
deletable = use_fossy_to.get_deletable_groups()

# Delete group
use_fossy_to.delete_group_by_id(group_id=3)

# Members
members = use_fossy_to.get_group_users_with_roles(group_id=1)
use_fossy_to.add_group_member(group_id=1, user_id=2, member_data={'perm': 'read'})
use_fossy_to.delete_group_member(group_id=1, user_id=2)
use_fossy_to.update_group_permission(group_id=1, user_id=2, permission_data={'perm': 'write'})
```

### Reports (2 methods)

```python
# Generate report
report = use_fossy_to.generate_and_get_desired_report_for_uploadid(
    upload_id=3, report_format=ReportFormat.unifiedreport)

# Import external report
use_fossy_to.upload_report(upload_id=3, report_format='SPDX', file_path='report.spdx')
```

### Search (2 methods)

```python
# Search files
results = use_fossy_to.search_files_based_on(
    filename_wildcard='draw%', search_type=SearchType.Directory,
    upload_id=4, tag='', filesizemin_bytes=0, filesizemax_bytes=0,
    license='', copyright='')

# Find file by hash
file = use_fossy_to.get_file_by_any_one_of_sha1_or_md5_or_sha256(
    sha1='abc123...', md5='', sha256='')
```

### Upload Conf (2 methods)

```python
conf = use_fossy_to.get_conf_info(upload_id=4)
use_fossy_to.update_conf_data(upload_id=4, {'key': 'value'})
```

### Overview / Admin (5 methods)

```python
db_contents = use_fossy_to.get_database_contents()
php_info    = use_fossy_to.get_php_info()
disk_usage  = use_fossy_to.get_disk_usage()
metrics     = use_fossy_to.get_database_metrics()
queries     = use_fossy_to.get_active_queries()
```

### Customise (3 methods)

```python
data   = use_fossy_to.get_customise_data()
use_fossy_to.update_customise_data({'key': 'value'})
banner = use_fossy_to.get_banner_message()
```

---

## Business-Relevant Utility Functions

The `easy_fossy/usecases.py` module provides 10 high-level workflows that combine multiple API calls into single, business-relevant operations.

```python
from easy_fossy.usecases import (
    full_package_scan_workflow,
    license_audit_report,
    clearing_status_dashboard,
    compliance_report_generation,
    user_audit_trail,
    folder_inventory,
    package_analysis_summary,
    license_candidate_review,
    job_dashboard_monitor,
    group_membership_audit,
)

client = fossy('config.ini', 'test')
```

### 1. Full Package Scan Workflow

Upload a package, schedule scans (nomos, monk, copyright), wait for completion, and collect all results:

```python
result = full_package_scan_workflow(
    client,
    file_path='package.zip',
    folder_id=1,
    scan_types=['nomos', 'monk', 'copyright'],
    poll_interval=2.0,
    timeout=300.0,
)
```

### 2. License Audit Report

Compare edited vs scanned licenses, identify unmatched/pending decisions:

```python
report = license_audit_report(client, upload_id=4, item_id=0)
```

### 3. Clearing Status Dashboard

Consolidated view of clearing progress, agents, revisions, and license reuse:

```python
dashboard = clearing_status_dashboard(client, upload_id=4)
```

### 4. Compliance Report Generation

License reuse summary data for compliance reporting:

```python
report = compliance_report_generation(client, upload_id=4, report_format='PDF')
```

### 5. User Audit Trail

Get user details, their jobs, and group memberships:

```python
audit = user_audit_trail(client)
```

### 6. Folder Inventory

Get folder contents with all uploads, their licenses, and status:

```python
inventory = folder_inventory(client, folder_id=1, include_licenses=True)
```

### 7. Package Analysis Summary (One-Shot)

Run nomos, monk, and CEU analysis on a file without uploading:

```python
summary = package_analysis_summary(client, file_path='sample.txt')
```

### 8. License Candidate Review (Admin)

Review pending license candidates and manage acknowledgements:

```python
review = license_candidate_review(client, acknowledge=[{"id": 1, "action": "enable"}])
```

### 9. Job Dashboard Monitor

Monitor all jobs, get statistics, filter by status:

```python
monitor = job_dashboard_monitor(client, status_filter='completed')
```

### 10. Group Membership Audit

List all groups with their members and permissions:

```python
audit = group_membership_audit(client)
for entry in audit:
    print(f"Group: {entry['group'].groupName}, Members: {len(entry['members'])}")
```

---

## Legacy Methods (v1.0.x)

Methods from earlier releases remain supported for backward compatibility:

```python
# 1.0.6+
use_fossy_to.get_all_license_based_on(is_active='true', license_kind=Kind.main, page=1, limit=1)
use_fossy_to.get_all_license_short_names_based_on(is_active='true', license_kind=Kind.main, contains_key='gp', page=1, limit=10000)

# 1.0.9+
use_fossy_to.get_license_by_short_name(short_name='AGPL-1.0')
use_fossy_to.add_new_license(unique_short_name='...', new_full_name='...', new_license_text='...',
                              new_url='', new_risk=2, isCandidate=True, merge_request=False)
use_fossy_to.update_license_info_by_short_name(short_name='...', new_full_name='...', new_license_text='...',
                                                new_url='', new_risk=2)
```

---

## Publishing

```bash
twine upload --repository pypi dist/* --config-file .pypirc
```

---

## License

MIT License

```
MIT License

Copyright (c) 2021 Dinesh Ravi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<1>
Font by Tehisa by Sealoung
https://www.fontspace.com/category/snake
License: Personal Use Free
