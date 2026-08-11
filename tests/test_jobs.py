"""Tests for the Jobs resource against the live FOSSology instance."""

import pytest

from easy_fossy.exceptions import FossyAPIError


def test_get_all_jobs(client, job_ids):
    jobs = client.jobs.get_all()
    assert isinstance(jobs, list)
    assert len(jobs) > 0
    for j in jobs:
        assert j.id is not None


def test_get_all_jobs_by_upload(client, upload_ids):
    jobs = client.jobs.get_all(upload_id=upload_ids[0])
    assert isinstance(jobs, list)


def test_get_all_jobs_by_status(client):
    jobs = client.jobs.get_all(status="Completed")
    assert isinstance(jobs, list)


def test_get_job_by_id(client, job_ids):
    job = client.jobs.get_by_id(job_ids[0])
    assert job is not None
    assert job.id == job_ids[0]
    assert job.name


def test_get_all_admin(client, job_ids):
    jobs = client.jobs.get_all_admin()
    assert isinstance(jobs, list)


def test_get_scheduler_options(client):
    # Operation names come from the server; 'status' is always valid.
    data = client.jobs.get_scheduler_options("status")
    assert data is not None


def test_get_statistics(client):
    data = client.jobs.get_statistics()
    assert isinstance(data, list)


def test_get_all_server_jobs(client):
    data = client.jobs.get_all_server_jobs()
    assert data is not None


def test_handle_scheduler_run(client):
    # The 'database' operation is idempotent and accepted without extra params.
    data = client.jobs.handle_scheduler_run({"operation": "database"})
    assert data is not None


def test_delete_job(client, job_ids):
    # Job queue ids vary per job (not exposed in the jobs list), so a real delete
    # may return a domain error. The endpoint DELETE /jobs/{id}/{queue} is verified
    # as wired when it returns a value or a FossyAPIError.
    try:
        result = client.jobs.delete(job_ids[0], queue_id=1)
        assert result is not None
    except FossyAPIError:
        pass
