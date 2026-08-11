"""Tests for the Groups resource against the live FOSSology instance."""

import time

import pytest

from easy_fossy.exceptions import FossyAPIError


def test_get_all_groups(client):
    groups = client.groups.get_all()
    assert isinstance(groups, list)
    assert len(groups) > 0
    for g in groups:
        assert g.id is not None


def test_get_users_with_roles(client, group_ids):
    members = client.groups.get_users_with_roles(group_ids[0])
    assert isinstance(members, list)


def test_get_deletable(client):
    data = client.groups.get_deletable()
    assert isinstance(data, list)


def test_group_roundtrip(client):
    """Create a group, exercise member management, then delete it."""
    gname = f"suite_group_{time.time_ns() % 10**6}"
    created = client.groups.create(gname, "suite test group")
    assert created is not None

    gid = next(g.id for g in client.groups.get_all() if g.name == gname)
    assert gid is not None

    # The group auto-adds the creator (admin, id 3); remove then re-add to exercise both.
    client.groups.delete_member(gid, 3)
    added = client.groups.add_member(gid, 3)
    assert added is not None

    members = client.groups.get_users_with_roles(gid)
    assert isinstance(members, list)
    assert len(members) >= 1

    perms = client.groups.update_permission(gid, 3, 10)
    assert perms is not None

    deleted = client.groups.delete(gid)
    assert deleted is not None


def test_delete_nonexistent_group(client):
    # Deleting a non-existent group yields a domain 404 (endpoint wired correctly).
    with pytest.raises(FossyAPIError):
        client.groups.delete(999999)
