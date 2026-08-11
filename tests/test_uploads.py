"""Tests for the Uploads resource against the live FOSSology instance."""

import pytest

from easy_fossy.exceptions import FossyAPIError


def test_get_all_uploads(client):
    uploads = client.uploads.get_all_uploads()
    assert isinstance(uploads, list)
    assert len(uploads) > 0
    for u in uploads:
        assert u.id is not None


def test_get_upload_by_id(client, upload_ids):
    upload = client.uploads.get_upload_by_id(upload_ids[0])
    assert upload is not None
    assert upload.id == upload_ids[0]
    assert upload.uploadname


def test_upload_file_multipart(client, temp_file, temp_folder):
    upload = client.uploads.upload_file(file_path=temp_file, folder_id=temp_folder)
    assert upload is not None, "upload_file returned None"
    assert upload.id is not None
    # Clean up the created upload
    client.uploads.delete_uploads_by_upload_id(upload.id)


def test_upload_by_url(client, temp_folder):
    url = "https://raw.githubusercontent.com/psf/requests/main/LICENSE"
    upload = client.uploads.upload_by_url(url=url, folder_id=temp_folder)
    assert upload is not None, "upload_by_url returned None"
    assert upload.id is not None
    client.uploads.delete_uploads_by_upload_id(upload.id)


def test_upload_by_giturl(client, temp_folder):
    giturl = "https://github.com/psf/requests.git"
    upload = client.uploads.upload_by_giturl(giturl=giturl, folder_id=temp_folder)
    assert upload is not None, "upload_by_giturl returned None"
    assert upload.id is not None
    client.uploads.delete_uploads_by_upload_id(upload.id)


def test_get_upload_tree_id(client, upload_ids):
    info = client.uploads.get_upload_tree_id_by_upload_id(upload_ids[0])
    assert info is not None
    assert info.message is not None  # Info.message carries the topitem upload_tree_id


def test_get_copyrights(client, upload_ids):
    # Use upload 3 which has a real tree (topitem 1331 discovered in recon); fall back
    # to the first upload's topitem.
    info = client.uploads.get_upload_tree_id_by_upload_id(upload_ids[0])
    tree_id = int(info.message)
    copyrights = client.uploads.get_copyrights_by_upload_id_uploadtree_id(
        upload_id=upload_ids[0], upload_tree_id=tree_id
    )
    assert isinstance(copyrights, list)


def test_delete_upload(client, temp_file, temp_folder):
    upload = client.uploads.upload_file(file_path=temp_file, folder_id=temp_folder)
    assert upload is not None
    result = client.uploads.delete_uploads_by_upload_id(upload.id)
    assert result is not None  # FOSSology returns 202 + a delete-job Info


def test_trigger_analysis_schedules_job(client, temp_file, temp_folder):
    # POST /jobs schedules a full analysis for an upload and returns an Info
    # payload whose ``message`` is the scheduled job id.
    upload = client.uploads.upload_file(file_path=temp_file, folder_id=temp_folder)
    assert upload is not None
    info = client.uploads.trigger_analysis_for_upload_id(upload_id=upload.id, folder_id=temp_folder)
    assert info is not None
    assert info.get("message") is not None  # Info.message carries the scheduled job id
    # Clean up the created upload
    client.uploads.delete_uploads_by_upload_id(upload.id)
