from datetime import datetime

from flask import Flask, jsonify, request, current_app
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt
)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Using the jwt_data_loader, we can change the values that
# will be present in the JWTs (that are made by the
# `create_jwt()` function). This will override everything
# currently in the token, so you will need to re-add
# the default claims (exp, iat, nbt, sub) if you still
# want them.
@jwt.jwt_data_loader
def add_claims_to_access_token(identity):
    if identity == 'admin':
        roles = 'admin'
    else:
        roles = 'peasant'

    now = datetime.utcnow()
    return {
        'exp': now + current_app.config['JWT_EXPIRES'],
        'iat': now,
        'nbf': now,
        'sub': identity,
        'roles': roles
    }


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {'jwt': create_jwt(username)}
    return jsonify(ret), 200


# In a protected view, you can get the full data encoded in the
# jwt with the `get_jwt()` function.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    jwt_data = get_jwt()
    if jwt_data['roles'] != 'admin':
        return jsonify(msg="Permission denied"), 403
    return jsonify(msg="Do not forget to drink your ovaltine")


if __name__ == '__main__':
    app.run()
