# easy_fossy
[![Snake fonts](https://see.fontimg.com/api/renderfont4/mLZ3a/eyJyIjoiZnMiLCJoIjoxNzEsInciOjI2MjUsImZzIjo2NSwiZmdjIjoiIzAwMDAwMCIsImJnYyI6IiNGRkZGRkYiLCJ0IjoxfQ/ZWFzeV9mb3NzeQ/terasong.png)](https://www.fontspace.com/category/snake)
accessing fossy api is made easier

[Production Index Registry](https://pypi.org/project/easy-fossy/)

[Test Index Registry](https://test.pypi.org/project/easy-fossy/)

```
pip install -i https://test.pypi.org/simple/ easy-fossy
```

Requires

```
#### 1. python 3.10
```

(uses latest structural matching case patterms)

```
#### 2. pip install easy-fossy  

```

```
#### 3. configure your server in config.ini
```

(config.ini file with below contents is essential & effortless kickstart)

```
[test]
url = http://fossology-test.com:port/repo/api/v1/
uname =
pwd =
access = write
bearer_token = Bearer OHNSUFaI6OtoFNz
token_valdity_days = 365
token_expire = 2022-10-29
reports_location = reports/
group_name = fossy

[prod]
url = http://fossology.com:port/repo/api/v1/
uname =
pwd =
access = write
bearer_token = Bearer OHNSUFaI6OtoFNz
token_valdity_days = 365
token_expire = 2022-10-29
reports_location = reports/
group_name = fossy
```

```
#### 4.  Kickstart straight away with example.py
```

[example.py](https://github.com/dineshr93/easy_fossy/blob/master/example.py)

```
Useful functions to import and try

from easy_fossy import *

1. delete_uploads_by_upload_id(upload_id=7, group_name=group_name)

2. trigger_analysis_for_git_upload_package(
    git_url='https://github.com/dineshr93/pageres', branch_name='master', folder_id=1, group_name='fossy')
Avoids duplicate uploads

3. trigger_analysis_for_url_upload_package(
    file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip', file_name='pageres.zip', branch_name='', folder_id=1, group_name='fossy')
Avoids duplicate uploads

4. trigger_analysis_for_upload_package(
    file_path='uploads/commons-lang3-3.12.0-src.zip', folder_id=1, group_name=group_name)
Avoids duplicate uploads

5. trigger_analysis_for_upload_id(
    upload_id=4, folder_id=1, group_name=group_name)

6. get_upload_id_by_giturl_package_upload(git_url='https://github.com/dineshr93/pageres', branch_name='master', upload_name='',
                                       folder_id=1, upload_desc='', visibility=Public.public, group_name='fossy')

7. get_upload_id_by_download_url_package_upload(
    file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip', file_name='pageres', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public, group_name='fossy')


8. get_upload_id_by_local_package_upload(
    file_path='uploads/commons-io-2.11.0-src.zip', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public,group_name=group_name)

9. get_licenses_found_by_agents_for_uploadid(upload_id=2, show_directories=True, group_name=group_name, agents=[
                                          Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name, Agent.reportImport.name, Agent.reso.name])


10. get_all_uploads_based_on(folder_id=1, is_recursive=True,
                         search_pattern_key='', upload_status=ClearingStatus.Open, assignee='', since_yyyy_mm_dd='', page=1, limit=1000,group_name=group_name)


11. get_upload_summary_for_uploadid(upload_id=2,group_name=group_name)


12. apply_action_to_folderid(actions=Action.move, folder_id=6, parent_folder_id=2,group_name=group_name)

13. delete_folder_by_id(folder_id=3,group_name=group_name)

14. get_all_folders()


15. create_folder_under_parent_folder_id(
    parent_folder_id=1, folder_name='test',group_name=group_name)

16. change_folder_name_or_desc(folder_id=3, new_folder_name='', new_folder_desc='',group_name=group_name)

17. get_folder_info_by_id(folder_id=11,group_name=group_name)

18. get_all_folders(group_name)

19. generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)

20. get_job_info_by_job_id(job_id=3,group_name=group_name)


21. get_job_info_by_job_id(job_id=3,group_name=group_name)

22. get_all_jobs(group_name)
```

### =====================================================================

### License: MIT

```
MIT License

Copyright (c) 2021 Dinesh Ravi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
