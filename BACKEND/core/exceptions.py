from fastapi import HTTPException


class AppException(Exception):
    """
    Base application exception
    """
    def __init__(self, message: str = "Application error", status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ValidationException(AppException):
    """
    Validation related errors
    """
    def __init__(self, message="Validation failed"):
        super().__init__(message, 422)


class NotFoundException(AppException):
    """
    Resource not found
    """
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class UnauthorizedException(AppException):
    """
    Unauthorized access
    """
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)


class ExternalServiceException(AppException):
    """
    External API / LLM errors
    """
    def __init__(self, message="External service failure"):
        super().__init__(message, 503)