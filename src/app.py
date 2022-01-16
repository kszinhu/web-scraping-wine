from flask import Flask, jsonify
from flask_restx import Api

from ma import ma
from db import db
from controllers.wine import Wine, WineList

from marshmallow import ValidationError

from server.instance import server

api = server.api
app = server.app

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.messages), 400

api.add_resource(Wine, '/wine/<int:id>')
api.add_resource(WineList, '/wines')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    server.run()
