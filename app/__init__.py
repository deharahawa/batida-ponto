from flask import Flask
from flask_migrate import Migrate
from flask_rest_jsonapi import Api
from .models import configure as config_db
from .models import UserOne, UserMany

def create_app():
  app = Flask(__name__)

  # sqlite db uri configuration
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/artists.db'

  # remove error from track mod
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  config_db(app)

  Migrate(app, app.db)

  api = Api(app)
  api.route(UserMany, 'user_many', '/users')
  # api.route(UserOne, 'user_one', '/user/<int:id>')


  return app