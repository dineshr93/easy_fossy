from typing import List
from .base import Resource
from ..models import User

class UsersResource(Resource):
    @property
    def base_path(self) -> str:
        return "users"

    def get_all(self, limit: int = 1000, page: int = 1) -> List[User]:
        """List of users present in the given instance"""
        params = {
            "limit": str(limit),
            "page": str(page),
            "groupName": self.config.group_name,
        }
        data = self._request("GET", params=params)
        return [User(**user) for user in data] if isinstance(data, list) else []

    def get_by_id(self, user_id: int) -> User:
        """Get user details by ID"""
        data = self._request("GET", path=f"/{user_id}")
        return User(**data) if data else None
