from urban_sdk_homework.core.errors import AppException


class NotFoundException(AppException):
    """The requested resource was not found."""

    status_code = 404
