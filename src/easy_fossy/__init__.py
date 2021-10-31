
from .models import (
    Public,
    Findings,
    ClearingStatus,
    Action,
    Action1,
    Agent,
    ApiInfo,
    File,
    Folder,
    Group,
    Hash,
    HeathInfo,
    Info,
    Job,
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
    ReportFormat
)

import requests
import time
import configparser
import datetime
import sys
from pathlib import Path
from typing import List
from requests_toolbelt.multipart.encoder import MultipartEncoder

config_parser = configparser.ConfigParser()
config_file = 'config.ini'
config_parser.read(config_file)
config = config_parser['test']
url = config.get('url')

token_expire = config.get('token_expire')
reports_location = config.get('reports_location')

today = datetime.date.today()

now = datetime.datetime.now()
dt_format = "%d-%m-%Y %H:%M"
# print(today)
# print(now.strftime(dt_format))
token_expire_yyyy_mm_dd = today + \
    datetime.timedelta(days=config.getint('token_valdity_days'))

bearer_token = config.get('bearer_token')
if token_expire:
    token_expire_datetime = datetime.date.fromisoformat(token_expire)
else:
    token_expire_datetime = None
# config = config['prod']


def create_new_user_group(new_group_name: str) -> str:
    payload = ""
    headers = {
        "accept": "application/json",
        "name": new_group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "POST", url+str('groups'), data=payload, headers=headers)

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'{report_info.message}')
            return new_group_name
        case _:
            print(response.text)


def get_user_group():
    group_name = config.get('group_name')
    if not group_name:
        config['group_name'] = str(
            create_new_user_group(new_group_name='fossy'))
        with open(config_file, 'w') as cf:
            config_parser.write(cf)
        return get_user_group()


def get_token_by_uname_pwd() -> str:
    """Get the token via user name and password in the config"""
    payload = {
        "username": config.get('uname'),
        "password": config.get('pwd'),
        "token_name": str('created_viaapi_on_')+str(now.strftime(dt_format)),
        "token_scope": config.get('access'),
        "token_expire": str(token_expire_yyyy_mm_dd)
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST", url+str('tokens'), json=payload, headers=headers)

    match response.json():
        case {"Authorization": bearer_token}:
            config['bearer_token'] = bearer_token
            config['token_expire'] = str(token_expire_yyyy_mm_dd)
            with open(config_file, 'w') as cf:
                config_parser.write(cf)
            return bearer_token
        case _:
            print('Error while getting token')
            print(response.text)
            sys.exit(1)


if(not bearer_token or not token_expire_datetime or (today > token_expire_datetime)):
    get_token_by_uname_pwd()
else:
    print('Re using the existing unexpired Token')

bearer_token = config.get('bearer_token')
print(bearer_token)


def get_all_jobs(group_name) -> List[Job]:
    """List of jobs present in the given instance"""
    payload = ""
    headers = {
        "accept": "application/json",
        "limit": "1000",
        "page": "1",
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('jobs'), data=payload, headers=headers)

    match response.json():
        case [*args]:
            jobs = []
            for job in args:
                jobs.append(Job(**job))
            # for j in jobs:
            #     print(jobs)
            return jobs
        case _:
            print(response.text)


# get_all_jobs(group_name)


def get_job_info_by_id(job_id: int, group_name='') -> Job:
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
    headers = {
        "accept": "application/json",
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('jobs/')+str(job_id), data=payload, headers=headers)

    match response.json():
        case {**job}:
            job = Job(**job)
            print(job)
            return job
        case _:
            print(response.text)

# get_job_info_by_job_id(job_id=3,group_name=group_name)


def get_job_info_by_upload_id(upload_id: int, group_name='') -> Job:
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
    headers = {
        "accept": "application/json",
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('jobs?upload=')+str(upload_id), data=payload, headers=headers)

    match response.json():
        case {**job}:
            job = Job(**job)
            print(job)
            return job
        case _:
            print(response.text)

# get_job_info_by_job_id(job_id=3,group_name=group_name)


def generate_and_get_desired_report_for_uploadid(upload_id: int, report_format: ReportFormat):
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
        "groupName": group_name,
        "Authorization": bearer_token
    }
    report_info: Info = None
    report_id: int = None
    response = requests.request(
        "GET", url+str('report'), data=payload, headers=headers)

    match response.json():
        case {"message": url_with_report_id}:
            report_id = url_with_report_id.rsplit('/', 1).pop()
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
        "groupName": group_name,
        "Authorization": bearer_token
    }
    timeout = 20
    timewait = 0.2
    timer = 0
    response = requests.request(
        "GET", url+str('report/')+str(report_id), data=payload, headers=headers)
    while response.status_code != 200:

        print(f'waiting for {timewait} sec')
        time.sleep(timewait)
        response = requests.request(
            "GET", url+str('report/')+str(report_id), data=payload, headers=headers)
        if timer > timeout:
            break
        if response.status_code == 200:
            break

    # print(response.headers)
    file_name = response.headers.get(
        "Content-Disposition").split("filename=")[1]
    path_with_file = reports_location+str(file_name.replace('"', ''))

    if report_format != ReportFormat.unifiedreport:
        with open(path_with_file, 'w', encoding="utf-8") as f:
            f.write(response.text)
    else:
        with open(path_with_file, 'wb') as f:
            for chunk in response.iter_content(1024 * 1024 * 2):  # 2 MB chunks
                f.write(chunk)

# generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)


def get_all_folders(group_name) -> List[Folder]:
    """ Get all the folders in given fossy instance"""
    payload = ""
    headers = {
        "accept": "application/json",
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('folders'), data=payload, headers=headers)

    match response.json():
        case [*args]:
            folders = []
            for folder in args:
                folders.append(Folder(**folder))
            for f in folders:
                print(f)
            # print(folders)
            return folders
        case _:
            print(response.text)


# get_all_folders(group_name)


def get_folder_info_by_id(folder_id: int, group_name: str) -> Folder:
    """get_folder_info_by_id(folder_id: int, group_name: str) -> Folder"""
    payload = ""
    headers = {
        "accept": "application/json",
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('folders/')+str(folder_id), data=payload, headers=headers)

    match response.json():
        case {**args}:
            folder = Folder(**args)
            print(folder)
            return folder
        case _:
            print(response.text)


# get_folder_info_by_id(folder_id=11,group_name=group_name)


def change_folder_name_or_desc(folder_id: int, new_folder_name: str = '', new_folder_desc: str = '', group_name: str = ''):
    """name and desc are optional, mandatory input is the folder id"""
    payload = ""
    headers = {
        "accept": "application/json",
        "name": new_folder_name,
        "description": new_folder_desc,
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "PATCH", url+str('folders/')+str(folder_id), data=payload, headers=headers)
    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(report_info.message)
            return report_info
        case _:
            print(response.text)


# change_folder_name_or_desc(folder_id=3, new_folder_name='', new_folder_desc='',group_name=group_name)

# change_folder_name_or_desc(folder_id=2, new_folder_name='', new_folder_desc = 'scans triggered from sw360 test',group_name=group_name)
# get_all_folders()


def create_folder_under_parent_folder_id(parent_folder_id: int, folder_name: str, group_name: str) -> Info:
    """create the folder under parent folder id with given folder_name"""
    payload = ""
    headers = {
        "accept": "application/json",
        "parentFolder": str(parent_folder_id),
        "folderName": folder_name,
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "POST", url+str('folders'), data=payload, headers=headers)

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'Created folder id is {report_info.message}')
            return report_info
        case _:
            print(response.text)


# create_folder_under_parent_folder_id(
#     parent_folder_id=1, folder_name='test',group_name=group_name)
# create_folder_under_parent_folder_id(
#     parent_folder_id=6, folder_name='submove',group_name=group_name)
# get_all_folders()


def delete_folder_by_id(folder_id: int, group_name: str):
    """delete_folder_by_id(folder_id: int, group_name: str)"""
    payload = ""
    headers = {
        "accept": "application/json",
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "DELETE", url+str('folders/')+str(folder_id), data=payload, headers=headers)

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'Deleted folder is {report_info.message}')
            # return report_info
        case _:
            print(response.text)

