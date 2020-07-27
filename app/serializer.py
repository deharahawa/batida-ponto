from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields



class UserSchema(Schema):
  class Meta:
    type_ = 'user'
    self_view = 'user_one'
    self_view_kwargs = {'id': '<id>'}
    self_view_many = 'user_many'

    id = fields.Integer()
    nome_completo = fields.Str(required=True)
    cpf = fields.Integer()
    email = fields.Str(required=True)
    data_cadastro = fields.DateTime(dump_only=True)