from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
  app = Flask(__name__)

  # sqlite db uri configuration
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/artists.db'

  # remove error from track mod
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  return app