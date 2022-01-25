from flask import url_for
from src.constants.http_status_code import HTTP_200_OK, HTTP_401_UNAUTHORIZED


def test_auth_required_without_token(client_no_headers):
    print('\n --- Should return 401 when token is missing')

    response = client_no_headers.get('/')
    assert response.status_code == HTTP_401_UNAUTHORIZED

def test_auth_required_with_token(client):
    print('\n --- Should return 200 when token is provided')
    
    token = client.application.config['API_TOKEN']

    response = client.get(url_for('api.wine_list'), headers={'wine-token': token})
    assert response.status_code == HTTP_200_OK
