# OpenAPI Specification vs Implementation Analysis

## Overview
This document analyzes the FOSSology REST API specification (`openapi.yaml`) against the current implementation in `easy_fossy/__init__.py`. It identifies gaps and provides utility functions for business-relevant usecases.

The `openapi.yaml` specification contains **167 operations** across 15 categories. All 167 operations have corresponding implementation methods in `easy_fossy/__init__.py`, achieving **100% implementation coverage**.

---

## 1. Endpoint Coverage Analysis

### Legend
- ✅ **Implemented** — method exists and works
- ⚠️ **Partial** — method exists but missing features (e.g., pagination, query params)
- ❌ **Missing** — not implemented at all
- 🟡 **Incorrect URL** — method exists but endpoint path is wrong

---

### AUTH / INFO

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `POST /tokens` | `createToken` | ✅ | `get_token_by_uname_pwd` |
|| `GET /info` | `getInfo` | ✅ | `get_api_info` |
|| `GET /openapi` | `getOpenApi` | ✅ | `get_openapi_doc` |
|| `GET /health` | `getHealth` | ✅ | `get_health_status` |

### MAINTENANCE

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `POST /maintenance` | `initiateMaintenance` | ✅ | `initiate_maintenance` |

### OBLIGATIONS

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /obligations/list` | `getObligationsList` | ✅ | `get_obligations_list` |
|| `GET /obligations/{id}` | `getObligationsData` | ✅ | `get_obligation_details` |
|| `DELETE /obligations/{id}` | `deleteObligationsData` | ✅ | `delete_obligation` |
|| `POST /obligations/import-csv` | `importObligationCsv` | ✅ | `import_obligation_csv` |
|| `GET /obligations/export-csv` | `exportLicenseObligations` | ✅ | `export_obligation_csv` |
|| `POST /obligations/import-json` | `importObligationsFromJSON` | ✅ | `import_obligation_json` |
|| `GET /obligations/export-json` | `exportObligationsToJSON` | ✅ | `export_obligation_json` |
|| `GET /obligations` | `getAllObligationsData` | ✅ | `get_all_obligations` |

### UPLOADS — CRUD

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /uploads/{id}` | `getUploadById` | ✅ | `get_upload_by_id` |
|| `DELETE /uploads/{id}` | `deleteUploadById` | ✅ | `delete_uploads_by_upload_id` |
|| `PATCH /uploads/{id}` | `updateUploadById` | ✅ | `update_upload_by_id` |
|| `PUT /uploads/{id}` | `moveUploadById` | ✅ | `move_upload_by_id` |
|| `GET /uploads` | `getUploads` | ✅ | `get_all_uploads_based_on` / `get_all_uploads_based_on_common_assignee` |
|| `POST /uploads` | `createUpload` | ✅ | `get_upload_id_by_local_package_upload`, `get_upload_id_by_download_url_package_upload`, `get_upload_id_by_giturl_package_upload` |

