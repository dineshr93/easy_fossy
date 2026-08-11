---
name: fossy
description: Call the FOSSology REST API via easy_fossy's 60 functions.
category: api-clients
version: 1.0.0
author: Dinesh (dineshr93), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fossology, rest, api, easy_fossy, license-scanning]
    related_skills: []
---

# fossy — FOSSology REST API Skill

Self-contained reference for driving the **FOSSology** license-analysis REST API through the `easy_fossy` Python client. It maps all **60 public resource functions** (plus the client constructors and backward-compat wrappers) to their exact HTTP calls, and documents secure token management for AI subagents. It works even on a machine where `easy_fossy` is **not installed** — you can replicate any call with `curl` or `requests`.

## When to Use

- The task involves the FOSSology REST API: uploads, folders, groups, jobs, licenses, or users.
- You need to know how to call a specific easy_fossy function, or the REST call behind it.
- You're on a machine without `easy_fossy` and must drive the API directly.
- An AI subagent needs scoped REST tokens rather than shared credentials.
- Don't use for: non-FOSSology HTTP APIs, or FOSSology CLI/UI workflows.

## Prerequisites

- A live FOSSology instance with REST enabled (`/repo/api/v1/`).
- Credentials as env vars OR a `config.ini`. If using the library:
  ```
  export FOSSY_URL="http://host:port/repo/api/v1/"
  export FOSSY_BEARER_TOKEN="Bearer YOUR_TOKEN"
  export FOSSY_TOKEN_EXPIRE="2026-09-09"
  export FOSSY_ACCESS="write"
  export FOSSY_VERIFY="false"
  ```
- Install the client. Recommended way to get it on a fresh machine (PyPI lags the repo — latest published 2.4.13 vs local 2.5.0, so pip-install from source):
  ```
  git clone https://github.com/dineshr93/easy_fossy.git
  cd easy_fossy
  pip install .
  ```
  or for local dev: `poetry install` in the repo, then `poetry run`.

## Client Setup

```python
# Library present
from easy_fossy.client import FossyClient
client = FossyClient.from_env(verify=False)      # env vars

# Or with a config.ini
from easy_fossy import easy_fossy
client = easy_fossy('config.ini', 'test', verify=False)

# Backward-compat wrappers on client: upload_file, get_upload_by_id,
# get_all_users, get_user_by_id, get_all_jobs, get_job_info_by_id
```

The six resource objects: `client.uploads`, `client.folders`, `client.groups`, `client.jobs`, `client.licenses`, `client.users`.

## Token Management (AI subagents)

For subagents, issue a **scoped, expiring REST token** instead of sharing the admin credential. Completion criterion: each subagent gets its own `token_name`/`token_scope`, and tokens are revoked after the job.

1. Create a token via the client (`POST /users/tokens`, body `token_name`/`token_scope`/`token_expire`).
2. Export it to the subagent as `FOSSY_BEARER_TOKEN="Bearer <token>"` plus `FOSSY_TOKEN_EXPIRE`.
3. On job end, delete the token with `client.users.delete(...)` or let it expire. Never write tokens to a committed file.

## Quick Reference (60 resource functions)

**uploads** — POST /uploads multipart `fileInput`, headers `folderId` + `uploadType=file` → `upload_file(file_path, folder_id)`; returns `Info{code,message=upload_id}`.
- `upload_by_url(url, folder_id, scan_options=None)` → POST /uploads, headers `folderId`+`uploadType=url`, JSON `{"location":{"url":...},"scanOptions":{analysis:{...}}}`
- `upload_by_giturl(giturl, folder_id, branch=None)` → POST /uploads, `uploadType=vcs`, JSON `{"location":{"vcsType":"git","vcsUrl":...,"vcsBranch":...}}`
- `get_upload_by_id(upload_id)` → GET /uploads/{id}
- `get_all_uploads(folder_id=None, page=1, limit=100)` → GET /uploads?folderId=, headers page/limit
- `trigger_analysis_for_upload_id(upload_id, folder_id)` → POST /jobs, headers folderId+uploadId, JSON `{"analysis":{nomos,monk,copyright_email_author,mime,keyword,bucket}}` (path is API root `/jobs`, not /uploads)
- `delete_uploads_by_upload_id(upload_id)` → DELETE /uploads/{id}
- `get_upload_tree_id_by_upload_id(upload_id)` → GET /uploads/{id}/topitem
- `get_copyrights_by_upload_id_uploadtree_id(upload_id, upload_tree_id)` → GET /uploads/{id}/item/{itemId}/copyrights?status=active

**folders**
- `get_all()` → GET /folders
- `get_by_id(folder_id)` → GET /folders/{id}
- `create(parent_folder_id, folder_name, folder_description=None)` → POST /folders, headers parentFolder/folderName/folderDescription
- `delete(folder_id)` → DELETE /folders/{id} (202, idempotent)
- `update(folder_id, folder_name, folder_desc)` → PATCH /folders/{id}, headers name/description
- `move(folder_id, target_folder_id)` → PUT /folders/{id}, headers parent + action=move
- `unlink_content(content_id)` → PUT /folders/contents/{content_id}/unlink
- `get_contents(folder_id)` → GET /folders/{id}/contents
- `get_unlinkable_contents(folder_id)` → GET /folders/{id}/contents/unlinkable

