#!/usr/bin/env python
"""
EasyFossy MCP Demo Script

This script demonstrates the three ways to use the EasyFossy MCP integration:
1. Direct MCP server usage
2. Python client
3. REST API via HTTP requests

Requirements:
- config.ini file with valid Fossology server credentials
- All dependencies installed
"""

import os
import sys
import json
import asyncio
import subprocess
import requests
import time
from pathlib import Path
import argparse
from contextlib import AsyncExitStack

# For MCP direct usage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# For Python client
from client_example import EasyFossyClient

def print_section(title):
    """Print a section header for better readability"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

async def demo_mcp_direct():
    """Demo direct usage of the MCP server"""
    print_section("DEMO 1: Direct MCP Server Usage")
    
    # Start MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=os.environ.copy()
    )
    
    async with AsyncExitStack() as stack:
        # Connect to server
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await stack.enter_async_context(ClientSession(stdio, write))
        
        # Initialize the session
        await session.initialize()
        
        # List available tools
        response = await session.list_tools()
        print(f"Connected to MCP server with {len(response.tools)} available tools:")
        for tool in response.tools[:5]:  # Just show first 5 tools
            print(f"- {tool.name}: {tool.description}")
        print(f"(... and {len(response.tools) - 5} more tools)")
        
        # Initialize fossy
        print("\nInitializing fossy with config.ini...")
        result = await session.invoke_tool(
            "initialize_fossy", 
            {
                "config_file": "config.ini",
                "server_to_use": "test",
                "verify": False
            }
        )
        print(f"Initialization result: {json.dumps(result.result, indent=2)}")
        
        # Get folders
        print("\nGetting folders...")
        folders_response = await session.invoke_tool("get_all_folders", {})
        folders = folders_response.result
        print(f"Found {len(folders)} folders")
        
        # We'll use just the first folder ID for the demo
        if folders:
            folder_id = folders[0]["id"]
            print(f"Using folder ID: {folder_id}")
            
            # Get licenses
            print("\nGetting licenses...")
            licenses_response = await session.invoke_tool(
                "get_all_licenses", 
                {
                    "active_only": True,
                    "license_kind": "main",
                    "page": 1,
                    "limit": 5
                }
            )
            licenses = licenses_response.result
            print(f"First 5 licenses:")
            for license in licenses:
                print(f"- {license.get('shortName', 'Unknown')}: {license.get('fullName', 'Unknown')}")

async def demo_python_client():
    """Demo using the Python client"""
    print_section("DEMO 2: Python Client Usage")
    
    client = EasyFossyClient()
    try:
        # Connect to server
        print("Connecting to MCP server...")
        await client.connect()
        
        # Initialize EasyFossy with config file
        print("\nInitializing fossy with config.ini...")
        result = await client.initialize_fossy("config.ini")
        print(f"Initialization result: {json.dumps(result, indent=2)}")
        
        # Get all folders
        print("\nGetting folders...")
        folders = await client.get_all_folders()
        print(f"Found {len(folders)} folders")
        
        # We'll use just the first folder ID for the demo
        if folders:
            folder_id = folders[0]["id"]
            print(f"Using folder ID: {folder_id}")
            
            # Get users
            print("\nGetting users...")
            users = await client.session.invoke_tool("get_all_users", {}).result
            print(f"Found {len(users)} users")
            if users:
                first_user = users[0]
                print(f"First user: {first_user.get('name', 'Unknown')} (ID: {first_user.get('id', 'Unknown')})")
    finally:
        # Disconnect
        await client.disconnect()

def demo_rest_api():
    """Demo using the REST API"""
    print_section("DEMO 3: REST API Usage")
    
    # Start the API server in a separate process
    api_process = subprocess.Popen(
        [sys.executable, "api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to start
    print("Starting API server...")
    time.sleep(5)
    
    try:
        # Check if server is running
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print(f"API server is running: {response.json()}")
            
            # Initialize fossy
            print("\nInitializing fossy with config.ini...")
            init_response = requests.post(
                "http://localhost:8000/initialize",
                json={"config_file": "config.ini", "server_to_use": "test"}
            )
            if init_response.status_code == 200:
                print(f"Initialization successful: {json.dumps(init_response.json(), indent=2)}")
                
                # Get folders
                print("\nGetting folders...")
                folders_response = requests.get("http://localhost:8000/folders")
                if folders_response.status_code == 200:
                    folders = folders_response.json()
                    print(f"Found {len(folders)} folders")
                    
                    # We'll use just the first folder ID for the demo
                    if folders:
                        folder_id = folders[0]["id"]
                        print(f"Using folder ID: {folder_id}")
                        
                        # Get jobs
                        print("\nGetting jobs...")
                        jobs_response = requests.get("http://localhost:8000/jobs")
                        if jobs_response.status_code == 200:
                            jobs = jobs_response.json()
                            print(f"Found {len(jobs)} jobs")
                            if jobs:
                                job = jobs[0]
                                print(f"First job: {job.get('name', 'Unknown')} (ID: {job.get('id', 'Unknown')})")
                                
                                # Get job details
                                job_id = job.get('id')
                                if job_id:
                                    print(f"\nGetting details for job {job_id}...")
                                    job_response = requests.get(f"http://localhost:8000/jobs/{job_id}")
                                    if job_response.status_code == 200:
                                        job_details = job_response.json()
                                        print(f"Job details: {json.dumps(job_details, indent=2)}")
                else:
                    print(f"Failed to get folders: {folders_response.status_code} - {folders_response.text}")
            else:
                print(f"Failed to initialize: {init_response.status_code} - {init_response.text}")
        else:
            print(f"API server is not responding: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the API server. Make sure it's running on port 8000.")
    finally:
        # Terminate the API server
        print("\nStopping API server...")
        api_process.terminate()
        api_process.wait()

async def main():
    # Create a parser for command-line arguments
    parser = argparse.ArgumentParser(description="EasyFossy MCP Demo")
    parser.add_argument("--demo", choices=["mcp", "client", "api", "all"], default="all",
                      help="Which demo to run (mcp, client, api, or all)")
    
    args = parser.parse_args()
    
    # Check if config.ini exists
    if not Path("config.ini").exists():
        print("Error: config.ini file not found. Please create one before running the demo.")
        return
    
    # Run the selected demo(s)
    if args.demo in ["mcp", "all"]:
        await demo_mcp_direct()
    
    if args.demo in ["client", "all"]:
        await demo_python_client()
    
    if args.demo in ["api", "all"]:
        demo_rest_api()
    
    print_section("DEMO COMPLETED")

if __name__ == "__main__":
    asyncio.run(main()) 