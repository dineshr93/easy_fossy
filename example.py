"""
easy_fossy usage examples — OLD vs NEW API.

The old monolithic ``fossy`` facade (single object with ~60 flat methods) is
commented out below (the "OLD WAY"). The current library exposes the same
capabilities through typed resources on the client (``f.users``, ``f.folders``,
``f.uploads``, ``f.jobs``, ``f.groups``, ``f.licenses``, ``f.reports``).

Run with:  poetry run python example.py
"""

from easy_fossy import (
    ReportFormat,
    Agent,
)
from easy_fossy import easy_fossy as fossy


# Same client either way: the factory returns a FossyClient.
f = fossy("config.ini", "test")


# ---------------------------------------------------------------------------
# OLD WAY  (commented off — legacy flat methods on the monolithic object)
# ---------------------------------------------------------------------------
# create_new_user_group,
# get_user_group,
# get_all_users()
# get_user_by_id(user_id=3)
# get_all_jobs,
# get_job_info_by_id,
# generate_and_get_desired_report_for_uploadid,
#
# get_all_folders,
# get_folder_info_by_id,
# change_folder_name_or_desc,
# create_folder_under_parent_folder_id,
# apply_action_to_folderid,
#
# trigger_analysis_for_upload_package,
# trigger_analysis_for_upload_id,
# get_licenses_found_by_agents_for_uploadid,
# get_all_uploads_based_on,
# get_upload_summary_for_uploadid,
# get_upload_id_by_local_package_upload,
#
# delete_folder_by_id,
# delete_uploads_by_upload_id
#
# f.get_job_info_by_id(101)
#
# # job_names = f.get_all_jobs()
# # job_names.sort(key=lambda x: x.id, reverse=True)
# # print(job_names[0])
#
# # f.get_all_jobs(group_name)
# # f.get_all_folders(group_name)
#
# # f.trigger_analysis_for_upload_package(
# #     file_path='uploads/commons-lang3-3.12.0-src.zip', folder_id=1, group_name=group_name)
#
# # f.get_all_uploads_based_on(folder_id=1, is_recursive=True,
# #                            search_pattern_key='', upload_status=ClearingStatus.Open,
# #                            assignee='', since_yyyy_mm_dd='', page=1, limit=1000,
# #                            group_name=group_name)
#
# # out = f.get_licenses_found_by_agents_for_uploadid(
# #     upload_id=2, show_directories=True, group_name=group_name, agents=[
# #         Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name,
# #         Agent.reportImport.name, Agent.reso.name])
#
# # f.change_folder_name_or_desc(folder_id=3, new_folder_name='', new_folder_desc='', group_name=group_name)
#
# # f.get_upload_summary_for_uploadid(upload_id=2, group_name=group_name)
#
# # f.create_folder_under_parent_folder_id(parent_folder_id=1, folder_name='test', group_name=group_name)
#
# # f.delete_uploads_by_upload_id(upload_id=7, group_name=group_name)
#
# # f.delete_folder_by_id(folder_id=3, group_name=group_name)
#
# # f.apply_action_to_folderid(actions=Action.copy, folder_id=5, parent_folder_id=2, group_name=group_name)
#
# # f.get_folder_info_by_id(folder_id=11, group_name=group_name)
#
# # f.generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)
#
# # f.trigger_analysis_for_upload_id(upload_id=4, folder_id=1, group_name=group_name)
#
# # f.get_upload_id_by_local_package_upload(
# #     file_path='uploads/commons-io-2.11.0-src.zip', folder_id=1,
# #     upload_desc='commons-io-2.11.0', visibility=Public.public, group_name=group_name)


# ---------------------------------------------------------------------------
# NEW WAY  (resource-based API — uncomment one at a time to run)
# ---------------------------------------------------------------------------

# --- Users: f.users --------------------------------------------------------
# f.users.get_all()                       # was: get_all_users()
# f.users.get_by_id(3)                    # was: get_user_by_id(user_id=3)
# f.users.get_self()
# f.users.get_tokens("active")
# f.users.create_token({...})             # create a REST API token

