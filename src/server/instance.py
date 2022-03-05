import os
from flask import Flask, Blueprint
from flask_restx import Api
from src.config import config

class Server():
  def __init__(self, ):
    
    self.app = Flask(__name__)
    self.blueprint = Blueprint('api', __name__, url_prefix='/api')
    self.api = Api(self.blueprint, doc='/doc', title='Wine Scraping Api')
    self.app.register_blueprint(self.blueprint)

    self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    self.app.config['PROPAGATE_EXCEPTIONS'] = True
    self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    self.wine_ns = self.wine_ns()

    super().__init__()

  def wine_ns(self, ):
    return self.api.namespace(name='Wines', description='Wine Scraping Api', path='/')

  def run(self, ):
    # Running on gunicorn
    self.app.run(host='0.0.0.0', port=5000, debug=True)

server = Server()