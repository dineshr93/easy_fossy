"""
Shared pytest fixtures for the easy_fossy API test suite.

The suite is driven entirely by environment variables (FOSSY_URL, FOSSY_BEARER_TOKEN,
FOSSY_TOKEN_EXPIRE, FOSSY_ACCESS, FOSSY_VERIFY) — the same ones the library uses in
``FossyClient.from_env()``. If the required variables are absent, the suite is
skipped rather than failing, so it can run in CI where a live instance may not exist.
"""

import os

import pytest

from easy_fossy.client import FossyClient

REQUIRED_ENV = ["FOSSY_URL", "FOSSY_BEARER_TOKEN", "FOSSY_TOKEN_EXPIRE"]


def _env_available() -> bool:
    return all(os.environ.get(k) for k in REQUIRED_ENV)


@pytest.fixture(scope="session")
def client():
    """A FossyClient wired to the live instance via environment variables."""
    if not _env_available():
        missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
        pytest.skip(
            f"FOSSology instance env vars missing: {missing}. "
            "Set FOSSY_URL / FOSSY_BEARER_TOKEN / FOSSY_TOKEN_EXPIRE."
        )
    return FossyClient.from_env(verify=False)


@pytest.fixture(scope="session")
def upload_ids(client):
    """Discover the current upload ids present on the instance."""
    uploads = client.uploads.get_all_uploads()
    return [u.id for u in uploads]


@pytest.fixture(scope="session")
def folder_ids(client):
    """Discover the current folder ids present on the instance."""
    folders = client.folders.get_all()
    return [f.id for f in folders]


@pytest.fixture(scope="session")
def job_ids(client):
    """Discover the current job ids present on the instance."""
    jobs = client.jobs.get_all()
    return [j.id for j in jobs]


@pytest.fixture(scope="session")
def group_ids(client):
    """Discover the current group ids present on the instance."""
    groups = client.groups.get_all()
    return [g.id for g in groups]


@pytest.fixture
def temp_folder(client):
    """Create a uniquely-named folder under the root and remove it afterwards."""
    name = f"suite_folder_{os.getpid()}_{__import__('time').time_ns() % 10**6}"
    result = client.folders.create(parent_folder_id=1, folder_name=name)
    folder_id = result.get("message") if isinstance(result, dict) else result
    assert folder_id is not None, f"Could not create temp folder: {result}"
    folder_id = int(folder_id)
    yield folder_id
    # Best-effort cleanup
    try:
        client.folders.delete(folder_id)
    except Exception:
        pass


@pytest.fixture
def temp_file(tmp_path):
    """Write a small license-bearing text file for upload tests."""
    p = tmp_path / "hello_license.txt"
    p.write_text(
        "This file is MIT licensed.\nCopyright (c) Test Suite.\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy.\n"
    )
    return str(p)
