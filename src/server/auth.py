from flask import request, jsonify
from functools import wraps
from src.constants.http_status_code import HTTP_401_UNAUTHORIZED
from src.helpers.token import decode_auth_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'wine-token' in request.headers:
            token = request.headers['wine-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), HTTP_401_UNAUTHORIZED

        if not decode_auth_token(token):
            return jsonify({'message': 'Token is invalid!'}), HTTP_401_UNAUTHORIZED
        return f(*args, **kwargs)
    return decorated
