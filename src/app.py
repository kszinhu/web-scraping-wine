from flask import Flask, jsonify
from flask_restx import Api
from src.ma import ma
from src.db import db
from src.controllers.wine import Wine, WineList

from marshmallow import ValidationError

from src.server.instance import server

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

db.init_app(app) # Initialize the database
if __name__ == '__main__':
    ma.init_app(app)
    server.run()
