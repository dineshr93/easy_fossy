class FossyError(Exception):
    """Base exception for easy_fossy library"""
    pass

class FossyAPIError(FossyError):
    """Raised when the API returns a non-success status code"""
    def __init__(self, message, status_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

class FossyAuthError(FossyAPIError):
    """Raised when authentication fails (401/403)"""
    pass

class FossyConnectionError(FossyError):
    """Raised when there is a network connectivity issue"""
    pass
