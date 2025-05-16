import asyncio
from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack
import os
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class EasyFossyClient:
    """Client for the EasyFossy MCP server"""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.connected = False
    
    async def connect(self, server_path: str = "./server.py"):
        """Connect to the EasyFossy MCP server
        
        Args:
            server_path: Path to the server.py file
        """
        if not Path(server_path).exists():
            raise FileNotFoundError(f"Server script not found: {server_path}")
        
        # Start the server process
        server_params = StdioServerParameters(
            command="python",
            args=[server_path],
            env=os.environ.copy()
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        # Initialize the session
        await self.session.initialize()
        
        # Get available tools
        response = await self.session.list_tools()
        print(f"Connected to EasyFossy MCP server with {len(response.tools)} available tools")
        
        self.connected = True
        return True
    
    async def disconnect(self):
        """Disconnect from the server"""
        if self.connected:
            await self.exit_stack.aclose()
            self.connected = False
            print("Disconnected from EasyFossy MCP server")
    
    async def initialize_fossy(self, config_file: str, server: str = "test", verify: bool = False) -> Dict[str, Any]:
        """Initialize the EasyFossy instance
        
        Args:
            config_file: Path to the config.ini file
            server: Server to use (test or prod)
            verify: Whether to verify SSL certificates
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        response = await self.session.invoke_tool(
            "initialize_fossy", 
            {
                "config_file": config_file,
                "server_to_use": server,
                "verify": verify
            }
        )
        return response.result
    
    async def get_all_folders(self) -> List[Dict[str, Any]]:
        """Get all folders in the Fossology instance"""
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        response = await self.session.invoke_tool("get_all_folders", {})
        return response.result
    
    async def upload_git_package(
        self, 
        git_url: str, 
        branch_name: str, 
        folder_id: int,
        upload_name: str = "",
        upload_desc: str = "",
        visibility: str = "public"
    ) -> str:
        """Upload a package from a Git repository
        
        Args:
            git_url: URL of the Git repository
            branch_name: Branch to clone
            folder_id: ID of the destination folder
            upload_name: Name for the upload (defaults to repository name)
            upload_desc: Description for the upload
            visibility: Visibility setting (public, protected, private)
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        response = await self.session.invoke_tool(
            "upload_git_package", 
            {
                "git_url": git_url,
                "branch_name": branch_name,
                "folder_id": folder_id,
                "upload_name": upload_name,
                "upload_desc": upload_desc,
                "visibility": visibility
            }
        )
        return response.result
    
    async def trigger_analysis(self, upload_id: int, folder_id: int) -> Dict[str, Any]:
        """Trigger analysis for an uploaded package
        
        Args:
            upload_id: ID of the upload to analyze
            folder_id: ID of the folder containing the upload
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        response = await self.session.invoke_tool(
            "trigger_analysis", 
            {
                "upload_id": upload_id,
                "folder_id": folder_id
            }
        )
        return response.result
    
    async def get_upload_summary(self, upload_id: int) -> Dict[str, Any]:
        """Get summary for an uploaded package
        
        Args:
            upload_id: ID of the upload to get summary for
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        response = await self.session.invoke_tool(
            "get_upload_summary", 
            {
                "upload_id": upload_id
            }
        )
        return response.result
    
    async def generate_report(self, upload_id: int, report_format: str) -> Dict[str, Any]:
        """Generate a report for an uploaded package
        
        Args:
            upload_id: ID of the upload to generate report for
            report_format: Format of the report (dep5, spdx2, spdx2tv, readmeoss, unifiedreport)
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        response = await self.session.invoke_tool(
            "generate_report", 
            {
                "upload_id": upload_id,
                "report_format": report_format
            }
        )
        return response.result
    
    async def get_licenses_found_by_agents(
        self, 
        upload_id: int, 
        show_directories: bool = True, 
        agents: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Get licenses found by scanners for an upload
        
        Args:
            upload_id: ID of the upload to get licenses for
            show_directories: Whether to include directories
            agents: List of agents to include results from (empty for all)
        """
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        response = await self.session.invoke_tool(
            "get_licenses_found_by_agents", 
            {
                "upload_id": upload_id,
                "show_directories": show_directories,
                "agents": agents
            }
        )
        return response.result

async def main():
    # Create client
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
        
        # Example: Upload a Git repository
        # upload_id = await client.upload_git_package(
        #     git_url="https://github.com/example/repo",
        #     branch_name="main",
        #     folder_id=1
        # )
        # print(f"Uploaded package with ID: {upload_id}")
        
        # Example: Trigger analysis
        # analysis_result = await client.trigger_analysis(
        #     upload_id=int(upload_id),
        #     folder_id=1
        # )
        # print(f"Analysis triggered: {analysis_result}")
        
        # Example: Get upload summary
        # summary = await client.get_upload_summary(int(upload_id))
        # print(f"Upload summary: {json.dumps(summary, indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Disconnect
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 