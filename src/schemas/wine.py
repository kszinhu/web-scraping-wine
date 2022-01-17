from src.ma import ma
from src.models.wine import WineModel

class WineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WineModel
        load_instance = True