# --- Groups: f.groups ------------------------------------------------------
# f.groups.get_all()                      # was: get_user_group()
# f.groups.create("suite_group", "desc")  # was: create_new_user_group()
# f.groups.get_users_with_roles(group_id)
# f.groups.add_member(group_id, user_id)
# f.groups.delete_member(group_id, user_id)
# f.groups.update_permission(group_id, user_id, level)
# f.groups.delete(group_id)

# --- Folders: f.folders ----------------------------------------------------
# f.folders.get_all()                     # was: get_all_folders()
# f.folders.get_by_id(folder_id)          # was: get_folder_info_by_id()
# f.folders.create(parent_folder_id=1, folder_name="test")  # was: create_folder_under_parent_folder_id()
# f.folders.update(folder_id, "newname", "new desc")        # was: change_folder_name_or_desc()
# f.folders.move(folder_id, target_parent_id)               # was: apply_action_to_folderid(actions=Action.move)
# f.folders.get_contents(folder_id)
# f.folders.delete(folder_id)             # was: delete_folder_by_id()

# --- Uploads: f.uploads ----------------------------------------------------
# f.uploads.get_all_uploads(folder_id=1)  # was: get_all_uploads_based_on(folder_id=1, ...)
# f.uploads.get_upload_by_id(upload_id)   # was: get_upload_summary_for_uploadid()
# f.uploads.upload_file("uploads/commons-io-2.11.0-src.zip", folder_id=1)  # was: get_upload_id_by_local_package_upload()
# f.uploads.upload_by_url("https://...", folder_id=1)
# f.uploads.upload_by_giturl("git://...", folder_id=1)
# f.uploads.trigger_analysis_for_upload_id(upload_id, folder_id=1)  # was: trigger_analysis_for_upload_id()
# f.uploads.delete_uploads_by_upload_id(upload_id)                 # was: delete_uploads_by_upload_id()

# --- Jobs: f.jobs ----------------------------------------------------------
# f.jobs.get_all()                        # was: get_all_jobs()
# f.jobs.get_by_id(job_id)                # was: get_job_info_by_id()
# f.jobs.get_all_admin()
# f.jobs.get_statistics()

# --- Licenses: f.licenses --------------------------------------------------
# f.licenses.get_all()                    # was: get_all_license_based_on() / get_all_license_short_names_based_on()
# f.licenses.get_by_short_name("MIT")     # was: get_license_by_short_name()
# f.licenses.get_histogram(upload_id=2)   # was: get_licenses_found_by_agents_for_uploadid()
# f.licenses.add(unique_short_name="X", new_full_name="...", new_license_text="...", new_url="...", new_risk=0)

# --- Reports: f.reports (new) ---------------------------------------------
# f.reports.get_reports_by_upload(upload_id, ReportFormat.unifiedreport)
# f.reports.download_report(report_id)
# f.reports.generate_and_get_desired_report_for_uploadid(
#     upload_id, ReportFormat.unifiedreport, save_to="reports/report.txt")  # was: generate_and_get_desired_report_for_uploadid()

# --- Backward-compat conveniences still on the client ----------------------
# f.get_all_users()
# f.get_user_by_id(3)
# f.get_all_jobs()
# f.get_job_info_by_id(101)
# f.get_upload_by_id(upload_id)
# f.upload_file("uploads/commons-io-2.11.0-src.zip", folder_id=1)
# f.generate_and_get_desired_report_for_uploadid(upload_id, ReportFormat.unifiedreport)

# ---------------------------------------------------------------------------
# One concrete end-to-end example (commented — uncomment to run live)
# ---------------------------------------------------------------------------
# upload = f.uploads.upload_file("uploads/commons-lang3-3.12.0-src.zip", folder_id=1)
# report_body = f.reports.generate_and_get_desired_report_for_uploadid(
#     upload.id, ReportFormat.unifiedreport, save_to="reports/unifiedreport.txt")
# print(upload.id, report_body[:200])