**groups**
- `get_all()` → GET /groups
- `delete(group_id)` → DELETE /groups/{id}
- `get_users_with_roles(group_id)` → GET /groups/{id}/members
- `create(group_name, group_desc=None)` → POST /groups, headers name/description
- `add_member(group_id, user_id)` → POST /groups/{id}/user/{user_id}
- `delete_member(group_id, user_id)` → DELETE /groups/{id}/user/{user_id}
- `update_permission(group_id, user_id, permission)` → PUT /groups/{id}/user/{user_id}, JSON `{"permission":...}`
- `get_deletable()` → GET /groups/deletable

**jobs**
- `get_all(upload_id=None, status=None, limit=1000, page=1)` → GET /jobs?limit&page&groupName&upload&status
- `get_by_id(job_id)` → GET /jobs/{id}
- `delete(job_id, queue_id=1)` → DELETE /jobs/{id}/{queue}
- `get_all_admin()` → GET /jobs/all
- `get_scheduler_options(operation_name)` → GET /jobs/scheduler/operation/{operation_name}
- `handle_scheduler_run(payload)` → POST /jobs/scheduler/operation/run
- `get_statistics()` → GET /jobs/dashboard/statistics
- `get_all_server_jobs()` → GET /jobs/dashboard

**licenses** (base_path `license`, singular)
- `get_all(is_active="true", license_kind="main", page=1, limit=100)` → GET /license?is_active&license_kind&page&limit
- `get_by_short_name(short_name)` → GET /license/{shortName}
- `add(unique_short_name, new_full_name, new_license_text, new_url, new_risk, isCandidate=True)` → POST /license, JSON `{shortName,fullName,text,url,risk,mergeRequest}`
- `get_histogram(upload_id, agent_id=None)` → GET /uploads/{id}/licenses/histogram?agentId (API root path)
- `import_csv(file_path, delimiter=",", enclosure='"')` → POST /license/import-csv multipart file_input/delimiter/enclosure
- `export_csv()` → GET /license/export-csv (returns text/csv, not JSON)
- `import_json(file_path)` → POST /license/import-json multipart fileInput
- `export_json()` → GET /license/export-json
- `update(short_name, payload)` → PATCH /license/{shortName}
- `get_admin_candidates()` → GET /license/admincandidates
- `delete_candidate(candidate_id)` → DELETE /license/admincandidates/{candidate_id}
- `get_admin_acknowledgements()` → GET /license/adminacknowledgements
- `mutate_acknowledgement(payload)` → PUT /license/adminacknowledgements
- `get_standard_comments()` → GET /license/stdcomments
- `mutate_std_comments(payload)` → PUT /license/stdcomments
- `verify(short_name, parent_shortname=None)` → PUT /license/verify/{shortname} JSON `{parentShortname}`
- `merge(short_name, parent_shortname=None)` → PUT /license/merge/{shortname} JSON `{parentShortname}`
- `suggest(payload)` → POST /license/suggest

**users**
- `get_all(limit=1000, page=1)` → GET /users?limit&page&groupName
- `get_by_id(user_id)` → GET /users/{id}
- `create(payload)` → POST /users
- `update(user_id, payload)` → PUT /users/{id}
- `delete(user_id)` → DELETE /users/{id}
- `get_self()` → GET /users/self
- `create_token(payload)` → POST /users/tokens  (body: token_name/token_scope/token_expire)
- `get_tokens(token_type)` → GET /users/tokens/{token_type}  (active|expired)

## Procedure (raw REST when the library is absent)

1. **Auth** — POST `{url}tokens` JSON `{username,password,token_name,token_scope,token_expire}` → returns `Authorization` header value to send as `Bearer ...`.
2. **Base URL** — every path below is relative to `FOSSY_URL` (e.g. `.../repo/api/v1/`). Never double-slash: `/uploads/` and `/uploads//5` → 404.
3. **Uploads** — POST `/uploads` with `folderId` + `uploadType` headers. Response `Info{code:201,message:<upload_id>}`. Poll GET `/uploads/{id}` (transiently 503 until ununpack starts) and `/jobs?upload=<id>`.
4. **Folders/groups create** — FOSSology passes name/parent/description as **headers**, not body.
5. **Delete** — DELETE returns 202 and schedules a job; verify with a follow-up GET list.
6. **License histogram/edited/scanned** — paths live under `/uploads/...`, not `/license/...`.

## Pitfalls

- Server rejects trailing/double slashes (`/uploads/`, `/uploads//5` → 404 "Unable to find the path").
- GET `/uploads/{id}` returns transient 503 "Ununpack job not started" — poll `/jobs?upload=<id>`.
- `license` base_path is singular; `uploads`/`folders`/`groups`/`jobs`/`users` are plural.
- `export_csv` returns raw text, not JSON; `export_json` returns JSON.
- `import_json` and `import_csv` use multipart; field names differ (`file_input` vs `fileInput`) — keep them distinct.
- `get_histogram`, `trigger_analysis_for_upload_id`, and copyright paths are relative to the API root, not their resource base_path.
- Tests create `suite_folder_*`/`suite_*` artifacts; failed teardowns can leave them behind.
- `usecases.py` references some not-yet-implemented methods (`schedule_agent`, `get_all_edited`, etc.) — do not trust it as a function reference; use the Quick Reference above.
- `pip install easy-fossy` pulls from PyPI, which lags the repo (latest published 2.4.13 vs local 2.5.0). Install from the git repo to get current source.

## Verification

- For a library call: `poetry run python -c "from easy_fossy import FossyClient; c=FossyClient.from_env(verify=False); print(len(c.folders.get_all()))"` returns a number ≥ 1.
- For a raw REST call: `curl -s -H "Authorization: Bearer $TOKEN" $FOSSY_URL/folders` returns a JSON array.
- After a DELETE, re-list to confirm the item is gone.
