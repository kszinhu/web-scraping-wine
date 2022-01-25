from src.models.wine import WineModel


def test_attributes():
    """
    GIVEN a WineModel
    THEN check if the attributes are defined correctly
    """
    print('\n --- Should return wine with correct name, price, link, and image')
    wine_attributes = ['name', 'price', 'link', 'image']
    for attribute in wine_attributes:
        if attribute == 'name':
            assert WineModel.name.unique == True
            assert WineModel.name.nullable == False
        elif attribute == 'price':
            assert WineModel.price.nullable == False
        elif attribute == 'link':
            assert WineModel.link.nullable == False
        elif attribute == 'image':
            assert WineModel.image.nullable == False
        assert hasattr(WineModel, attribute)
    assert WineModel.__tablename__ == 'wines'


def test_new_wine():
    """
    GIVEN a WineModel
    WHEN a new wine is created
    THEN check that the name, price, link, and image are defined correctly
    """
    print('\n --- Should return wine with correct name, price, link, and image')

    wine = WineModel(name='Test Wine', price=1000,
                     link='http://test.com', image='http://test.com/image.jpg')
    assert wine.name == 'Test Wine'
    assert wine.price == 1000
    assert wine.link == 'http://test.com'
    assert wine.image == 'http://test.com/image.jpg'
