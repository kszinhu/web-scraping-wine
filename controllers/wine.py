from flask import request
from flask_restplus import Resource, fields

from models.wines import WineModel
from schemas.wine import WineSchema

from server.instance import server

wine_ns = server.wine_ns

wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)


class Wine(Resource):

    def get(self, id):
        wine = WineModel.find_by_id(id)
        if wine:
            return wine_schema.dump(wine)
        return {'message': 'Wine not found'}, 404
