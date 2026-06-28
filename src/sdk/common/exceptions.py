class PlatformError(Exception):
    """
    Base exception for all domain and infrastructure errors across the platform.
    """
    def __init__(self, code: str, message: str, is_retryable: bool = False):
        self.code = code
        self.message = message
        self.is_retryable = is_retryable
        super().__init__(f"[{code}] {message}")

class ValidationException(PlatformError):
    def __init__(self, message: str):
        super().__init__("ERR_VALIDATION", message, is_retryable=False)

class AuthorizationException(PlatformError):
    def __init__(self, message: str):
        super().__init__("ERR_AUTH", message, is_retryable=False)

class ResourceNotFoundException(PlatformError):
    def __init__(self, message: str):
        super().__init__("ERR_NOT_FOUND", message, is_retryable=False)
