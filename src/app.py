from flask import jsonify
from src.ma import ma
from src.db import db
from src.server import auth # Authorization module
from src.config import config # Configuration module
from src.server.instance import server # Server instance
from src.controllers.wine import Wine, WineList # Controllers
from marshmallow import ValidationError

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