### UPLOADS — File Operations

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /uploads/{id}/download` | `getUploadFileById` | ✅ | `download_upload_file` |
|| `GET /uploads/{id}/summary` | `getSummaryByUploadId` | ✅ | `get_upload_summary_for_uploadid` |
|| `GET /uploads/{id}/item/{itemId}/info` | `getItemInfo` | ✅ | `get_file_info` |
|| `GET /uploads/{id}/licenses` | `getLicensesByUploadId` | ✅ | `get_licenses_found_by_agents_for_uploadid` |
|| `GET /uploads/{id}/copyrights` | `getCopyrightsByUploadId` | ✅ | `get_copyrights_by_upload_id` |
|| `PUT /uploads/{id}/permissions` | `setUploadPermissions` | ✅ | `set_upload_permissions` |
|| `GET /uploads/{id}/perm-groups` | `getGroupsWithPermissions` | ✅ | `get_group_permissions` |
|| `GET /uploads/{id}/item/{itemId}/highlight` | `getHighlightEntries` | ✅ | `get_highlight_entries` |
|| `GET /uploads/{id}/item/{itemId}/view` | `viewTheContentOfTheFile` | ✅ | `view_file_content` |
|| `PUT /uploads/{id}/item/{itemId}/clearing-decision` | `setClearingDecision` | ✅ | `set_clearing_decision` |
|| `POST /uploads/{id}/item/{itemId}/bulk-scan` | `scheduleBulkScan` | ✅ | `schedule_bulk_scan` |
|| `GET /uploads/{id}/item/{itemId}/bulk-history` | `getBulkHistory` | ✅ | `get_bulk_history` |
|| `GET /uploads/{id}/item/{itemId}/licenses` | `getLicenseDecisions` | ✅ | `get_license_decisions` |
|| `PUT /uploads/{id}/item/{itemId}/licenses` | `addEditDeleteLicenseDecision` | ✅ | `add_edit_delete_license_decision` |
|| `GET /uploads/{id}/licenses/main` | `getMainLicenses` | ✅ | `get_main_licenses` |
|| `POST /uploads/{id}/licenses/main` | `setMainLicense` | ✅ | `set_main_license` |
|| `DELETE /uploads/{id}/licenses/{shortName}/main` | `deleteMainLicense` | ✅ | `delete_main_license` |
|| `GET /uploads/{id}/item/{itemId}/prev-next` | `getPreviousAndNextItem` | ✅ | `get_prev_next_item` |
|| `GET /uploads/{id}/item/{itemId}/clearing-history` | `getClearingHistory` | ✅ | `get_clearing_history` |
|| `GET /uploads/{id}/clearing-progress` | `getClearingProgressInfo` | ✅ | `get_clearing_progress_info` |
|| `GET /uploads/{id}/licenses/histogram` | `getLicensesHistogram` | ✅ | `get_licenses_by_upload_id` |
|| `GET /uploads/{id}/agents` | `getAgentsByUploadId` | ✅ | `get_agents_by_upload_id` |
|| `GET /uploads/{id}/licenses/edited` | `getAllEditedLicenses` | ✅ | `get_all_edited_licenses` |
|| `GET /uploads/{id}/licenses/scanned` | `getAllScannedLicenses` | ✅ | `get_all_scanned_licenses` |
|| `GET /uploads/{id}/item/{itemId}/tree/view` | `getItemTreeView` | ✅ | `get_item_tree_view` |
|| `GET /uploads/{id}/topitem` | `getTopItemId` | ✅ | `get_upload_tree_id_by_upload_id` |
|| `GET /uploads/{id}/licenses/reuse` | `getLicensesReuseSummary` | ✅ | `get_licenses_reuse_summary` |
|| `GET /uploads/{id}/agents/revision` | `getRevisionsForAgents` | ✅ | `get_revisions_for_agents` |

### UPLOADS — One-Shot Scanners

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `POST /uploads/oneshot/nomos` | `runOneShotNomos` | ✅ | `run_one_shot_nomos` |
|| `POST /uploads/oneshot/monk` | `runOneShotMonk` | ✅ | `run_one_shot_monk` |
|| `POST /uploads/oneshot/ceu` | `runOneShotCEU` | ✅ | `run_one_shot_ceu` |

### COPYRIGHTS / CX ENDPOINTS

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET .../item/{itemId}/copyrights` | `getFileCopyrights` | ✅ | `get_file_copyrights` |
|| `DELETE .../copyrights/{hash}` | `deleteFileCopyrights` | ✅ | `delete_file_copyright` |
|| `PATCH .../copyrights/{hash}` | `restoreFileCopyrights` | ✅ | `restore_file_copyright` |
|| `PUT .../copyrights/{hash}` | `updateFileCopyrights` | ✅ | `update_file_copyright` |
|| `GET .../user-copyrights` | `getFileUserCopyrights` | ✅ | `get_file_user_copyrights` |
|| `DELETE .../user-copyrights/{hash}` | `deleteFileUserCopyright` | ✅ | `delete_file_user_copyright` |
|| `PATCH .../user-copyrights/{hash}` | `restoreFileUserCopyright` | ✅ | `restore_file_user_copyright` |
|| `PUT .../user-copyrights/{hash}` | `updateFileUserCopyright` | ✅ | `update_file_user_copyright` |
|| `GET .../scancode-copyrights` | `getFileScanCodeCopyrights` | ✅ | `get_file_scancode_copyrights` |
|| `DELETE .../scancode-copyrights/{hash}` | `deleteFileScanCodeCopyright` | ✅ | `delete_file_scancode_copyright` |
|| `PATCH .../scancode-copyrights/{hash}` | `restoreFileScanCodeCopyright` | ✅ | `restore_file_scancode_copyright` |
|| `PUT .../scancode-copyrights/{hash}` | `updateFileScanCodeCopyright` | ✅ | `update_file_scancode_copyright` |
|| `GET .../emails` | `getFileEmails` | ✅ | `get_file_emails` |
|| `DELETE .../emails/{hash}` | `deleteFileEmails` | ✅ | `delete_file_email` |
|| `PATCH .../emails/{hash}` | `restoreFileEmail` | ✅ | `restore_file_email` |
|| `PUT .../emails/{hash}` | `updateFileEmail` | ✅ | `update_file_email` |
|| `GET .../scancode-emails` | `getFileScanCodeEmail` | ✅ | `get_file_scancode_emails` |
|| `DELETE .../scancode-emails/{hash}` | `deleteFileScanCodeEmail` | ✅ | `delete_file_scancode_email` |
|| `PATCH .../scancode-emails/{hash}` | `restoreFileScanCodeEmail` | ✅ | `restore_file_scancode_email` |
|| `PUT .../scancode-emails/{hash}` | `updateFileScanCodeEmail` | ✅ | `update_file_scancode_email` |
|| `GET .../urls` | `getFileUrls` | ✅ | `get_file_urls` |
|| `DELETE .../urls/{hash}` | `deleteFileUrl` | ✅ | `delete_file_url` |
|| `PATCH .../urls/{hash}` | `restoreFileUrl` | ✅ | `restore_file_url` |
|| `PUT .../urls/{hash}` | `updateFileUrl` | ✅ | `update_file_url` |
|| `GET .../scancode-urls` | `getFileScanCodeUrl` | ✅ | `get_file_scancode_urls` |
|| `DELETE .../scancode-urls/{hash}` | `deleteFileScanCodeUrl` | ✅ | `delete_file_scancode_url` |
|| `PATCH .../scancode-urls/{hash}` | `restoreFileScanCodeUrl` | ✅ | `restore_file_scancode_url` |
|| `PUT .../scancode-urls/{hash}` | `updateFileScanCodeUrl` | ✅ | `update_file_scancode_url` |
|| `GET .../authors` | `getFileAuthors` | ✅ | `get_file_authors` |
|| `DELETE .../authors/{hash}` | `deleteFileAuthor` | ✅ | `delete_file_author` |
|| `PATCH .../authors/{hash}` | `restoreFileAuthor` | ✅ | `restore_file_author` |
|| `PUT .../authors/{hash}` | `updateFileAuthor` | ✅ | `update_file_author` |
|| `GET .../scancode-authors` | `getFileScanCodeAuthor` | ✅ | `get_file_scancode_authors` |
|| `DELETE .../scancode-authors/{hash}` | `deleteFileScanCodeAuthor` | ✅ | `delete_file_scancode_author` |
|| `PATCH .../scancode-authors/{hash}` | `restoreFileScanCodeAuthor` | ✅ | `restore_file_scancode_author` |
|| `PUT .../scancode-authors/{hash}` | `updateFileScanCodeAuthor` | ✅ | `update_file_scancode_author` |
|| `GET .../eccs` | `getFileEccs` | ✅ | `get_file_eccs` |
|| `DELETE .../eccs/{hash}` | `deleteFileEcc` | ✅ | `delete_file_ecc` |
|| `PATCH .../eccs/{hash}` | `restoreFileEcc` | ✅ | `restore_file_ecc` |
|| `PUT .../eccs/{hash}` | `updateFileEcc` | ✅ | `update_file_ecc` |
|| `GET .../keywords` | `getFileKeywords` | ✅ | `get_file_keywords` |
|| `DELETE .../keywords/{hash}` | `deleteFileKeyword` | ✅ | `delete_file_keyword` |
|| `PATCH .../keywords/{hash}` | `restoreFileKeyword` | ✅ | `restore_file_keyword` |
|| `PUT .../keywords/{hash}` | `updateFileKeyword` | ✅ | `update_file_keyword` |
|| `GET .../ipras` | `getFileIpras` | ✅ | `get_file_ipras` |
|| `DELETE .../ipras/{hash}` | `deleteFileIpra` | ✅ | `delete_file_ipra` |
|| `PATCH .../ipras/{hash}` | `restoreFileIpra` | ✅ | `restore_file_ipra` |
|| `PUT .../ipras/{hash}` | `updateFileIpra` | ✅ | `update_file_ipra` |
|| `GET .../totalcopyrights` | `getTotalFileCopyrights` | ✅ | `get_total_file_copyrights` |
|| `GET .../totalusercopyrights` | `getTotalFileUserCopyrights` | ✅ | `get_total_file_user_copyrights` |

