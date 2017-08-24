from flask import Flask, jsonify, request
from flask_jwt_simple import JWTManager, jwt_required, create_jwt

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint. There are other
# behaviors tht can be changed with these loader functions.
# Check the docs for a full list.
@jwt.expired_token_loader
def my_expired_token_callback():
    err_json = {
        "status": 401,
        "title": "Expired JWT",
        "detail": "The JWT has expired"
    }
    return jsonify(err_json), 401


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {'access_token': create_jwt(username)}
    return jsonify(ret), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'}), 200

if __name__ == '__main__':
    app.run()
