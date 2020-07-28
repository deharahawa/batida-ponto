from flask import Flask
from flask_migrate import Migrate
from .models import configure as config_db
from .serializer import configure as config_ma

def create_app():
  app = Flask(__name__)

  # sqlite db uri configuration
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'

  # remove error from track mod
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  # Configura DB
  config_db(app)
  # Configura Marshmallow
  config_ma(app)
  # Realiza migration
  Migrate(app, app.db)
  
  # Import dos blueprints
  from .users import user_blueprint
  app.register_blueprint(user_blueprint)

  from .checks import ponto_blueprint
  app.register_blueprint(ponto_blueprint)

  return app