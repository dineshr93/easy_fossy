# easy_fossy

[![Snake fonts](https://see.fontimg.com/api/renderfont4/mLZ3a/eyJyIjoiZnMiLCJoIjoxNzEsInciOjI2MjUsImZzIjo2NSwiZmdjIjoiIzAwMDAwMCIsImJnYyI6IiNGRkZGRkYiLCJ0IjoxfQ/ZWFzeV9mb3NzeQ/terasong.png)](https://www.fontspace.com/category/snake) For Font credit Refer <1>

Accessing fossy api is made easier (requires python 3.10)

[Production Index Registry](https://pypi.org/project/easy-fossy/)

[Test Index Registry](https://test.pypi.org/project/easy-fossy/)

```
pip install easy-fossy
```

Requires

```
#### 1. python 3.9
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

    from easy_fossy import easy_fossy as fossy


To set the location of config.ini file and get the instance to access all the methods use below code


    use_fossy_to=fossy('location/config.ini','test')


    use_fossy_to=fossy('location/config.ini','prod')


1. use_fossy_to.delete_uploads_by_upload_id(upload_id=7)

2. use_fossy_to.trigger_analysis_for_git_upload_package(
    git_url='https://github.com/dineshr93/pageres', branch_name='master', folder_id=1)
Avoids duplicate uploads

3. use_fossy_to.trigger_analysis_for_url_upload_package(
    file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip',
    file_name='pageres.zip', branch_name='', folder_id=1)
Avoids duplicate uploads

4. use_fossy_to.trigger_analysis_for_upload_package(
    file_path='uploads/commons-lang3-3.12.0-src.zip', folder_id=1)
Avoids duplicate uploads

5. use_fossy_to.trigger_analysis_for_upload_id(
    upload_id=4, folder_id=1)

6. use_fossy_to.get_upload_id_by_giturl_package_upload(git_url='https://github.com/dineshr93/pageres',
                                        branch_name='master', upload_name='',
                                       folder_id=1, upload_desc='', visibility=Public.public)

7. use_fossy_to.get_upload_id_by_download_url_package_upload(
    file_download_url='https://github.com/dineshr93/pageres/archive/refs/heads/master.zip',
    file_name='pageres', folder_id=1, upload_desc='commons-io-2.11.0', visibility=Public.public)


8. use_fossy_to.get_upload_id_by_local_package_upload(
    file_path='uploads/commons-io-2.11.0-src.zip', folder_id=1, upload_desc='commons-io-2.11.0',
    visibility=Public.public)

9. use_fossy_to.get_licenses_found_by_agents_for_uploadid
        (upload_id=2, show_directories=True, agents=[
                Agent.ninka.name, Agent.monk.name, Agent.nomos.name, Agent.ojo.name,
                Agent.reportImport.name,
                Agent.reso.name])


10. use_fossy_to.get_all_uploads_based_on(folder_id=1, is_recursive=True,
                         search_pattern_key='', upload_status=ClearingStatus.Open,
                         assignee='', since_yyyy_mm_dd='', page=1, limit=1000)


11. use_fossy_to.get_upload_summary_for_uploadid(upload_id=2)


12. use_fossy_to.apply_action_to_folderid(actions=Action.move, folder_id=6, parent_folder_id=2)

13. use_fossy_to.delete_folder_by_id(folder_id=3)

14. use_fossy_to.get_all_folders()


15. use_fossy_to.create_folder_under_parent_folder_id(
    parent_folder_id=1, folder_name='test')

16. use_fossy_to.change_folder_name_or_desc(folder_id=3, new_folder_name='', new_folder_desc='')

17. use_fossy_to.get_folder_info_by_id(folder_id=11)

18. use_fossy_to.get_all_folders()

19. use_fossy_to.generate_and_get_desired_report_for_uploadid(upload_id=3, report_format=ReportFormat.unifiedreport)

20. use_fossy_to.get_job_info_by_id(job_id=3)


21. use_fossy_to.get_job_info_by_upload_id(job_id=3)

22. use_fossy_to.get_all_jobs()

From 1.0.6
23. use_fossy_to.get_all_license_based_on(is_active='true', license_kind=Kind.main, page=1, limit=1)

24. sns = use_fossy_to.get_all_license_short_names_based_on(
        is_active='true', license_kind=Kind.main, contains_key='gp', page=1, limit=10000)
    for i, sn in enumerate(sns, start=1):
        print(f'{i}. {sn}')

From 1.0.9
25. use_fossy_to.get_license_by_short_name(short_name='AGPL-1.0')

26. use_fossy_to.add_new_license(unique_short_name='', new_full_name='', new_license_text='',
                new_url='', new_risk=2, isCandidate=True, merge_request=False)

27. use_fossy_to.update_license_info_by_short_name(short_name='', new_full_name='', new_license_text='', new_url='', new_risk=2)

28. use_fossy_to.search_files_based_on(self, filename_wildcard: str, searchType: SearchType, uploadId: int, tag: str, filesizemin_bytes: int, filesizemax_bytes: int, license: str, copyright: str) -> List[SearchResults] | Info:
--- give SearchType.Directory and filename_wildcard = 'draw%' (for draPaintIO.zip)

29 use_fossy_to.get_file_by_any_one_of_sha1_or_md5_or_sha256(self, sha1: str = '', md5: str = '', sha256: str = '') -> str | List[File]:
--- give only one hash of any of 3 format sha1 or sha256 or md5
--- returns list if even only data is there else it will return 'not found' string.

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

<1>
Font by Tehisa by Sealoung
https://www.fontspace.com/category/snake
License: Personal Use Free
