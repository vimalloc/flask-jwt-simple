import datetime

import jwt

from flask_jwt_simple.config import config
from flask_jwt_simple.exceptions import NoAuthorizationError, InvalidHeaderError
from flask_jwt_simple.default_callbacks import (
    default_expired_token_callback, default_invalid_token_callback,
    default_unauthorized_callback, default_jwt_data_callback
)


class JWTManager(object):
    """
    This object is used to hold the JWT settings and callback functions.
    Instances :class:`JWTManager` are *not* bound to specific apps, so
    you can create one in the main body of your code and then bind it
    to your app in a factory function.
    """

    def __init__(self, app=None):
        """
        Create the JWTManager instance. You can either pass a flask application
        in directly here to register this extension with the flask app, or
        call init_app after creating this object

        :param app: A flask application
        """
        # Register the default error handler callback methods. These can be
        # overridden with the appropriate loader decorators.
        self._expired_token_callback = default_expired_token_callback
        self._invalid_token_callback = default_invalid_token_callback
        self._unauthorized_callback = default_unauthorized_callback
        self._get_jwt_data = default_jwt_data_callback

        # Register this extension with the flask app now (if it is provided)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Register this extension with the flask app

        :param app: A flask application
        """
        # Save this so we can use it later in the extension
        if not hasattr(app, 'extensions'):   # pragma: no cover
            app.extensions = {}
        app.extensions['flask-jwt-simple'] = self

        # Set all the default configurations for this extension
        self._set_default_configuration_options(app)
        self._set_error_handler_callbacks(app)

        # Set propagate exceptions, so all of our error handlers properly
        # work in production
        app.config['PROPAGATE_EXCEPTIONS'] = True

    def _set_error_handler_callbacks(self, app):
        """
        Sets the error handler callbacks used by this extension
        """
        @app.errorhandler(NoAuthorizationError)
        def handle_no_auth_error(e):
            return self._unauthorized_callback(str(e))

        @app.errorhandler(InvalidHeaderError)
        def handle_invalid_header_error(e):
            return self._invalid_token_callback(str(e))

        @app.errorhandler(jwt.ExpiredSignatureError)
        def handle_expired_error(e):
            return self._expired_token_callback()

        @app.errorhandler(jwt.InvalidTokenError)
        def handle_invalid_token_error(e):
            return self._invalid_token_callback(str(e))

    @staticmethod
    def _set_default_configuration_options(app):
        """
        Sets the default configuration options used by this extension
        """
        # Options for JWTs when the TOKEN_LOCATION is headers
        app.config.setdefault('JWT_HEADER_NAME', 'Authorization')
        app.config.setdefault('JWT_HEADER_TYPE', 'Bearer')

        # How long an a token created with 'create_jwt' will last before
        # it expires (when using the default jwt_data_callback function).
        app.config.setdefault('JWT_EXPIRES', datetime.timedelta(hours=1))

        # What algorithm to use to sign the token. See here for a list of options:
        # https://github.com/jpadilla/pyjwt/blob/master/jwt/api_jwt.py
        app.config.setdefault('JWT_ALGORITHM', 'HS256')

        # Key that acts as the identity for the JWT
        app.config.setdefault('JWT_IDENTITY_CLAIM', 'sub')

        # Expected value of the audience claim
        app.config.setdefault('JWT_DECODE_AUDIENCE', None)

        # Secret key to sign JWTs with. Only used if a symmetric algorithm is
        # used (such as the HS* algorithms).
        app.config.setdefault('JWT_SECRET_KEY', None)

        # Keys to sign JWTs with when use when using an asymmetric
        # (public/private key) algorithms, such as RS* or EC*
        app.config.setdefault('JWT_PRIVATE_KEY', None)
        app.config.setdefault('JWT_PUBLIC_KEY', None)

    def expired_token_loader(self, callback):
        """
        Sets the callback method to be called if an expired JWT is received

        The default implementation will return json '{"msg": "Token has expired"}'
        with a 401 status code.

        Callback must be a function that takes zero arguments.
        """
        self._expired_token_callback = callback
        return callback

    def invalid_token_loader(self, callback):
        """
        Sets the callback method to be called if an invalid JWT is received.

        The default implementation will return json '{"msg": <err>}' with a 401
        status code.

        Callback must be a function that takes only one argument, which is the
        error message of why the token is invalid.
        """
        self._invalid_token_callback = callback
        return callback

    def unauthorized_loader(self, callback):
        """
        Sets the callback method to be called if no JWT is received

        The default implementation will return '{"msg": "Missing Authorization Header"}'
        json with a 401 status code.

        Callback must be a function that takes only one argument, which is the
        error message of why the token is invalid.
        """
        self._unauthorized_callback = callback
        return callback

    def jwt_data_loader(self, callback):
        """
        Sets the callback method to be called for what data should be included
        in a JWT (with the create_jwt() function).

        The default implementation will return the following data.

        .. code-block:: python

            {
                'exp': now + current_app.config['JWT_EXPIRES'],
                'iat': now,
                'nbf': now,
                'sub': identity
            }

        Callback must be a function that takes only one argument, which is the
        identity of the user this JWT is for.
        """
        self._get_jwt_data = callback
        return callback

    def _create_jwt(self, identity):
        jwt_data = self._get_jwt_data(identity)
        secret = config.encode_key
        algorithm = config.algorithm
        return jwt.encode(jwt_data, secret, algorithm).decode('utf-8')

