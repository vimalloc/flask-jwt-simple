import datetime
import pytest
from flask import Flask

from flask_jwt_simple import JWTManager
from flask_jwt_simple.config import config


@pytest.fixture(scope='function')
def app():
    app = Flask(__name__)
    JWTManager(app)
    return app


# noinspection PyStatementEffect
def test_default_configs(app):
    with app.test_request_context():
        assert config.is_asymmetric is False
        assert config.header_name == 'Authorization'
        assert config.header_type == 'Bearer'
        assert config.jwt_expires == datetime.timedelta(hours=1)
        assert config.algorithm == 'HS256'
        assert config.identity_claim == 'sub'
        assert config.audience is None
        with pytest.raises(RuntimeError):
            config.encode_key
        with pytest.raises(RuntimeError):
            config.decode_key


def test_default_with_symetric_secret_key(app):
    app.config['JWT_SECRET_KEY'] = 'foobarbaz'
    with app.test_request_context():
        assert config.encode_key == 'foobarbaz'
        assert config.decode_key == 'foobarbaz'


def test_default_with_assymetric_secret_key(app):
    app.config['JWT_PUBLIC_KEY'] = 'foo'
    app.config['JWT_PRIVATE_KEY'] = 'bar'
    app.config['JWT_ALGORITHM'] = 'RS256'
    with app.test_request_context():
        assert config.decode_key == 'foo'
        assert config.encode_key == 'bar'


def test_config_overrides(app):
    with app.test_request_context():
        app.config['JWT_EXPIRES'] = datetime.timedelta(hours=2)
        assert config.jwt_expires == datetime.timedelta(hours=2)

        app.config['JWT_IDENTITY_CLAIM'] = 'identity'
        assert config.identity_claim == 'identity'

        app.config['JWT_HEADER_NAME'] = 'banana'
        assert config.header_name == 'banana'

        app.config['JWT_HEADER_TYPE'] = 'banana'
        assert config.header_type == 'banana'

        app.config['JWT_HEADER_TYPE'] = ''
        assert config.header_type == ''

        app.config['JWT_ALGORITHM'] = 'HS512'
        assert config.algorithm == 'HS512'
        assert config.is_asymmetric is False

        app.config['JWT_ALGORITHM'] = 'RS256'
        assert config.algorithm == 'RS256'
        assert config.is_asymmetric is True

        app.config['JWT_DECODE_AUDIENCE'] = 'foobar'
        assert config.audience == 'foobar'


# noinspection PyStatementEffect
def test_config_invalid_options(app):
    with app.test_request_context():
        app.config['JWT_SECRET_KEY'] = 'foobarbaz'
        app.config['JWT_ALGORITHM'] = 'RS256'
        with pytest.raises(RuntimeError):
            config.encode_key
        with pytest.raises(RuntimeError):
            config.decode_key

        app.config['JWT_SECRET_KEY'] = None
        app.config['JWT_PUBLIC_KEY'] = 'foo'
        app.config['JWT_PRIVATE_KEY'] = 'bar'
        app.config['JWT_ALGORITHM'] = 'HS256'
        with pytest.raises(RuntimeError):
            config.encode_key
        with pytest.raises(RuntimeError):
            config.decode_key

        app.config['JWT_HEADER_NAME'] = ''
        with pytest.raises(RuntimeError):
            config.header_name

        app.config['JWT_EXPIRES'] = 'banana'
        with pytest.raises(RuntimeError):
            config.jwt_expires
