import json

import pytest
from flask import Flask, jsonify
from flask_jwt_simple import JWTManager


@pytest.fixture(scope='function')
def app():
    app = Flask(__name__)
    return app


def _parse_callback(result):
    response = result[0]
    status_code = result[1]
    data = json.loads(response.get_data(as_text=True))
    return status_code, data


def test_manual_init_app(app):
    jwt_manager = JWTManager()
    jwt_manager.init_app(app)
    assert jwt_manager == app.extensions['flask-jwt-simple']


def test_class_init_app(app):
    jwt_manager = JWTManager(app)
    assert jwt_manager == app.extensions['flask-jwt-simple']


def test_default_expired_token_callback(app):
    jwt_manager = JWTManager(app)

    with app.test_request_context():
        result = jwt_manager._expired_token_callback()
        status_code, data = _parse_callback(result)

        assert status_code == 401
        assert data == {'msg': 'Token has expired'}


def test_custom_expired_token_callback(app):
    jwt_manager = JWTManager(app)

    @jwt_manager.expired_token_loader
    def custom():
        return jsonify({"foo": "bar"}), 200

    with app.test_request_context():
        result = jwt_manager._expired_token_callback()
        status_code, data = _parse_callback(result)

        assert status_code == 200
        assert data == {'foo': 'bar'}


def test_default_invalid_token_callback(app):
    jwt_manager = JWTManager(app)

    with app.test_request_context():
        err = "Test error"
        result = jwt_manager._invalid_token_callback(err)
        status_code, data = _parse_callback(result)

        assert status_code == 422
        assert data == {'msg': err}


def test_custom_invalid_token_callback(app):
    jwt_manager = JWTManager(app)

    @jwt_manager.invalid_token_loader
    def custom(err):
        return jsonify({"foo": "bar"}), 200

    with app.test_request_context():
        err = "Test error"
        result = jwt_manager._invalid_token_callback(err)
        status_code, data = _parse_callback(result)

        assert status_code == 200
        assert data == {'foo': 'bar'}


def test_default_unauthorized_callback(app):
    jwt_manager = JWTManager(app)

    with app.test_request_context():
        err = "Test error"
        result = jwt_manager._unauthorized_callback(err)
        status_code, data = _parse_callback(result)

        assert status_code == 401
        assert data == {'msg': err}


def test_custom_unauthorized_callback(app):
    jwt_manager = JWTManager(app)

    @jwt_manager.unauthorized_loader
    def custom(err):
        return jsonify({"foo": "bar"}), 200

    with app.test_request_context():
        err = "Test error"
        result = jwt_manager._unauthorized_callback(err)
        status_code, data = _parse_callback(result)

        assert status_code == 200
        assert data == {'foo': 'bar'}


def test_default_get_jwt_data_callback(app):
    jwt_manager = JWTManager(app)

    with app.test_request_context():
        result = jwt_manager._get_jwt_data(identity='foo')
        assert 'exp' in result
        assert 'iat' in result
        assert 'nbf' in result
        assert result['sub'] == 'foo'


def test_custom_get_jwt_data_callback(app):
    jwt_manager = JWTManager(app)

    @jwt_manager.jwt_data_loader
    def custom(identity):
        return {"foo": "bar"}

    with app.test_request_context():
        result = jwt_manager._get_jwt_data(identity='foo')
        assert result == {"foo": "bar"}
