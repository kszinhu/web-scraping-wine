from flask import url_for
from src.models.wine import WineModel
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

wine_data = {
    'name': 'Test Wine',
    'price': 1000,
    'link': 'http://test.com',
    'image': 'http://test.com/image.jpg'}


def test_create_wine(client):
    """
    GIVEN a client
    WHEN a wine is created
    THEN check status code is CREATED and that the wine is in the database
    """
    print('\n --- Should return 200 when wine is created')

    response = client.post(url_for('api.wine_list'), json=wine_data)
    assert response.status_code == HTTP_201_CREATED
    assert WineModel.query.filter_by(name='Test Wine').first() is not None


def test_update_wine(client):
    """
    GIVEN a client
    WHEN a wine is updated
    THEN check status code is OK and that the wine is in the database
    """
    print('\n --- Should return 200 when wine is updated')

    response = client.put(url_for('api.wine', id=1), json={
                          **wine_data, 'name': 'Test Wine Updated'})
    assert response.status_code == HTTP_200_OK
    assert WineModel.query.filter_by(id=1).first().name == 'Test Wine Updated'


def test_delete_wine(client):
    """
    GIVEN a client
    WHEN a wine is deleted
    THEN check status code is OK and that the wine is not in the database
    """
    print('\n --- Should return 200 when wine is deleted')

    response = client.delete(url_for('api.wine', id=1))
    assert response.status_code == HTTP_204_NO_CONTENT
    assert WineModel.query.filter_by(id=1).first() is None


def test_index_wine(client):
    """
    GIVEN a client
    WHEN a wine is deleted
    THEN check status code is OK and that the wine is not in the database
    """
    print('\n --- Should return 200 when wine is deleted')

    response = client.get(url_for('api.wine_list'))
    assert response.status_code == HTTP_200_OK
    assert len(response.json) == WineModel.query.count()
