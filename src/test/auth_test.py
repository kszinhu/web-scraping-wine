from flask import url_for

def test_auth_required_without_token(client):
    print('\n --- Should return 401 when token is missing')

    response = client.get('/')
    assert response.status_code == 401

def test_auth_required_with_token(client):
    print('\n --- Should return 200 when token is provided')
    
    token = client.application.config['API_TOKEN']

    response = client.get(url_for('api.wine_list'), headers={'wine-token': token})
    assert response.status_code == 200