# delete_folder_by_id(folder_id=3,group_name=group_name)
# get_all_folders()


def apply_action_to_folderid(actions: Action, folder_id: int, parent_folder_id: int, group_name: str) -> Info:
    """apply_action_to_folderid(actions: Action, folder_id: int, parent_folder_id: int, group_name: str) -> Info"""
    payload = ""
    headers = {
        "accept": "application/json",
        "parent": str(parent_folder_id),
        "action": actions.name,
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "PUT", url+str('folders/')+str(folder_id), data=payload, headers=headers)

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'{report_info.message}')
            return report_info
        case _:
            print(response.text)


# apply_action_to_folderid(actions=Action.copy, folder_id=5, parent_folder_id=2,group_name=group_name)
# apply_action_to_folderid(actions=Action.move, folder_id=6, parent_folder_id=2,group_name=group_name)

# change_folder_name_or_desc(folder_id=11, new_folder_name='',
#                            new_folder_desc='scans triggered from sw360 test',group_name=group_name)

# get_all_folders('fossy')


def get_upload_summary_for_uploadid(upload_id: int, group_name: str) -> UploadSummary:
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
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str(f'uploads/{upload_id}/summary'), data=payload, headers=headers)
    match response.json():
        case {**info}:
            upload_summary = UploadSummary(**info)
            print(
                f'Returned upload summary for file {upload_summary.uploadName}')
            return upload_summary
        case _:
            print(response.text)


# get_upload_summary_for_uploadid(upload_id=2,group_name=group_name)

def get_all_uploads_based_on(folder_id: int, is_recursive: bool, search_pattern_key: str, upload_status: ClearingStatus, assignee: str, since_yyyy_mm_dd: str, page: int, limit: int, group_name: str) -> List[Upload]:
    """get_all_uploads_based_on(folder_id: int, is_recursive: bool, search_pattern_key: str, upload_status: ClearingStatus, assignee: str, since_yyyy_mm_dd: str, page: int, limit: int, group_name: str) -> List[Upload]"""
    querystring = {"folderId": folder_id, "recursive": is_recursive, "name": search_pattern_key,
                   "status": upload_status.name, "assignee": assignee, "since": since_yyyy_mm_dd}

    payload = ""
    headers = {
        "accept": "application/json",
        "groupName": group_name,
        "page": str(page),
        "limit": str(limit),
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('uploads'), data=payload, headers=headers, params=querystring)

    match response.json():
        case [*args]:
            uploads = []
            for upload in args:
                uploads.append(Upload(**upload))
            # for upload in uploads:
            #     print(upload)
            return uploads
        case _:
            print(response.text)


# get_all_uploads_based_on(folder_id=1, is_recursive=True,
#                          search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000,group_name=group_name)


def get_licenses_found_by_agents_for_uploadid(upload_id: int, agents: List[str], show_directories: bool, group_name: str) -> UploadLicenses | Info:
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
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str(f'uploads/{upload_id}/licenses'), data=payload, headers=headers, params=querystring)

    match response.json():
        case [*args]:
            UploadLicenses = []
            for uploadLicense in args:
                UploadLicenses.append(UploadLicense(**uploadLicense))
            for f in UploadLicenses:
                print(f)
            # print(folders)
            return UploadLicenses
        case {**info}:
            report_info = Info(**info)
            print(f'{report_info.message}')
            return report_info
        case _:
            print(response.text)


# get_licenses_found_by_agents_for_uploadid(upload_id=2, show_directories=True, group_name=group_name, agents=[
#                                           Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name, Agent.reportImport.name, Agent.reso.name])

