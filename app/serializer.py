from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from marshmallow import ValidationError

def must_not_be_blank(data):
  if not data:
    raise ValidationError('Dado não informado')

class UserSchema(Schema):
  class Meta:
    type_ = 'user'
    self_view = 'user_one'
    self_view_kwargs = {'id': '<id>'}
    self_view_many = 'user_many'

    id = fields.Integer(dump_only=True)
    nome_completo = fields.Str(required=True, validate=must_not_be_blank)
    cpf = fields.Str(required=True,validate=must_not_be_blank)
    email = fields.Str(required=True, validate=must_not_be_blank)
    data_cadastro = fields.DateTime(dump_only=True)