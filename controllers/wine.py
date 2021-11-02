from flask import request, jsonify
from flask_restplus import Resource, fields
from constants.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST

from models.wine import WineModel
from schemas.wine import WineSchema

from server.instance import server

wine_ns = server.wine_ns

wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)


class Wine(Resource):

    def get(self, id):
        wine = WineModel.find_by_id(id)
        if wine:
            return wine_schema.dump(wine), HTTP_200_OK
        return jsonify({"errors": "Wine not found"}), HTTP_400_BAD_REQUEST

    def delete(self, id):
        wine = WineModel.find_by_id(id)
        if wine:
            wine.delete_from_db()
            return wine_schema.dump(wine), HTTP_200_OK
        return jsonify({"errors": "Wine not found"}), HTTP_400_BAD_REQUEST
