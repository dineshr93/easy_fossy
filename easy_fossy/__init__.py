from .models import (
    License,
    Public,
    Findings,
    ClearingStatus,
    Action,
    Action1,
    Agent,
    ApiInfo,
    Copyright,
    File,
    Folder,
    Group,
    Hash,
    HeathInfo,
    Info,
    Job,
    Kind,
    Kind1,
    LicenseGetResponse,
    LicensePostRequest,
    LicenseShortnameGetResponse,
    LicenseShortnamePatchRequest,
    Public,
    ReportFormat1,
    ReportFormat2,
    ScanOptions,
    SearchResults,
    SearchType,
    SearchType1,
    SearchType2,
    Status5,
    TokenRequest,
    Upload,
    UploadLicense,
    UploadLicenses,
    UploadsPostRequest,
    UploadSummary,
    UploadType1,
    UploadType2,
    User,
    ReportFormat,
)

import requests
import time
import configparser
import datetime
import sys
from pathlib import Path
from typing import List
from requests_toolbelt.multipart.encoder import MultipartEncoder


class easy_fossy:
    def __init__(self, config_file: str, server_to_use: str = "test"):
        self.config_file = config_file
        self.server = server_to_use
        # config_file = 'config.ini'
        if not Path(config_file).exists():
            print(
                f"config.ini file ->  {config_file} doesn't exist. Please run set_config_ini_file_full_path(config_file='full_path_to_config.ini')"
            )
            sys.exit(1)
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(config_file)

        self.config = self.config_parser[self.server]
        self.url = self.config.get("url")

        if not self.url.endswith("/"):
            self.url = self.url + "/"

        self.token_expire = self.config.get("token_expire")
        self.reports_location = self.config.get("reports_location")

        self.today = datetime.date.today()

        self.now = datetime.datetime.now()
        self.dt_format = "%d-%m-%Y %H:%M"
        # print(today)
        # print(now.strftime(dt_format))
        self.token_expire_yyyy_mm_dd = self.today + datetime.timedelta(
            days=self.config.getint("token_valdity_days")
        )

        self.bearer_token = self.config.get("bearer_token")
        if self.token_expire:
            token_expire_datetime = datetime.date.fromisoformat(self.token_expire)
        else:
            token_expire_datetime = None
        self.group_name = self.config.get("group_name")

        def get_user_group(self):
            self.config["group_name"] = str(
                self.create_new_user_group(new_group_name="fossy")
            )
            print("No user group found, Creating a group_name called -> fossy")
            with open(self.config_file, "w") as cf:
                self.config_parser.write(cf)
            return self.config.get("group_name")

        if not self.group_name:
            self.group_name = get_user_group()

        if (
            not self.bearer_token
            or not token_expire_datetime
            or (self.today > token_expire_datetime)
        ):
            self.bearer_token = self.get_token_by_uname_pwd()
        else:
            print("Re using the existing unexpired Token")

    def set_config_ini_file_full_path(self, config_file: str):
        """Sets config file. set_config_ini_file_full_path(config_file= full_path_to/config.ini)"""
        self.config_file = config_file

    def create_new_user_group(self, new_group_name: str) -> str:
        payload = ""
        headers = {
            "accept": "application/json",
            "name": new_group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "POST", self.url + str("groups"), data=payload, headers=headers
        )

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"{report_info.message}")
                return new_group_name
            case _:
                print(response.text)

    def get_token_by_uname_pwd(self) -> str:
        """Get the token via user name and password in the config"""
        payload = {
            "username": self.config.get("uname"),
            "password": self.config.get("pwd"),
            "token_name": str("created_viaapi_on_")
            + str(self.now.strftime(self.dt_format)),
            "token_scope": self.config.get("access"),
            "token_expire": str(self.token_expire_yyyy_mm_dd),
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST", self.url + str("tokens"), json=payload, headers=headers
        )

        match response.json():
            case {"Authorization": self.bearer_token}:
                self.config["bearer_token"] = self.bearer_token
                self.config["token_expire"] = str(self.token_expire_yyyy_mm_dd)
                with open(self.config_file, "w") as cf:
                    self.config_parser.write(cf)
                self.bearer_token = self.config.get("bearer_token")
                if self.bearer_token != "":
                    print(
                        f"Added token to bearer_token param of your config {self.bearer_token}"
                    )
                return self.bearer_token
            case _:
                print("Error while getting token")
                print(response.text)
                sys.exit(1)

    def get_all_users(self) -> List[User]:
        """List of users present in the given instance"""
        payload = ""
        headers = {
            "accept": "application/json",
            "limit": "1000",
            "page": "1",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET", self.url + str("users"), data=payload, headers=headers
        )

        match response.json():
            case [*args]:
                # users = [print(user) and User(**user) for user in args]
                users = [User(**user) for user in args]
                # for j in jobs:
                #     print(jobs)
                return users
            case _:
                print(response.text)

    # get_all_users()

    def get_user_by_id(self, user_id: int) -> User:
        """give the user_id to get the
        {
        "id": 0,
        "name": "string",
        "description": "string",
        "email": "string",
        "accessLevel": "none",
        "rootFolderId": 0,
        "emailNotification": true,
        "defaultGroup": 0,
        "agents": {
            "bucket": true,
            "copyright_email_author": true,
            "ecc": true,
            "keyword": true,
            "mime": true,
            "monk": true,
            "nomos": true,
            "ojo": true,
            "package": true,
            "reso": true,
            "heritage": true
        },
        "defaultBucketpool": 0
        }
        """
        payload = ""
        headers = {"accept": "application/json", "Authorization": self.bearer_token}

        response = requests.request(
            "GET", self.url + str(f"users/{user_id}"), data=payload, headers=headers
        )

        match response.json():
            case {**user}:
                user = User(**user)
                # print(user)
                return user
            case _:
                print(response.text)

        # get_user_by_id(user_id=3)

    # get_user_by_id(user_id=)
    def get_all_jobs(self) -> List[Job]:
        """List of jobs present in the given instance"""
        payload = ""
        headers = {
            "accept": "application/json",
            "limit": "1000",
            "page": "1",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET", self.url + str("jobs"), data=payload, headers=headers
        )

        match response.json():
            case [*args]:
                jobs = [Job(**job) for job in args]
                # for j in jobs:
                #     print(jobs)
                return jobs
            case _:
                print(response.text)

    # get_all_jobs()

    def get_job_info_by_id(self, job_id: int) -> Job:
        """give the job_id to get the
        {
        "id": 2,
        "name": "drawio-Source.zip",
        "queueDate": "2021-10-04 10:42:38.577655+00",
        "uploadId": "2",
        "userId": "3",
        "groupId": "3",
        "eta": 0,
        "status": "Completed"
        }
        """
        payload = ""
        headers = {"accept": "application/json", "Authorization": self.bearer_token}

        response = requests.request(
            "GET", self.url + str(f"jobs/{job_id}"), data=payload, headers=headers
        )

        match response.json():
            case {**job}:
                job = Job(**job)
                print(job)
                return job
            case _:
                print(response.text)

    # get_job_info_by_id(job_id=3)

    def get_job_info_by_upload_id(self, upload_id: int) -> Job:
        """give the upload_id to get the job status
        {
        "id": 2,
        "name": "drawio-Source.zip",
        "queueDate": "2021-10-04 10:42:38.577655+00",
        "uploadId": "2",
        "userId": "3",
        "groupId": "3",
        "eta": 0,
        "status": "Completed"
        }
        """
        payload = ""
        headers = {"accept": "application/json", "Authorization": self.bearer_token}

        response = requests.request(
            "GET",
            self.url + str(f"jobs?upload={upload_id}"),
            data=payload,
            headers=headers,
        )

        match response.json():
            case {**job}:
                job = Job(**job)
                print(job)
                return job
            case _:
                print(response.text)

    # get_job_info_by_upload_id(job_id=3)

    def get_upload_tree_id_by_upload_id(self, upload_id: int) -> Info:
        """give the upload_id to get the upload_tree_id
        {
            "code": 200,
            "message": 18852769,
            "type": "INFO"
        }
        """
        payload = ""
        headers = {"accept": "application/json", "Authorization": self.bearer_token}

        response = requests.request(
            "GET",
            self.url + str(f"uploads/{upload_id}/topitem"),
            data=payload,
            headers=headers,
        )

        match response.json():
            case {**info}:
                info = Info(**info)
                # print(info)
                return info
            case _:
                print(response.text)

    # get_upload_tree_id_by_upload_id(upload_id=3)

    def get_copyrights_by_upload_id_uploadtree_id(
        self, upload_id: int, upload_tree_id: int
    ) -> List[Copyright]:
        """give the upload_id to get the upload_tree_id
        [{
            "content": "Copyright (C) 2008 dinesh Inc.",
            "hash": "7414e55329991506a99fe2fb3383bbee",
            "count": 28
        },
        {
            "content": "Copyright (C) 2009 ravi Inc.",
            "hash": "5c1af30f2523e1257bf8b7dba3e79776",
            "count": 4
        }]
        """
        payload = ""
        headers = {"accept": "application/json", "Authorization": self.bearer_token}

        response = requests.request(
            "GET",
            self.url + str(f"uploads/{upload_id}/item/{upload_tree_id}/copyrights"),
            data=payload,
            headers=headers,
        )

        match response.json():
            case [*args]:
                copyrights = [Copyright(**copyright) for copyright in args]
                # for j in jobs:
                #     print(jobs)
                return copyrights
            case _:
                print(response.text)

    # get_copyrights_by_upload_id_uploadtree_id(upload_id=3)

    def get_copyrights_by_upload_id(self, upload_id: int) -> List[Copyright]:
        """give the upload_id to get the upload_tree_id
        [{
            "content": "Copyright (C) 2008 dinesh Inc.",
            "hash": "7414e55329991506a99fe2fb3383bbee",
            "count": 28
        },
        {
            "content": "Copyright (C) 2009 ravi Inc.",
            "hash": "5c1af30f2523e1257bf8b7dba3e79776",
            "count": 4
        }]
        """
        payload = ""
        headers = {"accept": "application/json", "Authorization": self.bearer_token}

        upload_tree_id_info: Info = self.get_upload_tree_id_by_upload_id(
            upload_id=upload_id
        )
        upload_tree_id = upload_tree_id_info.message

        response = requests.request(
            "GET",
            self.url
            + str(
                f"uploads/{upload_id}/item/{upload_tree_id}/copyrights?status=active"
            ),
            data=payload,
            headers=headers,
        )

        match response.json():
            case [*args]:
                copyrights = [Copyright(**copyright) for copyright in args]
                # for j in jobs:
                #     print(jobs)
                return copyrights
            case _:
                print(response.text)

    # get_copyrights_by_upload_id(upload_id=3)

    def generate_and_get_desired_report_for_uploadid(
        self, upload_id: int, report_format: ReportFormat
    ):
        """For given upload_id generate the report job to get report id and use to download desired Report Format

        class ReportFormat(Enum):
            dep5 = 'dep5'
            spdx2 = 'spdx2'
            spdx2tv = 'spdx2tv'
            readmeoss = 'readmeoss'
            unifiedreport = 'unifiedreport'
        """
        payload = ""
        headers = {
            "accept": "application/json",
            "uploadId": str(upload_id),
            "reportFormat": str(report_format.name),
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }
        report_info: Info = None
        report_id: int = None
        response = requests.request(
            "GET", self.url + str("report"), data=payload, headers=headers
        )

        match response.json():
            case {"message": url_with_report_id}:
                report_id = url_with_report_id.rsplit("/", 1).pop()
                print(report_id)

            case {**info}:
                report_info = Info(**info)
                print(report_info.message)
                # return report_info
            case _:
                print(response.text)

        payload = ""
        headers = {
            "accept": "text/plain",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }
        timeout = 20
        timewait = 0.2
        timer = 0
        response = requests.request(
            "GET",
            self.url + str("report/") + str(report_id),
            data=payload,
            headers=headers,
        )
        while response.status_code != 200:

            print(f"waiting for {timewait} sec")
            time.sleep(timewait)
            response = requests.request(
                "GET",
                self.url + str(f"report/{report_id}"),
                data=payload,
                headers=headers,
            )
            if timer > timeout:
                break
            if response.status_code == 200:
                break

        # print(response.headers)
        file_name = response.headers.get("Content-Disposition").split("filename=")[1]
        path_with_file = self.reports_location + str(file_name.replace('"', ""))

        if report_format != ReportFormat.unifiedreport:
            with open(path_with_file, "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            with open(path_with_file, "wb") as f:
                # 2 MB chunks
                for chunk in response.iter_content(1024 * 1024 * 2):
                    f.write(chunk)

    # generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)

    def get_all_folders(self) -> List[Folder]:
        """Get all the folders in given fossy instance"""
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET", self.url + str("folders"), data=payload, headers=headers
        )

        match response.json():
            case [*args]:
                folders = [Folder(**folder) for folder in args]
                for f in folders:
                    print(f)
                # print(folders)
                return folders
            case _:
                print(response.text)

    # get_all_folders()

    def get_folder_info_by_id(self, folder_id: int) -> Folder:
        """get_folder_info_by_id(folder_id: int) -> Folder"""
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET",
            self.url + str("folders/") + str(folder_id),
            data=payload,
            headers=headers,
        )

        match response.json():
            case {**args}:
                folder = Folder(**args)
                print(folder)
                return folder
            case _:
                print(response.text)

    # get_folder_info_by_id(folder_id=11)

    def change_folder_name_or_desc(
        self, folder_id: int, new_folder_name: str = "", new_folder_desc: str = ""
    ):
        """name and desc are optional, mandatory input is the folder id"""
        payload = ""
        headers = {
            "accept": "application/json",
            "name": new_folder_name,
            "description": new_folder_desc,
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "PATCH",
            self.url + str(f"folders/{folder_id}"),
            data=payload,
            headers=headers,
        )
        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(report_info.message)
                return report_info
            case _:
                print(response.text)

    # change_folder_name_or_desc(folder_id=3, new_folder_name='', new_folder_desc='')

    # change_folder_name_or_desc(folder_id=2, new_folder_name='', new_folder_desc = 'scans triggered from sw360 test')
    # get_all_folders()

    def create_folder_under_parent_folder_id(
        self, parent_folder_id: int, folder_name: str
    ) -> Info:
        """create the folder under parent folder id with given folder_name"""
        payload = ""
        headers = {
            "accept": "application/json",
            "parentFolder": str(parent_folder_id),
            "folderName": folder_name,
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "POST", self.url + str("folders"), data=payload, headers=headers
        )

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"Created folder id is {report_info.message}")
                return report_info
            case _:
                print(response.text)

    # create_folder_under_parent_folder_id(
    #     parent_folder_id=1, folder_name='test')
    # create_folder_under_parent_folder_id(
    #     parent_folder_id=6, folder_name='submove')
    # get_all_folders()

    def delete_folder_by_id(self, folder_id: int):
        """delete_folder_by_id(folder_id: int)"""
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "DELETE",
            self.url + str("folders/{folder_id}"),
            data=payload,
            headers=headers,
        )

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"Deleted folder is {report_info.message}")
                # return report_info
            case _:
                print(response.text)

    # delete_folder_by_id(folder_id=3)
    # get_all_folders()

    def apply_action_to_folderid(
        self, actions: Action, folder_id: int, parent_folder_id: int
    ) -> Info:
        """apply_action_to_folderid(actions: Action, folder_id: int, parent_folder_id: int) -> Info"""
        payload = ""
        headers = {
            "accept": "application/json",
            "parent": str(parent_folder_id),
            "action": actions.name,
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "PUT", self.url + str("folders/{folder_id}"), data=payload, headers=headers
        )

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"{report_info.message}")
                return report_info
            case _:
                print(response.text)

    # apply_action_to_folderid(actions=Action.copy, folder_id=5, parent_folder_id=2)
    # apply_action_to_folderid(actions=Action.move, folder_id=6, parent_folder_id=2)

    # change_folder_name_or_desc(folder_id=11, new_folder_name='',
    #                            new_folder_desc='scans triggered from sw360 test')

    # get_all_folders('fossy')

    def get_upload_summary_for_uploadid(self, upload_id: int) -> UploadSummary:
        """get upload summary for given upload_id
        {
        "id": 2,
        "uploadName": "drawio-Source.zip",
        "assignee": null,
        "mainLicense": null,
        "uniqueLicenses": 29,
        "totalLicenses": 842,
        "uniqueConcludedLicenses": 0,
        "totalConcludedLicenses": 0,
        "filesToBeCleared": 933,
        "filesCleared": 933,
        "clearingStatus": "Open",
        "copyrightCount": 1359
        }
        """
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET",
            self.url + str(f"uploads/{upload_id}/summary"),
            data=payload,
            headers=headers,
        )
        match response.json():
            case {**info}:
                upload_summary = UploadSummary(**info)
                print(f"Returned upload summary for file {upload_summary.uploadName}")
                return upload_summary
            case _:
                print(response.text)

    # get_upload_summary_for_uploadid(upload_id=2)

    def get_all_uploads_based_on(
        self,
        folder_id: int,
        is_recursive: bool,
        search_pattern_key: str,
        upload_status: ClearingStatus,
        assignee: str,
        since_yyyy_mm_dd: str,
        page: int,
        limit: int,
    ) -> List[Upload]:
        """get_all_uploads_based_on(folder_id: int, is_recursive: bool, search_pattern_key: str, upload_status: ClearingStatus, assignee: str, since_yyyy_mm_dd: str, page: int, limit: int) -> List[Upload]"""
        querystring = {
            "folderId": folder_id,
            "recursive": is_recursive,
            "name": search_pattern_key,
            "status": upload_status,
            "assignee": assignee,
            "since": since_yyyy_mm_dd,
            "page": page,
            "limit": limit,
            "groupName": self.group_name,
        }

        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "page": str(page),
            "limit": str(limit),
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET",
            self.url + str("uploads"),
            data=payload,
            headers=headers,
            params=querystring,
        )

        match response.json():
            case [*args]:
                uploads = [Upload(**upload) for upload in args]
                # for upload in uploads:
                #     print(upload)
                return uploads
            case _:
                print(response.text)

    # get_all_uploads_based_on(folder_id=1, is_recursive=True,
    #                          search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000)

    def get_all_uploads_based_on_common_assignee(
        self,
        folder_id: int,
        is_recursive: bool,
        search_pattern_key: str,
        upload_status: ClearingStatus,
        # assignee: str,
        since_yyyy_mm_dd: str,
        page: int,
        limit: int,
    ) -> List[Upload]:
        """get_all_uploads_based_on(folder_id: int, is_recursive: bool, search_pattern_key: str, upload_status: ClearingStatus, assignee: str, since_yyyy_mm_dd: str, page: int, limit: int) -> List[Upload]"""
        querystring = {
            "folderId": folder_id,
            "recursive": is_recursive,
            "name": search_pattern_key,
            "status": upload_status.name,
            # "assignee": assignee,
            "since": since_yyyy_mm_dd,
        }

        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "page": str(page),
            "limit": str(limit),
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET",
            self.url + str("uploads"),
            data=payload,
            headers=headers,
            params=querystring,
        )

        match response.json():
            case [*args]:
                uploads = [Upload(**upload) for upload in args]
                # for upload in uploads:
                #     print(upload)
                return uploads
            case _:
                print(response.text)

    # get_all_uploads_based_on_common_assignee(folder_id=1, is_recursive=True,
    #                          search_pattern_key='', upload_status=ClearingStatus.Open, since_yyyy_mm_dd='', page=1, limit=1000)

    def get_licenses_found_by_agents_for_uploadid(
        self, upload_id: int, agents: List[str], show_directories: bool
    ) -> UploadLicenses | Info:
        """get licenses acc to agent
        class Agent(Enum):
            nomos = 'nomos'
            monk = 'monk'
            ninka = 'ninka'
            ojo = 'ojo'
            reportImport = 'reportImport'
            reso = 'reso'
        """
        querystring = {"agent": agents, "containers": str(show_directories)}
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET",
            self.url + str(f"uploads/{upload_id}/licenses"),
            data=payload,
            headers=headers,
            params=querystring,
        )

        match response.json():
            case [*args]:
                upload_icenses = [
                    UploadLicense(**uploadLicense) for uploadLicense in args
                ]
                for f in upload_icenses:
                    print(f)
                # print(folders)
                return upload_icenses
            case {**info}:
                report_info = Info(**info)
                print(f"{report_info.message}")
                return report_info
            case _:
                print(response.text)

    # get_licenses_found_by_agents_for_uploadid(upload_id=2, show_directories=True, group_name=group_name, agents=[
    #                                           Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name, Agent.reportImport.name, Agent.reso.name])

    def get_upload_id_by_local_package_upload(
        self, file_path: str, folder_id: int, upload_desc: str, visibility: Public
    ) -> str:
        """get_upload_id_by_local_package_upload(file_path: str, folder_id: int, upload_desc: str, visibility: Public) -> str"""
        # files = {'file': open(file_path, 'rb')}

        if Path(file_path).exists():
            print(f"File path {file_path} exists")

        file_name = file_path.split("/").pop()
        print(file_name)
        m = MultipartEncoder(
            [
                (
                    "fileInput",
                    (file_name, open(file_path, "rb"), "application/octet-stream"),
                )
            ],
            None,
            encoding="utf-8",
        )
        headers = {
            # "accept": "application/json",
            "folderId": str(folder_id),
            "groupName": self.group_name,
            "uploadDescription": upload_desc,
            "public": visibility.name,
            "Content-Type": m.content_type,
            "Authorization": self.bearer_token,
        }
        response = requests.post(self.url + str("uploads"), data=m, headers=headers)

        timeout = 20
        timewait = 0.2
        timer = 0

        while response.status_code != 201:

            print(f"waiting for {timewait} sec")
            time.sleep(timewait)
            response = requests.post(self.url + str("uploads"), data=m, headers=headers)
            timer = timer + timewait
            if timer > timeout:
                break
            if response.status_code == 201:
                break

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"upload id is {report_info.message}")
                return report_info.message
            case _:
                print(response.text)

    # get_upload_id_by_local_package_upload(
    #     file_path='uploads/commons-io-2.11.0-src.zip', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public)
    @staticmethod
    def check_url_exists(url: str):
        """
        Checks if a url exists
        :param url: url to check
        :return: True if the url exists, false otherwise.
        """
        return requests.head(url, allow_redirects=True).status_code == 200

    def get_upload_id_by_download_url_package_upload(
        self,
        file_download_url: str,
        file_name: str,
        folder_id: int,
        upload_desc: str,
        visibility: Public,
    ) -> str:
        """get_upload_id_by_download_url_package_upload(file_download_url: str, file_name: str, folder_id: int, upload_desc: str, visibility: Public) -> str"""
        # files = {'file': open(file_path, 'rb')}
        if not self.check_url_exists(file_download_url):
            print(f"git url {file_download_url} is malformed")

        m = MultipartEncoder(fields={"url": file_download_url, "name": file_name})
        headers = {
            # "accept": "application/json",
            "folderId": str(folder_id),
            "groupName": self.group_name,
            "uploadType": "url",
            "uploadDescription": upload_desc,
            "public": visibility.name,
            "Content-Type": m.content_type,
            "Authorization": self.bearer_token,
        }
        response = requests.post(self.url + str("uploads"), data=m, headers=headers)

        timeout = 20
        timewait = 0.2
        timer = 0

        while response.status_code != 201:

            print(f"waiting for {timewait} sec")
            time.sleep(timewait)
            response = requests.post(self.url + str("uploads"), data=m, headers=headers)
            # print(response.text)
            timer = timer + timewait
            if timer > timeout:
                break
            if response.status_code == 201:
                break

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"upload id is {report_info.message}")
                return report_info.message
            case _:
                print(response.text)

    # get_upload_id_by_download_url_package_upload(
    #     file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip', file_name='pageres', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public)

    def get_upload_id_by_giturl_package_upload(
        self,
        git_url: str,
        branch_name: str,
        upload_name: str,
        folder_id: int,
        upload_desc: str,
        visibility: Public,
    ) -> str:
        """get_upload_id_by_giturl_package_upload(git_url: str, branch_name: str, upload_name: str, folder_id: int, upload_desc: str, visibility: Public) -> str"""
        # files = {'file': open(file_path, 'rb')}

        if not self.check_url_exists(git_url):
            print(f"git url {git_url} is malformed")

        file_name = git_url.split("/").pop()
        print(file_name)

        payload = {
            "vcsType": "git",
            "vcsUrl": git_url,
            "vcsBranch": branch_name,
            "vcsName": upload_name,
        }
        headers = {
            # "accept": "application/json",
            "folderId": str(folder_id),
            "uploadDescription": upload_desc,
            "public": visibility.name,
            "ignoreScm": "true",
            "uploadType": "vcs",
            "groupName": self.group_name,
            # "Content-Type": "application/json",
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "POST", self.url + str("uploads"), json=payload, headers=headers
        )

        # print(response.status_code)
        # print(response.text)

        timeout = 20
        timewait = 0.2
        timer = 0

        while response.status_code != 201:

            print(f"waiting for {timewait} sec")
            time.sleep(timewait)
            response = requests.request(
                "POST", self.url + str("uploads"), json=payload, headers=headers
            )
            print(response.json())
            timer = timer + timewait
            if timer > timeout:
                break
            if response.status_code == 201:
                break

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"upload id is {report_info.message}")
                return report_info.message
            case _:
                print(response.text)

    # get_upload_id_by_giturl_package_upload(git_url='https://github.com/dineshr93/pageres', branch_name='master', upload_name='',
    #                                        folder_id=1, upload_desc='', visibility=Public.public)

    def trigger_analysis_for_upload_id(self, upload_id: int, folder_id: int) -> Info:
        """trigger_analysis_for_upload_id(upload_id: int, folder_id: int) -> Info"""
        payload = {
            "analysis": {
                "bucket": True,
                "copyright_email_author": True,
                "ecc": True,
                "keyword": True,
                "mime": True,
                "monk": True,
                "nomos": True,
                "ojo": True,
                "package": True,
                "reso": True,
            },
            "decider": {
                "nomos_monk": True,
                "bulk_reused": True,
                "new_scanner": True,
                "ojo_decider": True,
            },
            "reuse": {
                "reuse_upload": 0,
                "reuse_group": "string",
                "reuse_main": True,
                "reuse_enhanced": True,
                "reuse_report": True,
                "reuse_copyright": True,
            },
        }
        headers = {
            "accept": "application/json",
            "folderId": str(folder_id),
            "uploadId": upload_id,
            "groupName": self.group_name,
            "Content-Type": "application/json",
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "POST", self.url + str("jobs"), json=payload, headers=headers
        )
        timeout = 50
        timewait = 0.5
        timer = 0
        while response.status_code != 201:
            print(f"waiting for {timewait} sec")
            time.sleep(timewait)
            response = requests.request(
                "POST", self.url + str("jobs"), json=payload, headers=headers
            )
            print(response.text)
            timer = timer + timewait
            if timer > timeout:
                break
            if response.status_code == 201:
                break
        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"job id is {report_info.message}")
                return report_info
            case _:
                print(response.text)

    # trigger_analysis_for_upload_id(
    #     upload_id=4, folder_id=1, group_name=group_name)

    def trigger_analysis_for_upload_package(self, file_path: str, folder_id: int):
        """trigger_analysis_for_upload_package(file_path: str, folder_id: int)"""
        if not Path(file_path).exists():
            print(f"File path {file_path} doesn't exist")

        uploads: List[Upload] = self.get_all_uploads_based_on_common_assignee(
            folder_id=folder_id,
            is_recursive=True,
            search_pattern_key="",
            upload_status=ClearingStatus.Open,
            # assignee="",
            since_yyyy_mm_dd="",
            page=1,
            limit=1000,
            # group_name=self.group_name,
        )
        file_name = file_path.split("/").pop()

        # if folder is empty uploads will be None
        size = 0
        if uploads == None:
            size = 0
        else:
            upload_id = [u.id for u in uploads if file_name == u.uploadname]
            size = len(upload_id)
        is_present_uploadID = False
        if size > 1:
            is_present_uploadID = True
            print(f"{size} no of duplicates are there with ids {upload_id}")
            print(
                "exiting.. please comeback after deleting duplicates via delete_uploads_by_upload_id(upload_id=upload_id, group_name=group_name)"
            )
            sys.exit(1)
        elif size == 1:
            is_present_uploadID = True
            upload_id = upload_id[0]
        else:
            # no upload_id is there
            upload_id = self.get_upload_id_by_local_package_upload(
                file_path=file_path,
                folder_id=folder_id,
                upload_desc=file_name,
                visibility=Public.protected,
                # group_name=group_name,
            )

        if is_present_uploadID:
            # get_all_jobs() is very slow because of huge size so just returning message
            # jobs: List[Job] = [
            #     j for j in self.get_all_jobs() if j.uploadId == upload_id
            # ]

            # if len(jobs) >= 1:
            #     print(f"Multiple jobs exists for same upload_id: {upload_id}")
            #     job = jobs.pop()
            #     print(f" Returning Existing Job ID :{job.id}")
            #     return job.id
            # else:
            #     job = jobs.pop()
            #     print(f" Returning Existing Job ID :{job.id}")
            #     return job.id
            print(f"File {file_name} already present in folder id {folder_id}")
        else:
            info = self.trigger_analysis_for_upload_id(
                upload_id=upload_id,
                folder_id=folder_id,
                # group_name=self.group_name
            )
            print(f"Computed new Job ID is :{info.message}")
            return info.message

    # trigger_analysis_for_upload_package(
    #     file_path='uploads/commons-lang3-3.12.0-src.zip', folder_id=1, group_name=group_name)

    def trigger_analysis_for_url_upload_package(
        self, file_download_url: str, file_name: str, branch_name: str, folder_id: int
    ):
        """trigger_analysis_for_url_upload_package(file_download_url: str, file_name: str, branch_name: str, folder_id: int)"""
        if not self.check_url_exists(file_download_url):
            print(f"git url {file_download_url} is malformed")

        uploads: List[Upload] = self.get_all_uploads_based_on_common_assignee(
            folder_id=folder_id,
            is_recursive=True,
            search_pattern_key="",
            upload_status=ClearingStatus.Open,
            # assignee="",
            since_yyyy_mm_dd="",
            page=1,
            limit=1000,
            # group_name=self.group_name,
        )
        # if folder is empty uploads will be None
        size = 0
        upload_id: any
        if uploads == None:
            print("uploads is None")
            size = 0
        else:
            upload_id = [u.id for u in uploads if file_name == u.uploadname]
            # upload_id = []
            # for u in uploads:
            #     if file_name == u.uploadname:
            #         # print(
            #         #     f"Comparing file_name: {file_name} == u.uploadname: {u.uploadname}"
            #         # )
            #         upload_id.append(u.id)

            size = len(upload_id)
            # print(f"Existing upload size: {size}")
        is_present_uploadID = False
        if size > 1:
            # print("section size > 1")
            is_present_uploadID = True
            print(f"{size} no of duplicates are there with ids {upload_id}")
            print(
                "exiting.. please comeback after deleting duplicates via delete_uploads_by_upload_id(upload_id=upload_id, group_name=group_name)"
            )
            sys.exit(1)
        elif size == 1:
            # print("section size ==  1")
            is_present_uploadID = True
            upload_id = upload_id[0]
        else:
            # print("section else size ")
            # no upload_id is there
            upload_id = self.get_upload_id_by_download_url_package_upload(
                file_download_url=file_download_url,
                file_name=file_name,
                folder_id=folder_id,
                upload_desc=file_name,
                visibility=Public.public,
                # group_name=self.group_name,
            )

        if is_present_uploadID:
            # get_all_jobs() is very slow because of huge size so just returning message
            # jobs: List[Job] = [
            #     j for j in self.get_all_jobs() if j.uploadId == upload_id
            # ]

            # if len(jobs) >= 1:
            #     print(f"Multiple jobs exists for same upload_id: {upload_id}")
            #     job = jobs.pop()
            #     print(f" Returning Existing Job ID :{job.id}")
            #     return job.id
            # else:
            #     job = jobs.pop()
            #     print(f" Returning Existing Job ID :{job.id}")
            #     return job.id
            print(f"File {file_name} already present in folder id {folder_id}")
        else:
            info = self.trigger_analysis_for_upload_id(
                upload_id=upload_id, folder_id=folder_id
            )
            print(f"Computed new Job ID is :{info.message}")
            return info.message

    # trigger_analysis_for_url_upload_package(
    #     file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip', file_name='pageres.zip', branch_name='', folder_id=1)

    def trigger_analysis_for_git_upload_package(
        self, git_url: str, branch_name: str, folder_id: int
    ):
        """trigger_analysis_for_git_upload_package(git_url: str, branch_name: str, folder_id: int)"""
        if not self.check_url_exists(git_url):
            print(f"git url {git_url} is malformed")

        file_name = git_url.split("/").pop()
        print(file_name)

        uploads: List[Upload] = self.get_all_uploads_based_on_common_assignee(
            folder_id=folder_id,
            is_recursive=True,
            search_pattern_key="",
            upload_status=ClearingStatus.Open,
            # assignee="",
            since_yyyy_mm_dd="",
            page=1,
            limit=1000,
            # group_name=self.group_name,
        )

        # if folder is empty uploads will be None
        size = 0
        if uploads == None:
            size = 0
        else:
            upload_id = [u.id for u in uploads if file_name == u.uploadname]
            size = len(upload_id)
        is_present_uploadID = False
        if size > 1:
            is_present_uploadID = True
            print(f"{size} no of duplicates are there with ids {upload_id}")
            print(
                "exiting.. please comeback after deleting duplicates via delete_uploads_by_upload_id(upload_id=upload_id, group_name=group_name)"
            )
            sys.exit(1)
        elif size == 1:
            is_present_uploadID = True
            upload_id = upload_id[0]
        else:
            # no upload_id is there
            upload_id = self.get_upload_id_by_giturl_package_upload(
                git_url=git_url,
                branch_name=branch_name,
                upload_name=file_name,
                folder_id=folder_id,
                upload_desc="",
                visibility=Public.public,
                # group_name=self.group_name,
            )

        if is_present_uploadID:
            # get_all_jobs() is very slow because of huge size so just returning message
            # jobs: List[Job] = [
            #     j for j in self.get_all_jobs() if j.uploadId == upload_id
            # ]

            # if len(jobs) >= 1:
            #     print(f"Multiple jobs exists for same upload_id: {upload_id}")
            #     job = jobs.pop()
            #     print(f" Returning Existing Job ID :{job.id}")
            #     return job.id
            # else:
            #     job = jobs.pop()
            #     print(f" Returning Existing Job ID :{job.id}")
            #     return job.id
            print(f"File {file_name} already present in folder id {folder_id}")
        else:
            info = self.trigger_analysis_for_upload_id(
                upload_id=upload_id,
                folder_id=folder_id,
                # group_name=self.group_name
            )
            print(f"Computed new Job ID is :{info.message}")
            return info.message

    # trigger_analysis_for_git_upload_package(
    #     git_url='https://github.com/dineshr93/pageres', branch_name='master', folder_id=1)

    def delete_uploads_by_upload_id(self, upload_id: int) -> Info:
        """Delete the upload by given upload id"""
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "DELETE",
            self.url + str(f"uploads/{upload_id}"),
            data=payload,
            headers=headers,
        )

        match response.json():
            case {**info}:
                report_info = Info(**info)
                print(f"{report_info.message}")
                return report_info
            case _:
                print(response.text)

    # delete_uploads_by_upload_id(upload_id=7, group_name=group_name)

    def get_all_license_based_on(
        self, is_active: str, license_kind: Kind, page: int, limit: int
    ) -> List[License]:
        """
        get_all_license_based_on(is_active: str, license_kind: Kind, limit: int) -> List[License]

        is_active must be true or false

        class Kind(Enum):
        candidate = 'candidate'
        main = 'main'
        all = 'all'
        """
        querystring = {"kind": license_kind.name}

        payload = ""
        headers = {
            "accept": "application/json",
            "page": str(page),
            "limit": str(limit),
            "active": is_active.lower(),
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET",
            self.url + str("license"),
            data=payload,
            headers=headers,
            params=querystring,
        )

        match response.json():
            case [*args]:
                licenses = [License(**license) for license in args]
                # for lic in licenses:
                #     print('======')
                #     print(lic)
                return licenses
            case {**info}:
                report_info = Info(**info)
                print(f"{report_info.message}")
                return report_info
            case _:
                print(response.text)

    # get_all_license_based_on(
    #     is_active='true', license_kind=Kind.main, page=1, limit=1)

    def get_all_license_short_names_based_on(
        self,
        is_active: str,
        license_kind: Kind,
        page: int,
        contains_key: str,
        limit: int,
    ) -> List[str]:
        """
        get_all_license_short_names_based_on(is_active: str, license_kind: Kind, page: int, contains_key: str, limit: int) -> List[str]

        use contains_key to filter based on keywords.

        is_active must be true or false

        class Kind(Enum):
        candidate = 'candidate'
        main = 'main'
        all = 'all'
        """
        licenses = self.get_all_license_based_on(
            is_active=is_active,
            license_kind=license_kind,
            page=page,
            limit=limit,
            group_name=self.group_name,
        )
        license_shortnames = [
            license.shortName
            for license in licenses
            if contains_key.lower() in license.shortName.lower()
        ]
        if len(license_shortnames) > 0:
            return license_shortnames
        else:
            print("No License shortnames been found")
            return None

    # sns = get_all_license_short_names_based_on(
    #     is_active='true', license_kind=Kind.main, contains_key='gp', page=1, limit=10000)
    # for i, sn in enumerate(sns, start=1):
    #     print(f'{i}. {sn}')

    def get_license_by_short_name(self, short_name: str) -> LicenseShortnameGetResponse:
        """
        get_license_by_short_name(short_name: str) -> LicenseShortnameGetResponse
        {
        "id": 317,
        "shortName": "GPL",
        "fullName": "GNU General Public License",
        "text": "GPL is referenced without a version number. Please look up GPL in the License Admin to view the different versions.",
        "url": "",
        "risk": null,
        "isCandidate": false,
        "obligations": []
        }
        """
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET",
            self.url + str(f"license/{short_name}"),
            data=payload,
            headers=headers,
        )
        match response.json():
            case {**license_info} if response.status_code == 200:
                license_info = LicenseShortnameGetResponse(**license_info)
                print(f"{license_info}")
                return license_info
            case {**info} if response.status_code == 404:
                report_info = Info(**info)
                print(f"{report_info}")
                sys.exit(1)
            case _:
                print(response.text)
                sys.exit(1)

    # get_license_by_short_name(short_name='AGPL-1.0')

    def update_license_info_by_short_name(
        self,
        short_name: str,
        new_full_name: str,
        new_license_text: str,
        new_url: str,
        new_risk: int,
    ) -> Info:
        """update information about a specific license by shortname"""

        payload = {
            "fullName": new_full_name,
            "text": new_license_text,
            "url": new_url,
            "risk": new_risk,
        }
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Content-Type": "application/json",
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "PATCH",
            self.url + str(f"license/{short_name}"),
            json=payload,
            headers=headers,
        )

        match response.json():
            case {**info} if response.status_code == 200:
                report_info = Info(**info)
                print(f"{report_info}")
                return report_info
            case _:
                print(response.text)

    # update_license_info_by_short_name(short_name='', new_full_name='', new_license_text='', new_url='', new_risk=2)

    def add_new_license(
        self,
        unique_short_name: str,
        new_full_name: str,
        new_license_text: str,
        new_url: str,
        new_risk: int,
        isCandidate: bool,
        merge_request: bool,
    ) -> Info:
        """add_new_license(unique_short_name: str, new_full_name: str, new_license_text: str, new_url: str, new_risk: int, isCandidate: bool, merge_request: bool):"""
        payload = {
            "shortName": unique_short_name,
            "fullName": new_full_name,
            "text": new_license_text,
            "url": new_url,
            "risk": new_risk,
            "isCandidate": isCandidate,
            "mergeRequest": merge_request,
        }
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Content-Type": "application/json",
            "Authorization": self.bearer_token,
        }

        response = requests.request("POST", self.url, json=payload, headers=headers)

        match response.json():
            case {**info} if response.status_code == 200:
                report_info = Info(**info)
                print(f"{report_info}")
                return report_info
            case {**info} if response.status_code == 409:
                report_info = Info(**info)
                print(f"{report_info}")
                return report_info
            case _:
                print(response.text)

    # add_new_license(unique_short_name='', new_full_name='', new_license_text='',
    #                 new_url='', new_risk=2, isCandidate=True, merge_request=False)

    def search_files_based_on(
        self,
        filename_wildcard: str,
        searchType: SearchType,
        uploadId: int,
        tag: str,
        filesizemin_bytes: int,
        filesizemax_bytes: int,
        license: str,
        copyright: str,
    ) -> List[SearchResults] | Info:
        """Most are optional parameters
        def search_files_based_on(self, filename_wildcard: str, searchType: SearchType, uploadId: int, tag: str, filesizemin_bytes: int, filesizemax_bytes: int, license: str, copyright: str) -> List[SearchResults] | Info:
        """
        payload = ""
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "searchType": searchType.name,
            "uploadId": uploadId,
            "filename": filename_wildcard,
            "tag": tag,
            "filesizemin": filesizemin_bytes,
            "filesizemax": filesizemax_bytes,
            "license": license,
            "copyright": copyright,
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "GET", self.url + str("search"), data=payload, headers=headers
        )

        match response.json():
            case [*args]:
                search_results = [
                    SearchResults(**search_result) for search_result in args
                ]
                for s in search_results:
                    print(s)
                # print(folders)
                return search_results
            case {**info}:
                report_info = Info(**info)
                print(f"{report_info.message}")
                return report_info
            case _:
                print(response.text)

    def get_file_by_any_one_of_sha1_or_md5_or_sha256(
        self, sha1: str = "", md5: str = "", sha256: str = ""
    ) -> str | List[File]:
        """def get_file_by_any_one_of_sha1_or_md5_or_sha256(self, sha1: str = '', md5: str = '', sha256: str = '') -> str | List[File]"""
        json_params = ""
        if sha1 != "":
            json_params = str(f'"sha1": {sha1}')
        else:
            json_params = ""
        if md5 != "":
            json_params = str(f'"md5": {md5}')
        else:
            json_params = ""
        if sha256 != "":
            json_params = str(f'"sha256": {sha256}')
        else:
            json_params = ""

        if json_params == "":
            print("Please provide any_one_of_sha1_or_md5_or_sha256 values")
            sys.exit(1)
        payload = [{json_params}]
        headers = {
            "accept": "application/json",
            "groupName": self.group_name,
            "Content-Type": "application/json",
            "Authorization": self.bearer_token,
        }

        response = requests.request(
            "POST", self.url + str("filesearch"), json=payload, headers=headers
        )

        match response.json():
            case [{"message": error_message}]:
                print(error_message)
                return error_message
            case [*args]:
                files = [File(**file) for file in args]
                for f in files:
                    print(f)
                # print(folders)
                return files
            case _:
                print(response.text)
