import jwt
from flask import current_app

try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack

from flask_jwt_simple.config import config


def _get_jwt_manager():
    try:
        return current_app.extensions['flask-jwt-simple']
    except KeyError:  # pragma: no cover
        raise RuntimeError("You must initialize a JWTManager with this flask "
                           "application before using this method")


def get_jwt():
    """
    Returns the python dictionary which has all of the data in this JWT. If no
    JWT is currently present, and empty dict is returned
    """
    return getattr(ctx_stack.top, 'jwt', {})


def get_jwt_identity():
    """
    Returns the identity of the JWT in this context. If no JWT is present,
    None is returned.
    """
    return get_jwt().get(config.identity_claim, None)


def decode_jwt(encoded_token):
    """
    Returns the decoded token from an encoded one. This does all the checks
    to insure that the decoded token is valid before returning it.
    """
    secret = config.decode_key
    algorithm = config.algorithm
    audience = config.audience
    return jwt.decode(encoded_token, secret, algorithms=[algorithm], audience=audience)


def create_jwt(identity):
    """
    Creates a new JWT.

    :param identity: The identity of this token. This can be anything that is
                     json serializable.
    :return: A utf-8 encoded jwt.
    """
    jwt_manager = _get_jwt_manager()
    return jwt_manager._create_jwt(identity)