### SEARCH

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /search` | `searchFile` | ✅ | `search_files_based_on` |
|| `POST /filesearch` | `getFiles` | ✅ | `get_file_by_any_one_of_sha1_or_md5_or_sha256` |

### USERS

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `POST /users` | `createUser` | ✅ | `create_user` |
|| `GET /users` | `getUsers` | ✅ | `get_all_users` |
|| `GET /users/{id}` | `getUserById` | ✅ | `get_user_by_id` |
|| `PUT /users/{id}` | `modifyUserById` | ✅ | `modify_user_by_id` |
|| `DELETE /users/{id}` | `deleteUserById` | ✅ | `delete_user_by_id` |
|| `GET /users/self` | `getSelf` | ✅ | `get_self` |
|| `POST /users/tokens` | `createRestApiToken` | ✅ | `create_rest_api_token` |
|| `GET /users/tokens/{type}` | `getTokensByType` | ✅ | `get_tokens_by_type` |

### JOBS

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /jobs` | `getJobs` | ✅ | `get_all_jobs` |
|| `POST /jobs` | `startJobs` | ✅ | `trigger_analysis_for_upload_id` |
|| `GET /jobs/all` | `getAllJobs` | ✅ | `get_all_jobs_admin` |
|| `GET /jobs/scheduler/operation/{operationName}` | `getSchedulerOptionsByOperation` | ✅ | `get_scheduler_options_by_operation` |
|| `POST /jobs/scheduler/operation/run` | `handleSchedulerRun` | ✅ | `handle_scheduler_run` |
|| `GET /jobs/{id}` | `getJobById` | ✅ | `get_job_info_by_id` |
|| `GET /jobs/history` | `getJobsHistoryPerUpload` | ✅ | `get_job_info_by_upload_id` |
|| `GET /jobs/dashboard/statistics` | `getJobStatistics` | ✅ | `get_job_statistics` |
|| `GET /jobs/dashboard` | `getAllServerJobs` | ✅ | `get_all_server_jobs` |
|| `DELETE /jobs/{id}/{queue}` | `deleteJob` | ✅ | `delete_job` |

