"""
Shared pytest fixtures for the easy_fossy API test suite.

The suite is driven entirely by environment variables (FOSSY_URL, FOSSY_BEARER_TOKEN,
FOSSY_TOKEN_EXPIRE, FOSSY_ACCESS, FOSSY_VERIFY) — the same ones the library uses in
``FossyClient.from_env()``. If the required variables are absent, the suite is
skipped rather than failing, so it can run in CI where a live instance may not exist.
"""

import os
import time

import pytest

from easy_fossy.client import FossyClient

REQUIRED_ENV = ["FOSSY_URL", "FOSSY_BEARER_TOKEN", "FOSSY_TOKEN_EXPIRE"]

# Apache POI sources jar — a small, stable, license-bearing archive used to seed
# an upload when the instance is empty, so upload-dependent tests always have data.
UPLOAD_JAR_URL = "https://repo1.maven.org/maven2/org/apache/poi/poi/5.5.1/poi-5.5.1-sources.jar"


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
def suite_upload_folder(client):
    """A session-scoped temp folder used to host the seeded upload.

    ``temp_folder`` is function-scoped, so a fresh-instance seed needs its own
    session-scoped folder that lives for the whole run and is removed after.
    """
    name = f"suite_folder_{os.getpid()}_{time.time_ns() % 10**6}"
    result = client.folders.create(parent_folder_id=1, folder_name=name)
    folder_id = result.get("message") if isinstance(result, dict) else result
    assert folder_id is not None, f"Could not create suite upload folder: {result}"
    folder_id = int(folder_id)
    yield folder_id
    # Best-effort cleanup (the autouse cleanup_suite_folders sweep is a backstop)
    try:
        client.folders.delete(folder_id)
    except Exception:
        pass


@pytest.fixture(scope="session")
def upload_ids(client, suite_upload_folder):
    """Discover the current upload ids present on the instance.

    On a fresh/empty instance (no uploads) this seeds one upload from the Apache
    POI sources jar so every upload-dependent test has real data. The seeded
    upload (and its folder) are deleted after the session finishes.
    """
    uploads = client.uploads.get_all_uploads()
    ids = [u.id for u in uploads]
    seeded = None
    if not ids:
        import os as _os
        import tempfile
        import requests as _requests

        tmp_path = tempfile.NamedTemporaryFile(suffix=".jar", delete=False).name
        try:
            resp = _requests.get(UPLOAD_JAR_URL, timeout=60)
            resp.raise_for_status()
            with open(tmp_path, "wb") as f:
                f.write(resp.content)
            upload = client.uploads.upload_file(
                file_path=tmp_path, folder_id=suite_upload_folder
            )
            assert upload is not None, "Could not seed upload from Apache POI sources jar"
            seeded = upload.id
            ids = [upload.id]
        finally:
            _os.unlink(tmp_path)
    yield ids
    # Clean up the upload we seeded once all tests have finished.
    if seeded is not None:
        try:
            client.uploads.delete_uploads_by_upload_id(seeded)
        except Exception:
            pass


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


@pytest.fixture(scope="session", autouse=True)
def cleanup_suite_folders(client):
    """Best-effort, session-end sweep: delete any leftover ``suite_*`` folders.

    ``temp_folder`` normally removes its own folder via teardown, but if a test
    fails mid-way its teardown may not run, orphaning a ``suite_folder_*`` entry
    under the root. This autouse fixture runs after the whole session and
    deletes every folder whose name starts with ``suite_`` regardless of how
    the individual tests ended. It never raises so it cannot mask failures.
    """
    yield
    try:
        for f in client.folders.get_all():
            if f.name.startswith("suite_"):
                try:
                    client.folders.delete(f.id)
                except Exception:
                    # Orphaned folder may be mid-delete or already gone.
                    pass
    except Exception:
        # If the instance is unreachable at teardown, there is nothing to sweep.
        pass


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
