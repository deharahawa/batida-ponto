# from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from marshmallow import ValidationError
from flask_marshmallow import Marshmallow

ma = Marshmallow()

def configure(app):
  """
  Factory para poder configurar
  """
  ma.init_app(app)


def must_not_be_blank(data):
  """
  Valida que os dados nao estao em branco
  """
  if not data:
    raise ValidationError('Dado não informado')

# class UserSchema(Schema):
class UserSchema(ma.SQLAlchemyAutoSchema):
  """
  Define o Schema do User
  """
  id = fields.Integer()
  nome_completo = fields.Str(required=True, validate=must_not_be_blank)
  cpf = fields.Str(required=True,validate=must_not_be_blank)
  email = fields.Str(required=True, validate=must_not_be_blank)
  data_cadastro = fields.DateTime(dump_only=True)
  # pontos = ma.Nested(PontoSchema, many=True)


# class PontoSchema(Schema):
class PontoSchema(ma.SQLAlchemyAutoSchema):
  id = fields.Integer()
  user = fields.Nested(UserSchema, validate=must_not_be_blank)
  user_id = fields.Integer()
  data_batida = fields.DateTime(dump_only=True)
  tipo_batida = fields.Integer()