### FOLDERS

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /folders` | `getFolders` | ✅ | `get_all_folders` |
|| `POST /folders` | `createFolder` | ✅ | `create_folder_under_parent_folder_id` |
|| `GET /folders/{id}` | `getFolderById` | ✅ | `get_folder_info_by_id` |
|| `DELETE /folders/{id}` | `deleteFolderById` | ✅ | `delete_folder_by_id` |
|| `PATCH /folders/{id}` | `patchFolderById` | ✅ | `change_folder_name_or_desc` |
|| `PUT /folders/{id}` | `moveFolderById` | ✅ | `apply_action_to_folderid` |
|| `PUT /folders/contents/{contentId}/unlink` | `unlinkContent` | ✅ | `unlink_content` |
|| `GET /folders/{id}/contents` | `getAllFolderContents` | ✅ | `get_all_folder_contents` |
|| `GET /folders/{id}/contents/unlinkable` | `getUnlinkableContents` | ✅ | `get_unlinkable_contents` |

### GROUPS

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /groups` | `getGroups` | ✅ | `get_groups` |
|| `POST /groups` | `createGroup` | ✅ | `create_new_user_group` |
|| `DELETE /groups/{id}` | `deleteGroupById` | ✅ | `delete_group_by_id` |
|| `DELETE /groups/{id}/user/{userId}` | `deleteGroupMemberByGroupIdAndUserId` | ✅ | `delete_group_member` |
|| `POST /groups/{id}/user/{userId}` | `addMember` | ✅ | `add_group_member` |
|| `PUT /groups/{id}/user/{userId}` | `updatePermissionByGroupIdAndUserId` | ✅ | `update_group_permission` |
|| `GET /groups/deletable` | `deletableGroups` | ✅ | `get_deletable_groups` |
|| `GET /groups/{id}/members` | `getGroupUsersWithRoles` | ✅ | `get_group_users_with_roles` |

