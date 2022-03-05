from src.models.wine import WineModel


def test_attributes():
    """
    GIVEN a WineModel
    THEN check if the attributes are defined correctly
    """
    print('\n --- Should return wine with correct name, price, image, type, year and country')
    wine_attributes = ['name', 'price', 'year', 'image', 'type', 'country']
    for attribute in wine_attributes:
        if attribute == 'name':
            assert WineModel.name.unique == True
            assert WineModel.name.nullable == False
        elif attribute == 'price':
            assert WineModel.price.nullable == False
        elif attribute == 'year':
            assert WineModel.year.nullable == False
        elif attribute == 'image':
            assert WineModel.image.nullable == False
        assert hasattr(WineModel, attribute)
    assert WineModel.__tablename__ == 'wines'


def test_new_wine():
    """
    GIVEN a WineModel
    WHEN a new wine is created
    THEN check that the name, price, image, type, year and country are defined correctly
    """
    print('\n --- Should return wine with correct name, price, image, type, year and country')

    wine = WineModel(name='Test Wine', price=1000, image='http://test.com/image.jpg',
                     country='Test Country', year=2020, type='Test Type')
    assert wine.name == 'Test Wine'
    assert wine.price == 1000
    assert wine.image == 'http://test.com/image.jpg'
    assert wine.country == 'Test Country'
    assert wine.year == 2020
    assert wine.type == 'Test Type'
    
