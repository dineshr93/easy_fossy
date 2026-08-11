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

    def create(self, payload: dict):
        """Create user"""
        return self._request("POST", json=payload)

    def update(self, user_id: int, payload: dict):
        """Modify user by ID"""
        return self._request("PUT", path=f"/{user_id}", json=payload)

    def delete(self, user_id: int):
        """Delete user by ID"""
        return self._request("DELETE", path=f"/{user_id}")

    def get_self(self):
        """Get self user info"""
        return self._request("GET", path="/self")

    def create_token(self, payload: dict):
        """Create REST API token"""
        return self._request("POST", path="/tokens", json=payload)

    def get_tokens(self, token_type: str):
        """Get tokens by type"""
        return self._request("GET", path=f"/tokens/{token_type}")