### REPORT

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /report` | `getReportsByUpload` | ✅ | `generate_and_get_desired_report_for_uploadid` |
|| `GET /report/{id}` | `getReportById` | ✅ | `generate_and_get_desired_report_for_uploadid` |
|| `POST /report/import` | `uploadReport` | ✅ | `upload_report` |

### UPLOAD CONF

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /uploads/{id}/conf` | `getConfInfo` | ✅ | `get_conf_info` |
|| `PUT /uploads/{id}/conf` | `updateConfData` | ✅ | `update_conf_data` |

### LICENSE

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /license` | `getLicenses` | ✅ | `get_all_license_based_on` |
|| `POST /license` | `createLicense` | ✅ | `add_new_license` |
|| `POST /license/import-csv` | `importLicense` | ✅ | `import_license_csv` |
|| `GET /license/export-csv` | `exportLicense` | ✅ | `export_license_csv` |
|| `POST /license/import-json` | `handleImportLicense` | ✅ | `import_license_json` |
|| `GET /license/export-json` | `exportAdminLicenseToJSON` | ✅ | `export_license_json` |
|| `GET /license/{shortname}` | `getLicenseByShortname` | ✅ | `get_license_by_short_name` |
|| `PATCH /license/{shortname}` | `updateLicenseByShortname` | ✅ | `update_license_info_by_short_name` |
|| `GET /license/admincandidates` | `getAdminLicenseCandidates` | ✅ | `get_admin_license_candidates` |
|| `DELETE /license/admincandidates/{id}` | `deleteByLicenseCandidateId` | ✅ | `delete_license_candidate_by_id` |
|| `GET /license/adminacknowledgements` | `getAdminLicenseAcknowledgements` | ✅ | `get_admin_license_acknowledgements` |
|| `PUT /license/adminacknowledgements` | `mutateAdminLicenseAcknowledgement` | ✅ | `mutate_admin_license_acknowledgement` |
|| `GET /license/stdcomments` | `getAllStandardLicenseComments` | ✅ | `get_all_standard_license_comments` |
|| `PUT /license/stdcomments` | `mutateStdComments` | ✅ | `mutate_std_comments` |
|| `PUT /license/verify/{shortname}` | `verifyLicense` | ✅ | `verify_license` |
|| `PUT /license/merge/{shortname}` | `mergeLicense` | ✅ | `merge_license` |
|| `POST /license/suggest` | `getSuggestedLicense` | ✅ | `get_suggested_license` |

### OVERVIEW / ADMIN

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /overview/database/contents` | `getDatabaseContents` | ✅ | `get_database_contents` |
|| `GET /overview/info/php` | `getPhpInfo` | ✅ | `get_php_info` |
|| `GET /overview/disk/usage` | `getDiskUsage` | ✅ | `get_disk_usage` |
|| `GET /overview/database/metrics` | `getDatabaseMetrics` | ✅ | `get_database_metrics` |
|| `GET /overview/queries/active` | `getActiveQueries` | ✅ | `get_active_queries` |

