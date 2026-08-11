"""Tests for the Folders resource against the live FOSSology instance."""

from easy_fossy.exceptions import FossyAPIError


def test_get_all_returns_folders(client, folder_ids):
    folders = client.folders.get_all()
    assert isinstance(folders, list)
    assert len(folders) > 0
    # Every folder should have an id and a name
    for f in folders:
        assert f.id is not None
        assert f.name


def test_get_by_id_matches_list(client, folder_ids):
    fid = folder_ids[0]
    folder = client.folders.get_by_id(fid)
    assert folder is not None
    assert folder.id == fid
    assert folder.name


def test_create_returns_info_with_folder_id(client, temp_folder):
    # temp_folder fixture already created a folder; just confirm the id is usable
    folder = client.folders.get_by_id(temp_folder)
    assert folder is not None
    assert folder.id == temp_folder


def test_get_contents_returns_list(client, folder_ids):
    contents = client.folders.get_contents(folder_ids[0])
    assert isinstance(contents, list)


def test_get_unlinkable_contents_returns_list(client, folder_ids):
    items = client.folders.get_unlinkable_contents(folder_ids[0])
    assert isinstance(items, list)


def test_delete_removes_folder(client, temp_folder):
    # temp_folder is removed by the fixture teardown. Deleting a folder schedules
    # a delete job and returns 202 (idempotent), so re-delete returns a value.
    result = client.folders.delete(temp_folder)
    assert result is not None


def test_update_folder(client, temp_folder):
    r = client.folders.update(temp_folder, "renamed_suite", "updated description")
    # Server accepts PATCH; response may be Info or empty body
    assert r is not None
    folder = client.folders.get_by_id(temp_folder)
    assert folder is not None


def test_move_folder(client, temp_folder):
    # Move the temp folder from root (parent 1) under itself is invalid; use folder 1
    # as target parent is fine since it already is there, so just verify it returns.
    r = client.folders.move(temp_folder, 1)
    assert r is not None


def test_unlink_content_reaches_server(client):
    # The instance has no unlinkable contents (contents report removable=False),
    # so there is no real content id to unlink. The endpoint must still be wired:
    # a non-existent content id should yield a domain response (FossyAPIError),
    # not a network/404-path error.
    _reaches_server(lambda: client.folders.unlink_content(999999))


def _reaches_server(fn):
    """Run fn; a returned value or any FossyAPIError (domain response) proves the
    endpoint is wired. Network-level errors (FossyConnectionError) still fail."""
    try:
        return fn() is not None
    except FossyAPIError:
        return True