def get_upload_id_by_local_package_upload(file_path: str, folder_id: int, upload_desc: str, visibility: Public, group_name: str) -> str:
    """get_upload_id_by_local_package_upload(file_path: str, folder_id: int, upload_desc: str, visibility: Public, group_name: str) -> str"""
    # files = {'file': open(file_path, 'rb')}

    if Path(file_path).exists():
        print(f'File path {file_path} exists')

    file_name = file_path.split('/').pop()
    print(file_name)
    m = MultipartEncoder([('fileInput', (file_name, open(
        file_path, 'rb'), 'application/octet-stream'))],
        None, encoding='utf-8')
    headers = {
        # "accept": "application/json",
        "folderId": str(folder_id),
        "groupName": group_name,
        "uploadDescription": upload_desc,
        "public": visibility.name,
        "Content-Type": m.content_type,
        "Authorization": bearer_token
    }
    response = requests.post(url+str('uploads'), data=m, headers=headers)

    timeout = 20
    timewait = 0.2
    timer = 0

    while response.status_code != 201:

        print(f'waiting for {timewait} sec')
        time.sleep(timewait)
        response = requests.post(url+str('uploads'), data=m, headers=headers)
        timer = timer+timewait
        if timer > timeout:
            break
        if response.status_code == 201:
            break

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'upload id is {report_info.message}')
            return report_info.message
        case _:
            print(response.text)


# get_upload_id_by_local_package_upload(
#     file_path='uploads/commons-io-2.11.0-src.zip', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public,group_name=group_name)

def check_url_exists(url: str):
    """
    Checks if a url exists
    :param url: url to check
    :return: True if the url exists, false otherwise.
    """
    return requests.head(url, allow_redirects=True).status_code == 200


def get_upload_id_by_download_url_package_upload(file_download_url: str, file_name: str, folder_id: int, upload_desc: str, visibility: Public, group_name: str) -> str:
    """get_upload_id_by_download_url_package_upload(file_download_url: str, file_name: str, folder_id: int, upload_desc: str, visibility: Public, group_name: str) -> str"""
    # files = {'file': open(file_path, 'rb')}
    if not check_url_exists(file_download_url):
        print(f'git url {file_download_url} is malformed')

    m = MultipartEncoder(fields={'url': file_download_url, 'name': file_name})
    headers = {
        # "accept": "application/json",
        "folderId": str(folder_id),
        "groupName": group_name,
        "uploadType": 'url',
        "uploadDescription": upload_desc,
        "public": visibility.name,
        "Content-Type": m.content_type,
        "Authorization": bearer_token
    }
    response = requests.post(url+str('uploads'), data=m, headers=headers)

    timeout = 20
    timewait = 0.2
    timer = 0

    while response.status_code != 201:

        print(f'waiting for {timewait} sec')
        time.sleep(timewait)
        response = requests.post(url+str('uploads'), data=m, headers=headers)
        # print(response.text)
        timer = timer+timewait
        if timer > timeout:
            break
        if response.status_code == 201:
            break

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'upload id is {report_info.message}')
            return report_info.message
        case _:
            print(response.text)


# get_upload_id_by_download_url_package_upload(
#     file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip', file_name='pageres', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public, group_name='fossy')


def get_upload_id_by_giturl_package_upload(git_url: str, branch_name: str, upload_name: str, folder_id: int, upload_desc: str, visibility: Public, group_name: str) -> str:
    """get_upload_id_by_giturl_package_upload(git_url: str, branch_name: str, upload_name: str, folder_id: int, upload_desc: str, visibility: Public, group_name: str) -> str"""
    # files = {'file': open(file_path, 'rb')}

    if not check_url_exists(git_url):
        print(f'git url {git_url} is malformed')

    file_name = git_url.split('/').pop()
    print(file_name)

    payload = {
        "vcsType": "git",
        "vcsUrl": git_url,
        "vcsBranch": branch_name,
        "vcsName": upload_name
    }
    headers = {
        # "accept": "application/json",
        "folderId": str(folder_id),
        "uploadDescription": upload_desc,
        "public": visibility.name,
        "ignoreScm": 'true',
        'uploadType': 'vcs',
        "groupName": group_name,
        # "Content-Type": "application/json",
        "Authorization": bearer_token
    }

    response = requests.request(
        "POST", url+str('uploads'), json=payload, headers=headers)

    # print(response.status_code)
    # print(response.text)

    timeout = 20
    timewait = 0.2
    timer = 0

    while response.status_code != 201:

        print(f'waiting for {timewait} sec')
        time.sleep(timewait)
        response = requests.request(
            "POST", url+str('uploads'), json=payload, headers=headers)
        print(response.json())
        timer = timer + timewait
        if timer > timeout:
            break
        if response.status_code == 201:
            break

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'upload id is {report_info.message}')
            return report_info.message
        case _:
            print(response.text)


