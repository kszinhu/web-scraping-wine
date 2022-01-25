from flask import jsonify
from src.constants.http_status_code import HTTP_401_UNAUTHORIZED
import jwt


def decode_auth_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")
        return data['wine-token'] == app.config['API_TOKEN']
    except:
        return jsonify({'message': 'Token is invalid!'}), HTTP_401_UNAUTHORIZED
