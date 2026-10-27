class ServiceError(Exception):
    """Base class for errors raised below the route layer"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(ServiceError):
    """The request data is not valid"""


class NotFoundError(ServiceError):
    """The requested record does not exist"""


class PersistenceError(ServiceError):
    """The database rejected a change"""
