from flask import request, jsonify
from functools import wraps, update_wrapper
from src.constants.http_status_code import HTTP_401_UNAUTHORIZED

def decode_auth_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")
        return data['wine-token'] == app.config['API_TOKEN']
    except:
        return jsonify({'message': 'Token is invalid!'}), HTTP_401_UNAUTHORIZED

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


