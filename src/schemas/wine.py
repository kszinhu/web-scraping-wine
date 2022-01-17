from ma import ma
from models.wine import WineModel

class WineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WineModel
        load_instance = True