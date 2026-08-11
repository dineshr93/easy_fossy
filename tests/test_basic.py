import pytest
from easy_fossy import easy_fossy

def test_client_initialization():
    # This test checks if the client can be initialized without crashing
    # assuming a dummy config exists or is mocked.
    # Since we don't have a real config.ini here, we just test the import and call.
    try:
        client = easy_fossy("non_existent.ini")
    except FileNotFoundError:
        assert True
    except Exception as e:
        pytest.fail(f"Client initialization failed with unexpected error: {e}")
