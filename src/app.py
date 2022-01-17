from flask import Flask, jsonify, request
from flask_restx import Api
from src.ma import ma
from src.db import db
from src.helpers import auth # Auxiliary methods
from src.config import config # Configuration
from src.controllers.wine import Wine, WineList # Controllers

from marshmallow import ValidationError

from src.server.instance import server

api = server.api
app = server.app

# Add config to app
app.config.from_object(config)

# Verifies authorization to each request
@app.before_request
@auth.token_required

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

# Error handler
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.messages), 400

# Routes
api.add_resource(Wine, '/wine/<int:id>')
api.add_resource(WineList, '/wines')

# Initialize the database
db.init_app(app)
if __name__ == '__main__':
    ma.init_app(app)
    server.run()
