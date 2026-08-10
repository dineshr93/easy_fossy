import requests
import datetime
from typing import Optional
from .config import FossyConfig
from .resources.users import UsersResource
from .resources.uploads import UploadsResource
from .resources.jobs import JobsResource
from .resources.licenses import LicensesResource
from .resources.groups import GroupsResource
from .resources.folders import FoldersResource
from .exceptions import FossyAuthError

class FossyClient:
    def __init__(self, config_file: Optional[str], server_to_use: str = "test", verify: bool = False, config_override: Optional[FossyConfig] = None):
        if config_override:
            self.config = config_override
            self.config_file = "env_config"
        else:
            self.config_file = config_file
            self.config = FossyConfig.from_ini(config_file, server_to_use)
        
        self.config.verify = verify
        self.url = self.config.url
        if not self.url.endswith("/"):
            self.url += "/"

        self.session = requests.Session()
        self.session.verify = self.config.verify

        # Initialize resources
        self.users = UsersResource(self)
        self.uploads = UploadsResource(self)
        self.jobs = JobsResource(self)
        self.licenses = LicensesResource(self)
        self.groups = GroupsResource(self)
        self.folders = FoldersResource(self)

        self._authenticate()

    @classmethod
    def from_env(cls, verify: bool = False) -> "FossyClient":
        """Initialize the client using environment variables."""
        config = FossyConfig.from_env()
        return cls(config_file=None, config_override=config, verify=verify)

    def _authenticate(self):
        """Ensure the session has a valid bearer token"""
        today = datetime.date.today()
        token_expire = self.config.token_expire
        
        if token_expire:
            token_expire_date = datetime.date.fromisoformat(token_expire)
            if today <= token_expire_date and self.config.bearer_token:
                self.session.headers.update({"Authorization": self.config.bearer_token})
                return

        # Token expired or missing, get new one
        self.bearer_token = self._get_token()
        self.session.headers.update({"Authorization": self.bearer_token})

    def _get_token(self) -> str:
        payload = {
            "username": self.config.uname,
            "password": self.config.pwd,
            "token_name": f"created_viaapi_on_{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
            "token_scope": self.config.access,
            "token_expire": str(datetime.date.today() + datetime.timedelta(days=self.config.token_valdity_days)),
        }
        
        response = self.session.post(f"{self.url}tokens", json=payload)
        if response.status_code == 200:
            token = response.json().get("Authorization")
            # Update config and save to file if we have a valid config file
            if self.config_file and self.config_file != "env_config":
                self.config.bearer_token = token
                self.config.token_expire = str(datetime.date.today() + datetime.timedelta(days=self.config.token_valdity_days))
                self.config.save_to_ini(self.config_file)
            return token
        
        raise FossyAuthError(f"Failed to obtain token: {response.text}")

    # --- Backward Compatibility Layer ---
    
    def get_all_users(self):
        return self.users.get_all()

    def get_user_by_id(self, user_id: int):
        return self.users.get_by_id(user_id)

    def get_all_jobs(self, upload_id: Optional[int] = None):
        return self.jobs.get_all(upload_id=upload_id)

    def get_job_info_by_id(self, job_id: int):
        return self.jobs.get_by_id(job_id)

    def upload_file(self, file_path: str, folder_id: int):
        return self.uploads.upload_file(file_path, folder_id)

    def get_upload_by_id(self, upload_id: int):
        return self.uploads.get_upload_by_id(upload_id)
