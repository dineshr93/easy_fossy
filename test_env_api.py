import os
from easy_fossy.client import FossyClient
from easy_fossy.config import FossyConfig

def test_env_config():
    print("--- Testing FossyClient.from_env() ---")
    
    # 1. Setup environment variables
    os.environ["FOSSY_URL"] = "http://0.0.0.0:8081/repo/api/v1/"
    os.environ["FOSSY_BEARER_TOKEN"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3ODg5OTgzOTksIm5iZiI6MTc4NjMyMDAwMCwianRpIjoiTWk0eiIsInNjb3BlIjoid3JpdGUifQ.F5izMcOo7otGKP8vrVbP0oL2VYm3rDZj2PsdImSjkMI"
    os.environ["FOSSY_TOKEN_EXPIRE"] = "2026-09-09"
    os.environ["FOSSY_ACCESS"] = "write"
    os.environ["FOSSY_VERIFY"] = "false"

    # Create a real dummy file because FossyClient.__init__ still checks for it
    with open("dummy.ini", "w") as f:
        f.write("[test]\nurl=http://localhost\n")

    try:
        # Use the new helper method
        client = FossyClient.from_env()
        
        print(f"Client initialized. URL: {client.url}")
        
        print("\nAttempting to fetch folder list...")
        folders = client.folders.get_all()
        
        if folders is not None:
            print(f"SUCCESS: Retrieved {len(folders)} folders using FossyClient.from_env().")
            for folder in folders[:3]:
                print(f" - {folder}")
        else:
            print("FAILURE: No folders retrieved.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if os.path.exists("dummy.ini"):
            os.remove("dummy.ini")

if __name__ == "__main__":
    test_env_config()
