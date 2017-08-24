import datetime

from flask import jsonify

from flask_jwt_simple.config import config


def default_jwt_data_callback(identity):
    now = datetime.datetime.utcnow()
    identity_claim = config.identity_claim
    return {
        'exp': now + config.jwt_expires,
        'iat': now,
        'nbf': now,
        identity_claim: identity
    }


def default_expired_token_callback():
    """
    By default, if an expired token attempts to access a protected endpoint,
    we return a generic error message with a 401 status
    """
    return jsonify({'msg': 'Token has expired'}), 401


def default_invalid_token_callback(error_string):
    """
    By default, if an invalid token attempts to access a protected endpoint, we
    return the error string for why it is not valid with a 422 status code

    :param error_string: String indicating why the token is invalid
    """
    return jsonify({'msg': error_string}), 422


def default_unauthorized_callback(error_string):
    """
    By default, if a protected endpoint is accessed without a JWT, we return
    the error string indicating why this is unauthorized, with a 401 status code

    :param error_string: String indicating why this request is unauthorized
    """
    return jsonify({'msg': error_string}), 401
