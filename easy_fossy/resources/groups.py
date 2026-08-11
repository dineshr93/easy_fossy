from typing import List, Optional, Any
from .base import Resource
from ..models import Group

class GroupsResource(Resource):
    @property
    def base_path(self) -> str:
        return "groups"

    def get_all(self) -> List[Group]:
        """List all groups"""
        data = self._request("GET")
        return [Group(**g) for g in data] if isinstance(data, list) else []

    def delete(self, group_id: int):
        """Delete a group by ID"""
        return self._request("DELETE", path=f"/{group_id}")

    def get_users_with_roles(self, group_id: int):
        """Get group users and their roles"""
        return self._request("GET", path=f"/{group_id}/members")

    def create(self, group_name: str, group_desc: str = None):
        """Create a new user group.
        FOSSology contract: POST /groups with ``name`` as a header.
        """
        headers = {"name": group_name}
        if group_desc:
            headers["description"] = group_desc
        return self._request("POST", headers=headers)

    def add_member(self, group_id: int, user_id: int):
        """Add member to group"""
        return self._request("POST", path=f"/{group_id}/user/{user_id}")

    def delete_member(self, group_id: int, user_id: int):
        """Remove member from group"""
        return self._request("DELETE", path=f"/{group_id}/user/{user_id}")

    def update_permission(self, group_id: int, user_id: int, permission: int):
        """Update group permission for user"""
        payload = {"permission": permission}
        return self._request("PUT", path=f"/{group_id}/user/{user_id}", json=payload)

    def get_deletable(self):
        """Get deletable groups"""
        return self._request("GET", path="/deletable")