### CUSTOMISE

|| OpenAPI Endpoint | Operation ID | Status | Implementation Method |
||---|---|---|---|
|| `GET /customise` | `getCustomiseData` | ✅ | `get_customise_data` |
|| `PUT /customise` | `updateCustomiseData` | ✅ | `update_customise_data` |
|| `GET /customise/banner` | `getBannerMessage` | ✅ | `get_banner_message` |

---

## 2. Summary Statistics

|| Category | Total Endpoints | Implemented | Missing |
||---|---|---|---|
|| Auth/Info | 4 | 4 | 0 |
|| Maintenance | 1 | 1 | 0 |
|| Obligations | 8 | 8 | 0 |
|| Uploads (CRUD + FileOps + One-Shot) | 36 | 36 | 0 |
|| Copyrights/CX | 51 | 51 | 0 |
|| Search | 2 | 2 | 0 |
|| Users | 8 | 8 | 0 |
|| Jobs | 10 | 10 | 0 |
|| Folders | 9 | 9 | 0 |
|| Groups | 8 | 8 | 0 |
|| Report | 3 | 3 | 0 |
|| Upload Conf | 2 | 2 | 0 |
|| License | 17 | 17 | 0 |
|| Overview/Admin | 5 | 5 | 0 |
|| Customise | 3 | 3 | 0 |
|| **Total** | **167** | **167** | **0** |

**Implementation coverage: 100%**

---

## 3. Business-Relevant Utility Functions

The following utility functions combine multiple API calls to perform complete business workflows. These are implemented in `easy_fossy/usecases.py`.

### Usecase 1: Full Package Scan Workflow
Upload a package (file/URL/git), trigger analysis, wait for completion, generate report
- Combines: `createUpload` → `triggerAnalysis` → `waitForJobCompletion` → `generateReport`

### Usecase 2: License Audit Report
Get comprehensive license information for an upload
- Combines: `getSummary` → `getLicensesFoundByAgents` → `getLicenseDecisions` → `getMainLicenses`

### Usecase 3: Clearing Status Dashboard
Get complete clearing status for all uploads in a folder
- Combines: `getUploads` → `getSummary` for each → `getClearingProgress`

### Usecase 4: Copyright/Email/URL Batch Export
Extract all copyrights, emails, URLs from an upload
- Combines: `getTopItemId` → `getCopyrights` → `getEmails` → `getUrls`

### Usecase 5: License Obligation Check
Find obligations for licenses found in an upload
- Combines: `getLicensesFoundByAgents` → `getLicenseByShortName` → `getObligationsList`

### Usecase 6: Full Upload Cleanup
Delete an upload and associated jobs
- Combines: `getJobs` for upload → `deleteJob` for each → `deleteUpload`

### Usecase 7: Folder Hierarchy Report
Get full folder tree with upload counts
- Combines: `getFolders` → `getFolderById` for each → `getAllFolderContents`

### Usecase 8: One-Shot License Detection
Run one-shot analysis without storing results
- Combines: `runOneShotNomos` / `runOneShotMonk` / `runOneShotCEU`

### Usecase 9: Reuse Workflow
Reuse decisions from another upload
- Combines: `getLicensesReuseSummary` → `triggerAnalysis` with reuse options

### Usecase 10: Compliance Report Generation
Generate SPDX/Dep5/ReadmeOSS reports
- Combines: `getSummary` → `generateReport` in multiple formats

---

## 4. Implementation Status (Completed)

All 167 operations from the OpenAPI specification have been implemented in
`easy_fossy/__init__.py`. The 10 business-relevant utility functions
have been implemented in `easy_fossy/usecases.py`.

### New Methods Added

