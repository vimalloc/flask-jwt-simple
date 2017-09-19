import pytest
import datetime
from flask import Flask, jsonify, json

from flask_jwt_simple.utils import get_jwt_identity, create_jwt
from flask_jwt_simple import JWTManager, jwt_required, jwt_optional


RSA_PRIVATE = """
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDN+p9a9oMyqRzkae8yLdJcEK0O0WesH6JiMz+KDrpUwAoAM/KP
DnxFnROJDSBHyHEmPVn5x8GqV5lQ9+6l97jdEEcPo6wkshycM82fgcxOmvtAy4Uo
xq/AeplYqplhcUTGVuo4ZldOLmN8ksGmzhWpsOdT0bkYipHCn5sWZxd21QIDAQAB
AoGBAMJ0++KVXXEDZMpjFDWsOq898xNNMHG3/8ZzmWXN161RC1/7qt/RjhLuYtX9
NV9vZRrzyrDcHAKj5pMhLgUzpColKzvdG2vKCldUs2b0c8HEGmjsmpmgoI1Tdf9D
G1QK+q9pKHlbj/MLr4vZPX6xEwAFeqRKlzL30JPD+O6mOXs1AkEA8UDzfadH1Y+H
bcNN2COvCqzqJMwLNRMXHDmUsjHfR2gtzk6D5dDyEaL+O4FLiQCaNXGWWoDTy/HJ
Clh1Z0+KYwJBANqRtJ+RvdgHMq0Yd45MMyy0ODGr1B3PoRbUK8EdXpyUNMi1g3iJ
tXMbLywNkTfcEXZTlbbkVYwrEl6P2N1r42cCQQDb9UQLBEFSTRJE2RRYQ/CL4yt3
cTGmqkkfyr/v19ii2jEpMBzBo8eQnPL+fdvIhWwT3gQfb+WqxD9v10bzcmnRAkEA
mzTgeHd7wg3KdJRtQYTmyhXn2Y3VAJ5SG+3qbCW466NqoCQVCeFwEh75rmSr/Giv
lcDhDZCzFuf3EWNAcmuMfQJARsWfM6q7v2p6vkYLLJ7+VvIwookkr6wymF5Zgb9d
E6oTM2EeUPSyyrj5IdsU2JCNBH1m3JnUflz8p8/NYCoOZg==
-----END RSA PRIVATE KEY-----
"""


RSA_PUBLIC = """
-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAM36n1r2gzKpHORp7zIt0lwQrQ7RZ6wfomIzP4oOulTACgAz8o8OfEWd
E4kNIEfIcSY9WfnHwapXmVD37qX3uN0QRw+jrCSyHJwzzZ+BzE6a+0DLhSjGr8B6
mViqmWFxRMZW6jhmV04uY3ySwabOFamw51PRuRiKkcKfmxZnF3bVAgMBAAE=
-----END RSA PUBLIC KEY-----
"""

# Slightly modifed version of above to test invalid jwts
BAD_RSA_PUBLIC = """
-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAM36n1r2gzKpHORp8zIt0lwQrQ7RZ6wfomIzP4oOulTACgAz8o8OfEWd
E4kNIEfIcSY9WfnHwapXmVD37qX3uN0QRw+jrCSyHJwzzZ+BzE6a+0DLhSjGr8B6
mViqmWFxRMZW6jhmV04uY3ySwabOFamw51PRuRiKkcKfmxZnF3bVAgMBAAE=
-----END RSA PUBLIC KEY-----
"""


def cartesian_product_configs():
    jwt_identity_claims = ['identity', 'sub']

    configs = []
    for identity in jwt_identity_claims:
        configs.append({
            'JWT_SECRET_KEY': 'testing_secret_key',
            'JWT_ALGORITHM': 'HS256',
            'JWT_IDENTITY_CLAIM': identity
        })
        configs.append({
            'JWT_PUBLIC_KEY': RSA_PUBLIC,
            'JWT_PRIVATE_KEY': RSA_PRIVATE,
            'JWT_ALGORITHM': 'RS256',
            'JWT_IDENTITY_CLAIM': identity
        })
    return configs


CONFIG_COMBINATIONS = cartesian_product_configs()


@pytest.fixture(scope='function', params=CONFIG_COMBINATIONS)
def app(request):
    app = Flask(__name__)

    for key, value in request.param.items():
        app.config[key] = value

    JWTManager(app)

    @app.route('/jwt', methods=['POST'])
    def create_token_endpoint():
        access_token = create_jwt('username')
        return jsonify(jwt=access_token)

    @app.route('/protected')
    @jwt_required
    def protected():
        return jsonify(foo='bar')

    @app.route('/optional')
    @jwt_optional
    def optional():
        if get_jwt_identity():
            return jsonify(foo='bar')
        else:
            return jsonify(foo='baz')

    return app


def _make_jwt_request(test_client, jwt, request_url):
    app = test_client.application
    header_name = app.config['JWT_HEADER_NAME']
    header_type = app.config['JWT_HEADER_TYPE']
    return test_client.get(
        request_url,
        content_type='application/json',
        headers={header_name: '{} {}'.format(header_type, jwt).strip()}
    )


def _get_jwt(test_client):
    response = test_client.post('/jwt')
    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert 'jwt' in json_data
    return json_data['jwt']


