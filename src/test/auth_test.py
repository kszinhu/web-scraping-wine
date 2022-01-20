# When token not provided, the request will fail with 401
def test_auth_required_without_token(client):
    print('\nShould return 401 when token is missing')

    response = client.get('/wines')
    assert response.status_code == 401


def test_auth_required_with_token(client, fake_db):
    import os
    print('\nShould return 200 when token is provided')
    
    api_key_headers = {'wine-token': os.environ['API_TOKEN']}
    response = client.get('/wines', headers=api_key_headers)
    assert response.status_code == 200
