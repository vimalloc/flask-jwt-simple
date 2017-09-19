import datetime

from flask import current_app

# Older versions of pyjwt do not have the requires_cryptography set. Also,
# older versions will not be adding new algorithms to them, so I can hard code
# the default version here and be safe. If there is a newer algorithm someone
# wants to use, they will need newer versions of pyjwt and it will be included
# in their requires_cryptography set, and if they attempt to use it in older
# versions of pyjwt, it will kick it out as an unrecognized algorithm.
try:
    from jwt.algorithms import requires_cryptography
except ImportError:  # pragma: no cover
    requires_cryptography = {'RS256', 'RS384', 'RS512', 'ES256', 'ES384',
                             'ES521', 'ES512', 'PS256', 'PS384', 'PS512'}


class _Config(object):
    """
    Helper object for accessing and verifying options in this extension. This
    is meant for internal use of the application; modifying config options
    should be done with flasks ```app.config```.

    Default values for the configuration options are set in the jwt_manager
    object. All of these values are read only.
    """

    @property
    def is_asymmetric(self):
        return self.algorithm in requires_cryptography

    @property
    def encode_key(self):
        return self._private_key if self.is_asymmetric else self._secret_key

    @property
    def decode_key(self):
        return self._public_key if self.is_asymmetric else self._secret_key

    @property
    def header_name(self):
        name = current_app.config['JWT_HEADER_NAME']
        if not name:
            raise RuntimeError("JWT_HEADER_NAME cannot be empty")
        return name

    @property
    def header_type(self):
        return current_app.config['JWT_HEADER_TYPE']

    @property
    def jwt_expires(self):
        delta = current_app.config['JWT_EXPIRES']
        if not isinstance(delta, datetime.timedelta):
            raise RuntimeError('JWT_EXPIRES must be a datetime.timedelta')
        return delta

    @property
    def algorithm(self):
        return current_app.config['JWT_ALGORITHM']

    @property
    def audience(self):
        return current_app.config['JWT_DECODE_AUDIENCE']

    @property
    def _secret_key(self):
        key = current_app.config['JWT_SECRET_KEY']
        if not key:
            raise RuntimeError('JWT_SECRET_KEY must be set to use '
                               'symmetric cryptography algorithm '
                               '"{}"'.format(self.algorithm))
        return key

    @property
    def _public_key(self):
        key = current_app.config['JWT_PUBLIC_KEY']
        if not key:
            raise RuntimeError('JWT_PUBLIC_KEY must be set to use '
                               'asymmetric cryptography algorithm '
                               '"{}"'.format(self.algorithm))
        return key

    @property
    def _private_key(self):
        key = current_app.config['JWT_PRIVATE_KEY']
        if not key:
            raise RuntimeError('JWT_PRIVATE_KEY must be set to use '
                               'asymmetric cryptography algorithm '
                               '"{}"'.format(self.algorithm))
        return key

    @property
    def identity_claim(self):
        return current_app.config['JWT_IDENTITY_CLAIM']

config = _Config()


