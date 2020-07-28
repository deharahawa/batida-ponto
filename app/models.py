from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import ResourceDetail, ResourceList
from .serializer import UserSchema

db = SQLAlchemy()

def configure(app):
  """
  Factory para poder configurar
  """
  # Inicializa o app
  db.init_app(app)
  with app.app_context():
    # Cria as alteracoes usando o contexto
    db.create_all()
  app.db = db

class User(db.Model):
  """
  Define a class que reprenta o model do User
  """
  id = db.Column(db.Integer, primary_key=True)
  nome_completo = db.Column(db.String(255))
  cpf = db.Column(db.String(11))
  email = db.Column(db.String(255))
  data_cadastro = db.Column(db.DateTime)


class Ponto(db.Model):
  """
  Define a class que reprenta o model do Ponto
  """
  id = db.Column(db.Integer, primary_key=True)
  # Define a chave estrangeira do relacionamento 1 para muitos
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  # Define o relacionamento entre user e pontos
  user = db.relationship('User', backref='checks')
  data_batida = db.Column(db.DateTime)
  tipo_batida = db.Column(db.Integer)