from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure(app):
  db.init_app(app)
  app.db = db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome_completo = db.Column(db.String(255))
  cpf = db.Column(db.String(11))
  email = db.Column(db.String(255))
  data_cadastro = db.Column(db.DateTime)


class Ponto(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User')
  data_batida = db.Column(db.DateTime)
  tipo_batida = db.Column(db.Integer)
