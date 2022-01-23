from flask import request
import jwt
from config import JWT_ALGORITHM, JWT_SECRET_KEY, JWT_TOKEN_EXPIRY_SECONDS
import datetime
from functools import wraps


def verify_password():
    auth = request.authorization

    if not auth:
        return {"error": "Basic Auth necessary"}, 401

    _id = auth["username"]
    pwd = auth["password"]

    valid_user = all([_id == "super-user", pwd == "secret"])

    if not valid_user:
        return {"error": "Invalid Username or Password"}, 401

    return auth


def generate_token(client_id):

    payload = {
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(seconds=JWT_TOKEN_EXPIRY_SECONDS),
        "iat": datetime.datetime.utcnow(),
        "sub": client_id,

    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def auth_needed(func):
    @wraps(func)
    def verify_token():
        auth_header = request.headers.get("Authorization")

        token = auth_header.split(" ")[1]

        import ipdb; ipdb.set_trace()
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    return verify_token
