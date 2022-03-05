from flask import request, jsonify
from flask_restx import Resource, fields
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from src.models.wine import WineModel
from src.schemas.wine import WineSchema

from src.server.instance import server

wine_ns = server.wine_ns

wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)

item = wine_ns.model('Wine', {
    'name': fields.String(description='Wine name'),
    'price': fields.Float(description='Wine price'),
    'image': fields.String(description='Wine image'),
    'type': fields.String(description='Wine type'),
    'year': fields.Integer(description='Wine year'),
    'country': fields.String(description='Wine country')
})


class Wine(Resource):

    def get(self, id):
        wine = WineModel.find_by_id(id)
        if wine:
            return wine_schema.dump(wine), HTTP_200_OK
        return jsonify({"errors": "Wine not found"}), HTTP_400_BAD_REQUEST

    def put(self, id):
        wine = WineModel.find_by_id(id)
        if wine:
            data = request.get_json()
            fields = ['name', 'price', 'image', 'type', 'year', 'country']
            for field in fields:
                if field in data:
                    setattr(wine, field, data[field])
            wine.save_to_db()
            return wine_schema.dump(wine), HTTP_200_OK
        return jsonify({"errors": "Wine not found"}), HTTP_400_BAD_REQUEST

    def delete(self, id):
        wine = WineModel.find_by_id(id)
        if wine:
            wine.delete_from_db()
            return wine_schema.dump(wine), HTTP_204_NO_CONTENT
        return jsonify({"errors": "Wine not found"}), HTTP_400_BAD_REQUEST


class WineList(Resource):

    def get(self):
        wines = WineModel.find_all()
        return wine_list_schema.dump(wines), HTTP_200_OK

    @wine_ns.expect(item)
    @wine_ns.doc('Create a new wine')
    def post(self):
        wine_data = request.get_json()
        wine = WineModel(**wine_data)
        wine.save_to_db()
        return wine_schema.dump(wine), HTTP_201_CREATED
