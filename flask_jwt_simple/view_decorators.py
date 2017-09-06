from functools import wraps

from flask import request
try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack

from flask_jwt_simple.utils import decode_jwt
from flask_jwt_simple.config import config
from flask_jwt_simple.exceptions import InvalidHeaderError, NoAuthorizationError


def jwt_required(fn):
    """
    If you decorate a view with this, it will ensure that the requester has a
    valid JWT before calling the actual view.

    :param fn: The view function to decorate
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        jwt_data = _decode_jwt_from_headers()
        ctx_stack.top.jwt = jwt_data
        return fn(*args, **kwargs)
    return wrapper


def jwt_optional(fn):
    """
    If you decorate a view with this, it will check the request for a valid
    JWT and put it into the Flask application context before calling the view.
    If no authorization header is present, the view will be called without the
    application context being changed. Other authentication errors are not
    affected. For example, if an expired JWT is passed in, it will still not
    be able to access an endpoint protected by this decorator.

    :param fn: The view function to decorate
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            jwt_data = _decode_jwt_from_headers()
            ctx_stack.top.jwt = jwt_data
        except (NoAuthorizationError, InvalidHeaderError):
            pass
        return fn(*args, **kwargs)
    return wrapper


def _decode_jwt_from_headers():
    header_name = config.header_name
    header_type = config.header_type

    # Verify we have the auth header
    jwt_header = request.headers.get(header_name, None)
    if not jwt_header:
        raise NoAuthorizationError("Missing {} Header".format(header_name))

    # Make sure the header is in a valid format that we are expecting, ie
    # <HeaderName>: <HeaderType(optional)> <JWT>
    parts = jwt_header.split()
    if not header_type:
        if len(parts) != 1:
            msg = "Bad {} header. Expected value '<JWT>'".format(header_name)
            raise InvalidHeaderError(msg)
        token = parts[0]
    else:
        if parts[0] != header_type or len(parts) != 2:
            msg = "Bad {} header. Expected value '{} <JWT>'".format(header_name, header_type)
            raise InvalidHeaderError(msg)
        token = parts[1]

    return decode_jwt(encoded_token=token)
