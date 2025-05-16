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


    use_fossy_to=fossy('location/config.ini','prod',verify=True)


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

30  get_all_users()

31  get_user_by_id(user_id=)
```
```
twine upload --repository pypi dist/* --config-file .pypirc
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

# EasyFossy with MCP

This project integrates [easy_fossy](https://github.com/dineshr93/easy_fossy) with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) to provide an API for accessing Fossology license scanning and management capabilities.

## Features

- Complete access to Fossology API via easy_fossy
- Model Context Protocol (MCP) integration for programmatic access
- FastAPI-based REST API
- Support for uploading and analyzing packages from various sources (local files, URLs, Git)
- License scanning and reporting
- Folder and upload management
- Search capabilities

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/easy_fossy_mcp.git
cd easy_fossy_mcp
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.ini` file with your Fossology server details:

```ini
[test]
url = http://fossology-test.com:port/repo/api/v1/
uname = your_username
pwd = your_password
access = write
bearer_token = Bearer your_token  # Will be populated automatically
token_valdity_days = 365
token_expire = 2023-10-29  # Will be updated automatically
reports_location = reports/
group_name = fossy

[prod]
url = http://fossology.com:port/repo/api/v1/
uname = your_username
pwd = your_password
access = write
bearer_token = Bearer your_token
token_valdity_days = 365
token_expire = 2023-10-29
reports_location = reports/
group_name = fossy
```

## Usage Options

This project provides three ways to interact with Fossology:

1. **MCP Server**: Direct integration with LLM applications
2. **Python Client**: Programmatic access via the MCP client
3. **REST API**: HTTP-based access via FastAPI

### Option 1: MCP Server

Running the MCP server directly:

```bash
python server.py
```

### Option 2: Python Client

The `client_example.py` file demonstrates how to connect to and use the EasyFossy MCP server:

```python
import asyncio
from client_example import EasyFossyClient

async def run_example():
    client = EasyFossyClient()
    try:
        # Connect to server
        await client.connect()
        
        # Initialize EasyFossy with config file
        result = await client.initialize_fossy("config.ini")
        print(f"Initialized EasyFossy: {result}")
        
        # Get all folders
        folders = await client.get_all_folders()
        print(f"Found {len(folders)} folders")
        
        # Upload a Git repository
        upload_id = await client.upload_git_package(
            git_url="https://github.com/example/repo",
            branch_name="main",
            folder_id=1
        )
        print(f"Uploaded package with ID: {upload_id}")
        
        # Trigger analysis
        analysis_result = await client.trigger_analysis(
            upload_id=int(upload_id),
            folder_id=1
        )
        print(f"Analysis triggered: {analysis_result}")
        
    finally:
        # Disconnect
        await client.disconnect()

asyncio.run(run_example())
```

### Option 3: REST API

The project also includes a FastAPI-based REST API that provides HTTP access to all the functionality:

```bash
# Start the API server
python api.py
```

This will start the API server at http://localhost:8000. You can access the interactive Swagger documentation at http://localhost:8000/docs.

#### API Endpoints

The API provides the following endpoints:

- **GET /** - Root endpoint, server status
- **POST /initialize** - Initialize Fossology connection
- **GET /folders** - Get all folders
- **POST /folders** - Create a new folder
- **GET /folders/{folder_id}** - Get folder information
- **DELETE /folders/{folder_id}** - Delete a folder
- **POST /uploads/git** - Upload a Git repository
- **POST /uploads/{upload_id}/analyze** - Analyze an upload
- **GET /uploads/{upload_id}** - Get upload summary
- **POST /uploads/{upload_id}/report** - Generate a report
- **GET /uploads/{upload_id}/licenses** - Get licenses in an upload
- **GET /licenses** - Get all licenses
- **GET /licenses/{short_name}** - Get license by short name
- **GET /users** - Get all users
- **GET /users/{user_id}** - Get user by ID
- **GET /jobs** - Get all jobs
- **GET /jobs/{job_id}** - Get job by ID

#### Example API Usage

```bash
# Initialize Fossology connection
curl -X POST "http://localhost:8000/initialize" \
  -H "Content-Type: application/json" \
  -d '{"config_file": "config.ini", "server_to_use": "test"}'

# Get all folders
curl -X GET "http://localhost:8000/folders"

# Upload a Git repository
curl -X POST "http://localhost:8000/uploads/git" \
  -H "Content-Type: application/json" \
  -d '{
    "git_url": "https://github.com/example/repo",
    "branch_name": "main",
    "folder_id": 1
  }'

# Analyze an upload
curl -X POST "http://localhost:8000/uploads/123/analyze?folder_id=1"

# Get licenses in an upload
curl -X GET "http://localhost:8000/uploads/123/licenses"
```

## Supported Functions

The MCP server provides the following tools:

### Initialization
- `initialize_fossy`: Initialize the easy_fossy instance with configuration

### User Management
- `get_all_users`: List all users
- `get_user_by_id`: Get user details by ID

### Job Management
- `get_all_jobs`: List all jobs
- `get_job_info_by_id`: Get job information by ID
- `get_job_info_by_upload_id`: Get job information by upload ID

### Folder Management
- `get_all_folders`: Get all folders
- `get_folder_info_by_id`: Get folder information by ID
- `create_folder`: Create a new folder
- `delete_folder`: Delete a folder
- `change_folder_name_or_desc`: Change folder name or description
- `apply_folder_action`: Apply an action (copy/move) to a folder

### Upload Management
- `get_all_uploads`: Get all uploads based on search criteria
- `get_upload_summary`: Get summary for an uploaded package
- `delete_upload`: Delete an upload

### Package Upload
- `upload_local_package`: Upload a local package file
- `upload_url_package`: Upload a package from URL
- `upload_git_package`: Upload a package from Git repository

### Analysis
- `trigger_analysis`: Trigger analysis for an uploaded package
- `trigger_analysis_for_package`: Trigger analysis for a local package file
- `trigger_analysis_for_url_package`: Trigger analysis for a package from URL
- `trigger_analysis_for_git_package`: Trigger analysis for a package from Git repository

### License Management
- `get_licenses_found_by_agents`: Get licenses found by scanners
- `get_license_by_shortname`: Get license details by short name
- `get_all_licenses`: Get all licenses
- `get_license_shortnames`: Get all license short names

### Report Generation
- `generate_report`: Generate and download a report for an upload

### Search
- `search_files`: Search files based on various criteria
- `get_file_by_hash`: Get file information by hash (SHA1, MD5, or SHA256)
- `get_copyrights_by_upload_id`: Get copyrights for an upload

## Integrating with LLM Applications

This MCP server can be integrated with LLM applications that support the Model Context Protocol. For example:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic

async def run_with_llm():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            
            # Get available tools
            response = await session.list_tools()
            tools = response.tools
            
            # Set up Anthropic Claude client
            client = Anthropic()
            
            # Make a query using Claude with tool access
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": "Upload the repository https://github.com/example/repo to Fossology folder ID 1, analyze it, and summarize the licenses found."
                    }
                ],
                tools=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    } for tool in tools
                ]
            )
            
            # Process Claude's response and handle tool calls
            # ...

# Run with asyncio.run(run_with_llm())
```

## License

Same as the original easy_fossy project.

## Credits

This project is based on [easy_fossy](https://github.com/dineshr93/easy_fossy) and uses the [Model Context Protocol](https://modelcontextprotocol.io/).
