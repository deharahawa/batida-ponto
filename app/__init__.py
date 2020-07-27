from flask import Flask
from flask_migrate import Migrate
from .models import configure as config_db

def create_app():
  app = Flask(__name__)

  # sqlite db uri configuration
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'

  # remove error from track mod
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  config_db(app)

  Migrate(app, app.db)

  from .users import user_blueprint
  app.register_blueprint(user_blueprint)

  return app