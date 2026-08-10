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
        params = {"group_id": str(group_id)}
        return self._request("GET", params=params)
