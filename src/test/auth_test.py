# from api import check_auth

def test_auth_required_401(client):
    response = client.get('/wines')
    assert response.status_code == 401

# def test_auth_required_with_token(client):
#     response = client.get('http://localhost:5000/wines',
#                        headers={'wine-token': os.environ.get('TEST_TOKEN')})
#     assert response.status_code == 200