# get_upload_id_by_giturl_package_upload(git_url='https://github.com/dineshr93/pageres', branch_name='master', upload_name='',
#                                        folder_id=1, upload_desc='', visibility=Public.public, group_name='fossy')


def trigger_analysis_for_upload_id(upload_id: int, folder_id: int, group_name: str) -> Info:
    """trigger_analysis_for_upload_id(upload_id: int, folder_id: int, group_name: str) -> Info"""
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
            "reso": True
        },
        "decider": {
            "nomos_monk": True,
            "bulk_reused": True,
            "new_scanner": True,
            "ojo_decider": True
        },
        "reuse": {
            "reuse_upload": 0,
            "reuse_group": "string",
            "reuse_main": True,
            "reuse_enhanced": True,
            "reuse_report": True,
            "reuse_copyright": True
        }
    }
    headers = {
        "accept": "application/json",
        "folderId": str(folder_id),
        "uploadId": upload_id,
        "groupName": group_name,
        "Content-Type": "application/json",
        "Authorization": bearer_token
    }

    response = requests.request(
        "POST", url+str('jobs'), json=payload, headers=headers)
    timeout = 50
    timewait = 0.5
    timer = 0
    while response.status_code != 201:
        print(f'waiting for {timewait} sec')
        time.sleep(timewait)
        response = requests.request(
            "POST", url+str('jobs'), json=payload, headers=headers)
        print(response.text)
        timer = timer + timewait
        if timer > timeout:
            break
        if response.status_code == 201:
            break
    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'job id is {report_info.message}')
            return report_info
        case _:
            print(response.text)

# trigger_analysis_for_upload_id(
#     upload_id=4, folder_id=1, group_name=group_name)


def trigger_analysis_for_upload_package(file_path: str, folder_id: int, group_name: str):
    """trigger_analysis_for_upload_package(file_path: str, folder_id: int, group_name: str)"""
    if not Path(file_path).exists():
        print(f'File path {file_path} doesn\'t exist')

    uploads: List[Upload] = get_all_uploads_based_on(folder_id=folder_id, is_recursive=True,
                                                     search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000, group_name=group_name)
    file_name = file_path.split('/').pop()

    upload_id = [u.id for u in uploads if file_name == u.uploadname]
    size = len(upload_id)
    is_present_uploadID = False
    if size > 1:
        is_present_uploadID = True
        print(f'{size} no of duplicates are there with ids {upload_id}')
        print('exiting.. please comeback after deleting duplicates via delete_uploads_by_upload_id(upload_id=upload_id, group_name=group_name)')
        sys.exit(1)
    elif size == 1:
        is_present_uploadID = True
        upload_id = upload_id[0]
    else:
        # no upload_id is there
        upload_id = get_upload_id_by_local_package_upload(
            file_path=file_path, folder_id=folder_id, upload_desc=file_name, visibility=Public.protected, group_name=group_name)

    if is_present_uploadID:
        jobs: List[Job] = [
            j for j in get_all_jobs(group_name) if j.uploadId == upload_id]

        if len(jobs) >= 1:
            print(f'Multiple jobs exists for same upload_id: {upload_id}')
            job = jobs.pop()
            print(f' Returning Existing Job ID :{job.id}')
            return job.id
    else:
        info = trigger_analysis_for_upload_id(
            upload_id=upload_id, folder_id=folder_id, group_name=group_name)
        print(f'Computed new Job ID is :{info.message}')
        return info.message


# trigger_analysis_for_upload_package(
#     file_path='uploads/commons-lang3-3.12.0-src.zip', folder_id=1, group_name=group_name)

