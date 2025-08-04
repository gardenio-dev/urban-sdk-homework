class AppException(Exception):
    """Base class for all exceptions."""

    code: int = 500

    def __init__(self, message=None, code=None):
        self.message = message or self.__doc__
        self.code = code or self.code
        super().__init__(self.message)

    def __str__(self):
        return f"{self.code}: {self.message}"


class TenantException(AppException):
    """A tenant exception occurred."""

    code: int = 400


class TenantMismatchException(TenantException):
    """The tenant does not match."""
