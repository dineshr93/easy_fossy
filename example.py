from easy_fossy import (
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
    ReportFormat,
)
from easy_fossy import easy_fossy as fossy


f = fossy("config.ini", "test")

# create_new_user_group,
# get_user_group,
# get_all_users()
# get_user_by_id(user_id=3)
# get_all_jobs,
# get_job_info_by_id,
# generate_and_get_desired_report_for_uploadid,

# get_all_folders,
# get_folder_info_by_id,
# change_folder_name_or_desc,
# create_folder_under_parent_folder_id,
# apply_action_to_folderid,

# trigger_analysis_for_upload_package,
# trigger_analysis_for_upload_id,
# get_licenses_found_by_agents_for_uploadid,
# get_all_uploads_based_on,
# get_upload_summary_for_uploadid,
# get_upload_id_by_local_package_upload,

# delete_folder_by_id,
# delete_uploads_by_upload_id
# print(dir(f))


# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'add_new_license', 'apply_action_to_folderid', 'bearer_token', 'change_folder_name_or_desc', 'check_url_exists', 'config', 'config_file', 'config_parser', 'create_folder_under_parent_folder_id', 'create_new_user_group', 'delete_folder_by_id', 'delete_uploads_by_upload_id', 'dt_format', 'generate_and_get_desired_report_for_uploadid', 'get_all_folders', 'get_all_jobs', 'get_all_license_based_on', 'get_all_license_short_names_based_on', 'get_all_uploads_based_on', 'get_file_by_any_one_of_sha1_or_md5_or_sha256', 'get_folder_info_by_id', 'get_job_info_by_id', 'get_job_info_by_upload_id', 'get_license_by_short_name', 'get_licenses_found_by_agents_for_uploadid', 'get_token_by_uname_pwd', 'get_upload_id_by_download_url_package_upload', 'get_upload_id_by_giturl_package_upload', 'get_upload_id_by_local_package_upload', 'get_upload_summary_for_uploadid', 'group_name', 'now', 'reports_location', 'search_files_based_on', 'server', 'set_config_ini_file_full_path', 'today', 'token_expire', 'token_expire_yyyy_mm_dd', 'trigger_analysis_for_git_upload_package', 'trigger_analysis_for_upload_id', 'trigger_analysis_for_upload_package', 'trigger_analysis_for_url_upload_package', 'update_license_info_by_short_name', 'url']

f.get_job_info_by_id(101)

# job_names = f.get_all_jobs()
# job_names.sort(key=lambda x: x.id, reverse=True)
# print(job_names[0])

# print(f.get_all_jobs(group_name))
# print(f.get_all_folders(group_name))

# f.get_job_info_by_id(upload_id=3,group_name=group_name)

# f.trigger_analysis_for_upload_package(
#     file_path='uploads/commons-lang3-3.12.0-src.zip', folder_id=1, group_name=group_name)

# uploads = f.get_all_uploads_based_on(folder_id=1, is_recursive=True,
#                                    search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000, group_name=group_name)
# print(len(uploads))

# out = f.get_licenses_found_by_agents_for_uploadid(upload_id=2, show_directories=True, group_name=group_name, agents=[
#     Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name, Agent.reportImport.name, Agent.reso.name])
# print(out)

# f.change_folder_name_or_desc(folder_id=3, new_folder_name='', new_folder_desc='',group_name=group_name)

# f.get_upload_summary_for_uploadid(upload_id=2,group_name=group_name)

# f.create_folder_under_parent_folder_id(
#     parent_folder_id=1, folder_name='test',group_name=group_name)

# f.delete_uploads_by_upload_id(upload_id=7, group_name=group_name)

# f.delete_folder_by_id(folder_id=3,group_name=group_name)

# f.apply_action_to_folderid(actions=Action.copy, folder_id=5, parent_folder_id=2,group_name=group_name)


# f.get_folder_info_by_id(folder_id=11,group_name=group_name)

# f.generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)

# f.trigger_analysis_for_upload_id(
#     upload_id=4, folder_id=1, group_name=group_name)

# f.get_upload_id_by_local_package_upload(
#     file_path='uploads/commons-io-2.11.0-src.zip', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public,group_name=group_name)
