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
    ReportFormat
)
from easy_fossy import (
    create_new_user_group,
    get_user_group,

    get_all_jobs,
    get_job_info_by_id,
    generate_and_get_desired_report_for_uploadid,

    get_all_folders,
    get_folder_info_by_id,
    change_folder_name_or_desc,
    create_folder_under_parent_folder_id,
    apply_action_to_folderid,



    trigger_analysis_for_upload_package,
    trigger_analysis_for_upload_id,
    get_licenses_found_by_agents_for_uploadid,
    get_all_uploads_based_on,
    get_upload_summary_for_uploadid,
    get_upload_id_by_local_package_upload,



    delete_folder_by_id,
    delete_uploads_by_upload_id

)


group_name = get_user_group()

print(group_name)

# print(get_all_jobs(group_name))
# print(get_all_folders(group_name))

# get_job_info_by_id(upload_id=3,group_name=group_name)

# trigger_analysis_for_upload_package(
#     file_path='uploads/commons-lang3-3.12.0-src.zip', folder_id=1, group_name=group_name)

# uploads = get_all_uploads_based_on(folder_id=1, is_recursive=True,
#                                    search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000, group_name=group_name)
# print(len(uploads))

# out = get_licenses_found_by_agents_for_uploadid(upload_id=2, show_directories=True, group_name=group_name, agents=[
#     Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name, Agent.reportImport.name, Agent.reso.name])
# print(out)

# change_folder_name_or_desc(folder_id=3, new_folder_name='', new_folder_desc='',group_name=group_name)

# get_upload_summary_for_uploadid(upload_id=2,group_name=group_name)

# create_folder_under_parent_folder_id(
#     parent_folder_id=1, folder_name='test',group_name=group_name)

# delete_uploads_by_upload_id(upload_id=7, group_name=group_name)

# delete_folder_by_id(folder_id=3,group_name=group_name)

# apply_action_to_folderid(actions=Action.copy, folder_id=5, parent_folder_id=2,group_name=group_name)


# get_folder_info_by_id(folder_id=11,group_name=group_name)

# generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)

# trigger_analysis_for_upload_id(
#     upload_id=4, folder_id=1, group_name=group_name)

# get_upload_id_by_local_package_upload(
#     file_path='uploads/commons-io-2.11.0-src.zip', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public,group_name=group_name)
