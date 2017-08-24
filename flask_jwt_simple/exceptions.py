class FlaskJWTException(Exception):
    """
    Base except which all flask_jwt_simple errors extend
    """
    pass


class InvalidHeaderError(FlaskJWTException):
    """
    An error raised when the expected header format does not match what was received
    """
    pass


class NoAuthorizationError(FlaskJWTException):
    """
    An error raised when no JWT was found when a protected endpoint was accessed
    """
    pass
