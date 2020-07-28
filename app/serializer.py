# from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from marshmallow import ValidationError
from flask_marshmallow import Marshmallow

ma = Marshmallow()

def configure(app):
  ma.init_app(app)


def must_not_be_blank(data):
  if not data:
    raise ValidationError('Dado não informado')

# class UserSchema(Schema):
class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    type_ = 'user'
    self_view = 'user_one'
    self_view_kwargs = {'id': '<id>'}
    self_view_many = 'user_many'

  id = fields.Integer()
  nome_completo = fields.Str(required=True, validate=must_not_be_blank)
  cpf = fields.Str(required=True,validate=must_not_be_blank)
  email = fields.Str(required=True, validate=must_not_be_blank)
  data_cadastro = fields.DateTime(dump_only=True)


# class PontoSchema(Schema):
class PontoSchema(ma.SQLAlchemyAutoSchema):
  # class Meta:
  #   type_ = 'ponto'
  #   self_view = 'ponto_one'
  #   self_view_kwargs = {'id': '<id>'}
  id = fields.Integer()
  user = fields.Nested(UserSchema, validate=must_not_be_blank)
  data_batida = fields.DateTime(dump_only=True)
  tipo_batida = fields.Integer()
