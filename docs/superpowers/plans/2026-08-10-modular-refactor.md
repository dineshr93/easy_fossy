# Modular Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Decompose the monolithic `easy_fossy` client into a modular resource-based architecture to improve extensibility and maintainability.

**Architecture:** A coordinator `FossyClient` delegates to resource-specific classes (e.g., `UploadsResource`). A centralized `_request` method handles versioning and errors.

**Tech Stack:** Python 3.10+, Pydantic v2, Requests.

**Spec:** docs/superpowers/specs/2026-08-10-modular-refactor-design.md

## Global Constraints
- Maintain backward compatibility for all existing public method names.
- No `sys.exit(1)` or `print` for error handling; use custom exceptions.
- Every task must be verified against the local instance at `http://localhost:8081/repo/`.
- Frequent commits after each task.

---

## Phase 1: Foundation

### Task 1: Exception Hierarchy
**Files:**
- Create: `easy_fossy/exceptions.py`

**Interfaces:**
- Produces: `FossyError`, `FossyAPIError`, `FossyAuthError`, `FossyConnectionError`.

- [ ] **Step 1: Define exception classes**
```python
class FossyError(Exception): pass
class FossyAPIError(FossyError): pass
class FossyAuthError(FossyAPIError): pass
class FossyConnectionError(FossyError): pass
```
- [ ] **Step 2: Commit**
```bash
git add easy_fossy/exceptions.py
git commit -m "refactor: add custom exception hierarchy"
```

### Task 2: Configuration System
**Files:**
- Create: `easy_fossy/config.py`
- Modify: `easy_fossy/models.py` (add Version enum)

**Interfaces:**
- Produces: `FossyConfig` Pydantic model.

- [ ] **Step 1: Define Version enum in models.py**
- [ ] **Step 2: Implement FossyConfig with from_ini, from_env methods**
- [ ] **Step 3: Test config loading with a sample .ini**
- [ ] **Step 4: Commit**
```bash
git add easy_fossy/config.py easy_fossy/models.py
git commit -m "refactor: implement modular configuration system"
```

### Task 3: Base Resource Class
**Files:**
- Create: `easy_fossy/resources/base.py`

**Interfaces:**
- Consumes: `FossyConfig`, `requests.Session`
- Produces: `Resource` base class with `_request` method.

- [ ] **Step 1: Implement Base Resource and _request helper**
```python
class Resource:
    def __init__(self, client):
        self.client = client
        self.config = client.config

    def _request(self, method, path, **kwargs):
        # Centralized request logic with error handling
        pass
```
- [ ] **Step 2: Commit**
```bash
git add easy_fossy/resources/base.py
git commit -m "refactor: add base resource class with request helper"
```

---

## Phase 2: Resource Migration

### Task 4: User Resource
**Files:**
- Create: `easy_fossy/resources/users.py`
- Modify: `easy_fossy/__init__.py` (remove user methods)

**Interfaces:**
- Produces: `UsersResource` with `get_all()` and `get_by_id(user_id)`.

- [ ] **Step 1: Implement UsersResource inheriting from Resource**
- [ ] **Step 2: Migrate get_all_users and get_user_by_id logic**
- [ ] **Step 3: Verify against localhost:8081**
- [ ] **Step 4: Commit**
```bash
git add easy_fossy/resources/users.py easy_fossy/__init__.py
git commit -m "refactor: migrate user endpoints to UsersResource"
```

### Task 5: Upload Resource
**Files:**
- Create: `easy_fossy/resources/uploads.py`
- Modify: `easy_fossy/__init__.py` (remove upload methods)

**Interfaces:**
- Produces: `UploadsResource`.

- [ ] **Step 1: Implement UploadsResource**
- [ ] **Step 2: Migrate upload_file, get_upload_by_id, etc.**
- [ ] **Step 3: Verify against localhost:8081**
- [ ] **Step 4: Commit**
```bash
git add easy_fossy/resources/uploads.py easy_fossy/__init__.py
git commit -m "refactor: migrate upload endpoints to UploadsResource"
```

*(Note: Repeat similar tasks for Jobs, Licenses, Groups, and Folders resources)*

---

## Phase 3: Client Integration

### Task 6: FossyClient Coordinator
**Files:**
- Create: `easy_fossy/client.py`
- Modify: `easy_fossy/__init__.py`

**Interfaces:**
- Produces: `FossyClient` class.

- [ ] **Step 1: Implement FossyClient with session and resource initialization**
- [ ] **Step 2: Implement delegation methods to maintain backward compatibility**
```python
def get_all_users(self):
    return self.users.get_all()
```
- [ ] **Step 3: Implement token refresh logic in client**
- [ ] **Step 4: Commit**
```bash
git add easy_fossy/client.py easy_fossy/__init__.py
git commit -m "refactor: implement FossyClient coordinator"
```

---

## Phase 4: Verification & Cleanup

### Task 7: Usecase Migration
**Files:**
- Modify: `easy_fossy/usecases.py`

**Interfaces:**
- Consumes: `FossyClient`

- [ ] **Step 1: Update usecase function signatures to expect FossyClient**
- [ ] **Step 2: Verify all 10 usecases against localhost:8081**
- [ ] **Step 3: Commit**
```bash
git add easy_fossy/usecases.py
git commit -m "refactor: update usecases to use new Modular Client"
```

### Task 8: Full Integration Test Suite
**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_modular_client.py`

- [ ] **Step 1: Setup pytest fixtures for local instance**
- [ ] **Step 2: Write tests covering key paths of all resources**
- [ ] **Step 3: Run `pytest tests/` and verify all PASS**
- [ ] **Step 4: Final Commit**
```bash
git add tests/
git commit -m "test: add comprehensive integration test suite"
```