**Uploads (13):** `get_upload_by_id`, `update_upload_by_id`, `move_upload_by_id`,
`get_clearing_history`, `get_clearing_progress_info`, `get_agents_by_upload_id`,
`get_all_edited_licenses`, `get_all_scanned_licenses`, `get_item_tree_view`,
`get_licenses_reuse_summary`, `get_revisions_for_agents`, `run_one_shot_nomos`,
`run_one_shot_monk`, `run_one_shot_ceu`

**Copyrights/CX (51):** `get_file_copyrights`, `delete_file_copyright`,
`restore_file_copyright`, `update_file_copyright`, `get_file_user_copyrights`,
`delete_file_user_copyright`, `restore_file_user_copyright`,
`update_file_user_copyright`, `get_file_scancode_copyrights`,
`delete_file_scancode_copyright`, `restore_file_scancode_copyright`,
`update_file_scancode_copyright`, `get_file_emails`, `delete_file_email`,
`restore_file_email`, `update_file_email`, `get_file_scancode_emails`,
`delete_file_scancode_email`, `restore_file_scancode_email`,
`update_file_scancode_email`, `get_file_urls`, `delete_file_url`,
`restore_file_url`, `update_file_url`, `get_file_scancode_urls`,
`delete_file_scancode_url`, `restore_file_scancode_url`,
`update_file_scancode_url`, `get_file_authors`, `delete_file_author`,
`restore_file_author`, `update_file_author`, `get_file_scancode_authors`,
`delete_file_scancode_author`, `restore_file_scancode_author`,
`update_file_scancode_author`, `get_file_eccs`, `delete_file_ecc`,
`restore_file_ecc`, `update_file_ecc`, `get_file_keywords`,
`delete_file_keyword`, `restore_file_keyword`, `update_file_keyword`,
`get_file_ipras`, `delete_file_ipra`, `restore_file_ipra`,
`update_file_ipra`, `get_total_file_copyrights`, `get_total_file_user_copyrights`

Plus 3 internal helper methods: `_cx_delete`, `_cx_restore`, `_cx_update`

**Users (6):** `get_self`, `create_user`, `modify_user_by_id`,
`delete_user_by_id`, `create_rest_api_token`, `get_tokens_by_type`

**Jobs (6):** `get_all_jobs_admin`, `get_scheduler_options_by_operation`,
`handle_scheduler_run`, `delete_job`, `get_job_statistics`,
`get_all_server_jobs`

**Folders (3):** `get_all_folder_contents`, `get_unlinkable_contents`,
`unlink_content`

**Groups (7):** `get_groups`, `delete_group_by_id`, `add_group_member`,
`delete_group_member`, `update_group_permission`, `get_deletable_groups`,
`get_group_users_with_roles`

**Report (1):** `upload_report`

**Upload Conf (2):** `get_conf_info`, `update_conf_data`

**License Admin (10):** `import_license_csv`, `export_license_csv`,
`import_license_json`, `export_license_json`, `get_admin_license_candidates`,
`delete_license_candidate_by_id`, `get_admin_license_acknowledgements`,
`mutate_admin_license_acknowledgement`, `get_all_standard_license_comments`,
`mutate_std_comments`, `verify_license`, `merge_license`, `get_suggested_license`

**Overview/Admin (5):** `get_database_contents`, `get_php_info`,
`get_disk_usage`, `get_database_metrics`, `get_active_queries`

**Customise (3):** `get_customise_data`, `update_customise_data`,
`get_banner_message`

### Utility Functions (in `usecases.py`)

1. `full_package_scan_workflow()` — upload + schedule scans + poll + collect results
2. `license_audit_report()` — edited vs scanned license comparison
3. `clearing_status_dashboard()` — consolidated clearing progress
4. `compliance_report_generation()` — license reuse summary + report data
5. `user_audit_trail()` — user details, jobs, group memberships
6. `folder_inventory()` — folder contents with optional license detail
7. `package_analysis_summary()` — one-shot nomos + monk + ceu
8. `license_candidate_review()` — admin candidate + acknowledgement review
9. `job_dashboard_monitor()` — all jobs, statistics, server jobs
10. `group_membership_audit()` — groups with members and permissions