def trigger_analysis_for_url_upload_package(file_download_url: str, file_name: str, branch_name: str, folder_id: int, group_name: str):
    """trigger_analysis_for_url_upload_package(file_download_url: str, file_name: str, branch_name: str, folder_id: int, group_name: str)"""
    if not check_url_exists(file_download_url):
        print(f'git url {file_download_url} is malformed')

    uploads: List[Upload] = get_all_uploads_based_on(folder_id=folder_id, is_recursive=True,
                                                     search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000, group_name=group_name)

    upload_id = [u.id for u in uploads if file_name == u.uploadname]
    size = len(upload_id)
    is_present_uploadID = False
    if size > 1:
        is_present_uploadID = True
        print(f'{size} no of duplicates are there with ids {upload_id}')
        print('exiting.. please comeback after deleting duplicates via delete_uploads_by_upload_id(upload_id=upload_id, group_name=group_name)')
        sys.exit(1)
    elif size == 1:
        is_present_uploadID = True
        upload_id = upload_id[0]
    else:
        # no upload_id is there
        upload_id = get_upload_id_by_download_url_package_upload(
            file_download_url=file_download_url, file_name=file_name, folder_id=1, upload_desc=file_name, visibility=Public.public, group_name=group_name)

    if is_present_uploadID:
        jobs: List[Job] = [
            j for j in get_all_jobs(group_name) if j.uploadId == upload_id]

        if len(jobs) >= 1:
            print(f'Multiple jobs exists for same upload_id: {upload_id}')
            job = jobs.pop()
            print(f' Returning Existing Job ID :{job.id}')
            return job.id
    else:
        info = trigger_analysis_for_upload_id(
            upload_id=upload_id, folder_id=folder_id, group_name=group_name)
        print(f'Computed new Job ID is :{info.message}')
        return info.message


# trigger_analysis_for_url_upload_package(
#     file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip', file_name='pageres.zip', branch_name='', folder_id=1, group_name='fossy')


def trigger_analysis_for_git_upload_package(git_url: str, branch_name: str, folder_id: int, group_name: str):
    """trigger_analysis_for_git_upload_package(git_url: str, branch_name: str, folder_id: int, group_name: str)"""
    if not check_url_exists(git_url):
        print(f'git url {git_url} is malformed')

    file_name = git_url.split('/').pop()
    print(file_name)

    uploads: List[Upload] = get_all_uploads_based_on(folder_id=folder_id, is_recursive=True,
                                                     search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000, group_name=group_name)

    upload_id = [u.id for u in uploads if file_name == u.uploadname]
    size = len(upload_id)
    is_present_uploadID = False
    if size > 1:
        is_present_uploadID = True
        print(f'{size} no of duplicates are there with ids {upload_id}')
        print('exiting.. please comeback after deleting duplicates via delete_uploads_by_upload_id(upload_id=upload_id, group_name=group_name)')
        sys.exit(1)
    elif size == 1:
        is_present_uploadID = True
        upload_id = upload_id[0]
    else:
        # no upload_id is there
        upload_id = get_upload_id_by_giturl_package_upload(git_url=git_url, branch_name=branch_name, upload_name=file_name,
                                                           folder_id=1, upload_desc='', visibility=Public.public, group_name=group_name)

    if is_present_uploadID:
        jobs: List[Job] = [
            j for j in get_all_jobs(group_name) if j.uploadId == upload_id]

        if len(jobs) >= 1:
            print(f'Multiple jobs exists for same upload_id: {upload_id}')
            job = jobs.pop()
            print(f' Returning Existing Job ID :{job.id}')
            return job.id
    else:
        info = trigger_analysis_for_upload_id(
            upload_id=upload_id, folder_id=folder_id, group_name=group_name)
        print(f'Computed new Job ID is :{info.message}')
        return info.message


# trigger_analysis_for_git_upload_package(
#     git_url='https://github.com/dineshr93/pageres', branch_name='master', folder_id=1, group_name='fossy')


def delete_uploads_by_upload_id(upload_id: int, group_name: str) -> Info:
    """Delete the upload by given upload id"""
    payload = ""
    headers = {
        "accept": "application/json",
        "groupName": group_name,
        "Authorization": bearer_token
    }

    response = requests.request(
        "DELETE", url+str(f'uploads/{upload_id}'), data=payload, headers=headers)

    match response.json():
        case {**info}:
            report_info = Info(**info)
            print(f'{report_info.message}')
            return report_info
        case _:
            print(response.text)


# delete_uploads_by_upload_id(upload_id=7, group_name=group_name)
