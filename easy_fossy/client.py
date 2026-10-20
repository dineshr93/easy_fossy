import requests
from typing import Optional
from .auth import AuthModule
from .config import FossyConfig
from .transport import Transport
from .resources.users import UsersResource
from .resources.uploads import UploadsResource
from .resources.jobs import JobsResource
from .resources.licenses import LicensesResource
from .resources.groups import GroupsResource
from .resources.folders import FoldersResource
from .resources.reports import ReportsResource


class FossyClient:
    """Coordinator: resolves config, owns the session and transport, wires resources.

    Constructing a client performs no I/O. The bearer token is fetched lazily by
    ``AuthModule.ensure_token`` on the first request that crosses the transport.
    """

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

        self.transport = Transport(self.url, self.session, AuthModule(self.config, self.session, self.config_file))

        # Initialize resources
        self.users = UsersResource(self)
        self.uploads = UploadsResource(self)
        self.jobs = JobsResource(self)
        self.licenses = LicensesResource(self)
        self.groups = GroupsResource(self)
        self.folders = FoldersResource(self)
        self.reports = ReportsResource(self)

    @classmethod
    def from_env(cls, verify: bool = False) -> "FossyClient":
        """Initialize the client using environment variables."""
        config = FossyConfig.from_env()
        return cls(config_file=None, config_override=config, verify=verify)

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

    def generate_and_get_desired_report_for_uploadid(
        self, upload_id: int, report_format, save_to: Optional[str] = None
    ):
        """Generate and download a report for ``upload_id`` (legacy convenience)."""
        return self.reports.generate_and_get_desired_report_for_uploadid(
            upload_id, report_format, save_to=save_to
        )
