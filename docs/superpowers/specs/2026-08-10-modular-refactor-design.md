# Design Specification: Modular Refactor of easy_fossy

**Date:** 2026-08-10
**Status:** Draft
**Approach:** Modular Refactor (Option 2)

## 1. Objective
Transform `easy_fossy` from a monolithic API wrapper into a modular, extensible library suitable for use as a dependency in other projects, while maintaining backward compatibility and supporting multiple FOSSology versions.

## 2. Architecture

### 2.1 Client Decomposition
The current `easy_fossy` class will be split into a coordinator client and several resource-specific clients.

- **`FossyClient`**: The main entry point. Coordinates authentication, session management, and delegates requests to resource clients.
- **`Resource` (Base Class)**: Contains the centralized `_request` helper, error handling, and base path logic.
- **Resource Clients**:
    - `UploadsResource`: Handles `/uploads`
    - `UsersResource`: Handles `/users`
    - `LicensesResource`: Handles `/licenses`
    - `JobsResource`: Handles `/jobs`
    - `GroupsResource`: Handles `/groups`
    - `FoldersResource`: Handles `/folders`

### 2.2 Configuration System
Replace `.ini` file reliance with a flexible `FossyConfig` model.

- **`FossyConfig` (Pydantic)**:
    - Supports loading from `.ini` files, environment variables, or direct Python dictionaries.
    - Handles token expiration and validity logic.
    - Stores server version to enable version-specific path adjustments.

### 2.3 Session & Request Management
- Use `requests.Session` for connection pooling and automatic header management.
- Implement a centralized `_request` method in the `Resource` base class to handle:
    - URL construction based on version.
    - Payload encoding.
    - Response parsing into Pydantic models.
    - Raising structured exceptions (`FossyAPIError`, `FossyAuthError`, etc.).

## 3. Multi-Version Compatibility
- **Versioned Paths**: Resource classes will use properties for their base paths, allowing overrides based on the configured version in `FossyConfig`.
- **Model Flexibility**: Pydantic models in `models.py` will be updated with aliases and validators to handle field name variations across versions.

## 4. Backward Compatibility & Transition

### 4.1 API Preservation
`FossyClient` will maintain all existing method names from the original `easy_fossy` class. Methods will delegate internally:
```python
def get_all_users(self):
    return self.users.get_all()
```

### 4.2 Usecase Migration
`easy_fossy/usecases.py` will be updated to use the new `FossyClient` instance without changing the high-level business logic.

## 5. Testing Strategy
- **Framework**: `pytest`.
- **Integration Tests**: Targeted at `http://localhost:8081/repo/`.
- **Mock Tests**: Using `responses` to simulate multiple FOSSology versions and API errors.
- **Regression Testing**: Ensure all 184+ existing methods still return expected data shapes.

## 6. File Structure Changes
```text
easy_fossy/
├── __init__.py       # Exposes FossyClient and models
├── client.py         # Main FossyClient implementation
├── config.py         # FossyConfig and settings
├── exceptions.py     # Custom error hierarchy
├── models.py         # Pydantic data models
├── usecases.py       # High-level workflows
└── resources/        # Resource-specific clients
    ├── __init__.py
    ├── base.py       # Base Resource class
    ├── uploads.py
    ├── users.py
    ├── licenses.py
    ├── jobs.py
    ├── groups.py
    └── folders.py
```
