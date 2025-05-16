from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import asyncio
import uvicorn
import json
from pathlib import Path
from contextlib import asynccontextmanager

from client_example import EasyFossyClient

# Global client
fossy_client = None

# Manage application lifespan and client connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: Connect to MCP server on startup
    global fossy_client
    fossy_client = EasyFossyClient()
    await fossy_client.connect()
    yield
    # Cleanup: Disconnect on shutdown
    await fossy_client.disconnect()

# Create FastAPI app
app = FastAPI(
    title="EasyFossy API",
    description="REST API for Fossology license scanning and management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to verify client is connected
def get_client():
    if not fossy_client or not fossy_client.connected:
        raise HTTPException(status_code=503, detail="MCP server not connected")
    return fossy_client

# Models
class InitializeRequest(BaseModel):
    config_file: str = Field(..., description="Path to config.ini file")
    server_to_use: str = Field(default="test", description="Server to use (test or prod)")
    verify: bool = Field(default=False, description="Whether to verify SSL certificates")

class UploadRequest(BaseModel):
    git_url: str = Field(..., description="URL of the Git repository")
    branch_name: str = Field(default="main", description="Branch to clone")
    folder_id: int = Field(..., description="ID of the destination folder")
    upload_name: str = Field(default="", description="Name for the upload (defaults to repository name)")
    upload_desc: str = Field(default="", description="Description for the upload")
    visibility: str = Field(default="public", description="Visibility setting (public, protected, private)")

class AnalysisRequest(BaseModel):
    upload_id: int = Field(..., description="ID of the upload to analyze")
    folder_id: int = Field(..., description="ID of the folder containing the upload")

class ReportRequest(BaseModel):
    upload_id: int = Field(..., description="ID of the upload to generate report for")
    report_format: str = Field(..., description="Format of the report (dep5, spdx2, spdx2tv, readmeoss, unifiedreport)")

class FolderRequest(BaseModel):
    parent_folder_id: int = Field(..., description="ID of the parent folder")
    folder_name: str = Field(..., description="Name for the new folder")

# Routes
@app.get("/")
async def root():
    return {"message": "EasyFossy API is running"}

@app.post("/initialize", response_model=Dict[str, Any])
async def initialize(request: InitializeRequest, client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.initialize_fossy(
            config_file=request.config_file,
            server=request.server_to_use,
            verify=request.verify
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/folders", response_model=List[Dict[str, Any]])
async def get_folders(client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.get_all_folders()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/folders", response_model=Dict[str, Any])
async def create_folder(request: FolderRequest, client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.session.invoke_tool(
            "create_folder", 
            {
                "parent_folder_id": request.parent_folder_id,
                "folder_name": request.folder_name
            }
        ).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/folders/{folder_id}", response_model=Dict[str, Any])
async def get_folder(folder_id: int, client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.session.invoke_tool(
            "get_folder_info_by_id", 
            {
                "folder_id": folder_id
            }
        ).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, client: EasyFossyClient = Depends(get_client)):
    try:
        await client.session.invoke_tool(
            "delete_folder", 
            {
                "folder_id": folder_id
            }
        )
        return {"status": "success", "message": f"Folder {folder_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/uploads/git", response_model=Dict[str, Any])
async def upload_git_package(request: UploadRequest, client: EasyFossyClient = Depends(get_client)):
    try:
        upload_id = await client.upload_git_package(
            git_url=request.git_url,
            branch_name=request.branch_name,
            folder_id=request.folder_id,
            upload_name=request.upload_name,
            upload_desc=request.upload_desc,
            visibility=request.visibility
        )
        return {"status": "success", "upload_id": upload_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/uploads/{upload_id}/analyze", response_model=Dict[str, Any])
async def analyze_upload(upload_id: int, folder_id: int, client: EasyFossyClient = Depends(get_client)):
    try:
        result = await client.trigger_analysis(
            upload_id=upload_id,
            folder_id=folder_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/uploads/{upload_id}", response_model=Dict[str, Any])
async def get_upload_summary(upload_id: int, client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.get_upload_summary(upload_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/uploads/{upload_id}/report", response_model=Dict[str, Any])
async def generate_upload_report(upload_id: int, report_format: str, client: EasyFossyClient = Depends(get_client)):
    try:
        result = await client.generate_report(upload_id, report_format)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/uploads/{upload_id}/licenses", response_model=List[Dict[str, Any]])
async def get_upload_licenses(
    upload_id: int, 
    show_directories: bool = True,
    client: EasyFossyClient = Depends(get_client)
):
    try:
        return await client.get_licenses_found_by_agents(
            upload_id=upload_id,
            show_directories=show_directories
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/licenses", response_model=List[Dict[str, Any]])
async def get_licenses(
    active_only: bool = True,
    license_kind: str = "main",
    page: int = 1,
    limit: int = 100,
    client: EasyFossyClient = Depends(get_client)
):
    try:
        return await client.session.invoke_tool(
            "get_all_licenses",
            {
                "active_only": active_only,
                "license_kind": license_kind,
                "page": page,
                "limit": limit
            }
        ).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/licenses/{short_name}", response_model=Dict[str, Any])
async def get_license_by_shortname(short_name: str, client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.session.invoke_tool(
            "get_license_by_shortname",
            {
                "short_name": short_name
            }
        ).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", response_model=List[Dict[str, Any]])
async def get_users(client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.session.invoke_tool("get_all_users", {}).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user(user_id: int, client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.session.invoke_tool(
            "get_user_by_id",
            {
                "user_id": user_id
            }
        ).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs", response_model=List[Dict[str, Any]])
async def get_jobs(client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.session.invoke_tool("get_all_jobs", {}).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/{job_id}", response_model=Dict[str, Any])
async def get_job(job_id: int, client: EasyFossyClient = Depends(get_client)):
    try:
        return await client.session.invoke_tool(
            "get_job_info_by_id",
            {
                "job_id": job_id
            }
        ).result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Main function to start the API server
def main():
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main() 