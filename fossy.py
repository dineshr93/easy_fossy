
from models import (
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
from typing import List

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
            config['token_expire'] = str(
                token_expire_yyyy_mm_dd)
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
# print(bearer_token)


def get_all_jobs() -> List[Job]:
    payload = ""
    headers = {
        "accept": "application/json",
        "limit": "1000",
        "page": "1",
        "groupName": "fossy",
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('jobs'), data=payload, headers=headers)

    match response.json():
        case [*args]:
            jobs = []
            for job in args:
                jobs.append(Job(**job))

            # print(jobs)
            return jobs
        case _:
            print(response.text)
# get_all_jobs()


def get_job_by_id(id: int) -> Job:
    payload = ""
    headers = {
        "accept": "application/json",
        "Authorization": bearer_token
    }

    response = requests.request(
        "GET", url+str('jobs/')+str(id), data=payload, headers=headers)

    match response.json():
        case {**job}:
            job = Job(**job)
            print(job)
            return job
        case _:
            print(response.text)

# get_job_by_id(3)


def generate_and_get_desired_report_for_uploadid(upload_id: int, report_format: ReportFormat) -> Info:
    payload = ""
    headers = {
        "accept": "application/json",
        "uploadId": str(upload_id),
        "reportFormat": str(report_format.name),
        "groupName": "fossy",
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
        "groupName": "fossy",
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


# generate_and_get_desired_report_for_uploadid(3, ReportFormat.unifiedreport)
