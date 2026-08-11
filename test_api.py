from easy_fossy import easy_fossy

def test_api():
    try:
        # Use the config we created
        f = easy_fossy("test/config.ini", "test")
        
        print("Connecting to server at:", f.url)
        
        print("\nAttempting to fetch basic server info...")
        # The client now uses resource objects. 
        # Folders are under f.folders
        folders = f.folders.get_all()
        
        if folders is not None:
            print(f"SUCCESS: Retrieved {len(folders)} folders.")
            for folder in folders[:3]: # Print first 3
                print(f" - {folder}")
        else:
            print("FAILURE: Could not retrieve folders.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_api()