def test_protected_without_jwt(app):
    test_client = app.test_client()
    response = test_client.get('/protected')
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert json_data == {'msg': 'Missing Authorization Header'}


def test_protected_with_jwt(app):
    test_client = app.test_client()
    jwt = _get_jwt(test_client)
    response = _make_jwt_request(test_client, jwt, '/protected')
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_data == {'foo': 'bar'}


def test_optional_without_jwt(app):
    test_client = app.test_client()
    response = test_client.get('/optional')
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_data == {'foo': 'baz'}


def test_optional_with_jwt(app):
    test_client = app.test_client()
    jwt = _get_jwt(test_client)
    response = _make_jwt_request(test_client, jwt, '/optional')
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_data == {'foo': 'bar'}


@pytest.mark.parametrize("header_name", ['Authorization', 'Foo'])
@pytest.mark.parametrize("header_type", ['Bearer', 'JWT', ''])
def test_with_custom_headers(app, header_name, header_type):
    app.config['JWT_HEADER_NAME'] = header_name
    app.config['JWT_HEADER_TYPE'] = header_type

    test_client = app.test_client()
    jwt = _get_jwt(test_client)
    response = _make_jwt_request(test_client, jwt, '/protected')
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_data == {'foo': 'bar'}


@pytest.mark.parametrize("endpoint", [
    '/protected',
    '/optional',
])
@pytest.mark.parametrize("header_type", ['Foo', ''])
def test_with_bad_header(app, endpoint, header_type):
    app.config['JWT_HEADER_TYPE'] = header_type

    test_client = app.test_client()
    jwt = _get_jwt(test_client)

    headers = {'Authorization': 'Bearer {}'.format(jwt)}
    response = test_client.get(
        endpoint,
        content_type='application/json',
        headers=headers
    )
    json_data = json.loads(response.get_data(as_text=True))

    expected_results = (
        (422, {'msg': "Bad Authorization header. Expected value '<JWT>'"}),
        (422, {'msg': "Bad Authorization header. Expected value 'Foo <JWT>'"}),
        (200, {'foo': "baz"})  # Returns this if unauthorized in jwt_optional test endpoint
    )
    assert (response.status_code, json_data) in expected_results


@pytest.mark.parametrize("endpoint", [
    '/protected',
    '/optional',
])
def test_with_bad_token(app, endpoint):
    test_client = app.test_client()
    jwt = _get_jwt(test_client)

    # change teh secret key here to make the token we just got invalid
    app.config['JWT_SECRET_KEY'] = 'something_different'
    app.config['JWT_PUBLIC_KEY'] = BAD_RSA_PUBLIC

    response = _make_jwt_request(test_client, jwt, endpoint)
    json_data = json.loads(response.get_data(as_text=True))

    assert json_data == {'msg': 'Signature verification failed'}
    assert response.status_code == 422


@pytest.mark.parametrize("endpoint", [
    '/protected',
    '/optional',
])
def test_expired_token(app, endpoint):
    app.config['JWT_EXPIRES'] = datetime.timedelta(hours=-1)

    test_client = app.test_client()
    jwt = _get_jwt(test_client)
    response = _make_jwt_request(test_client, jwt, endpoint)
    json_data = json.loads(response.get_data(as_text=True))

    assert json_data == {'msg': 'Token has expired'}
    assert response.status_code == 401


@pytest.mark.parametrize("endpoint", [
    '/protected',
    '/optional',
])
def test_valid_aud(app, endpoint):
    app.config['JWT_DECODE_AUDIENCE'] = 'foo'
    jwt_manager = app.extensions['flask-jwt-simple']

    @jwt_manager.jwt_data_loader
    def change_claims(identity):
        now = datetime.datetime.utcnow()
        identity_claim = app.config['JWT_IDENTITY_CLAIM']
        return {
            'exp': now + app.config['JWT_EXPIRES'],
            'iat': now,
            'nbf': now,
            identity_claim: identity,
            'aud': 'foo'
        }

    test_client = app.test_client()
    jwt = _get_jwt(test_client)
    response = _make_jwt_request(test_client, jwt, endpoint)
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert json_data == {'foo': 'bar'}


@pytest.mark.parametrize("endpoint", [
    '/protected',
    '/optional',
])
def test_invalid_aud(app, endpoint):
    app.config['JWT_DECODE_AUDIENCE'] = 'bar'
    jwt_manager = app.extensions['flask-jwt-simple']

    @jwt_manager.jwt_data_loader
    def change_claims(identity):
        now = datetime.datetime.utcnow()
        identity_claim = app.config['JWT_IDENTITY_CLAIM']
        return {
            'exp': now + app.config['JWT_EXPIRES'],
            'iat': now,
            'nbf': now,
            identity_claim: identity,
            'aud': 'foo'
        }

    test_client = app.test_client()
    jwt = _get_jwt(test_client)
    response = _make_jwt_request(test_client, jwt, endpoint)
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 422
    assert json_data == {'msg': 'Invalid audience'}


@pytest.mark.parametrize("endpoint", [
    '/protected',
    '/optional',
])
def test_missing_aud(app, endpoint):
    app.config['JWT_DECODE_AUDIENCE'] = 'bar'

    test_client = app.test_client()
    jwt = _get_jwt(test_client)
    response = _make_jwt_request(test_client, jwt, endpoint)
    json_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 422
    assert json_data == {'msg': 'Token is missing the "aud" claim'}
