from urban_sdk_homework.core.errors import AppException


class UnauthorizedException(AppException):
    """Unauthorized."""

    status_code: int = 401


class ForbiddenException(AppException):
    """Forbidden."""

    status_code: int = 403


class TokenException(AppException):
    """Token Exception."""

    status_code: int = 501
