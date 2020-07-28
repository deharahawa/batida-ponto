from flask import Blueprint, request, jsonify, current_app
from .serializer import PontoSchema
from .models import Ponto, User
from datetime import datetime
from marshmallow import ValidationError


ponto_blueprint = Blueprint('checks', __name__)

@ponto_blueprint.route('/ponto', methods=['POST'])
def cadastrar():
  ponto_schema = PontoSchema()

  json_data = request.json
  if not json_data:
    return {"message": "Sem dados informados"}, 400
  
  try:
    data, errors = ponto_schema.load(json_data)
  except ValidationError as err:
    return err.messages, 422

  user = User.query.filter_by(id = data['user_id']).first()

  now = datetime.now()

  if user is None:
    user = User(nome_completo="Nao identificado", cpf="0", email='nao@identificado.com', data_cadastro=now)

  ponto = Ponto(user=user, user_id=data['user_id'], tipo_batida=data['tipo_batida'], data_batida=now)
  print('ponto', ponto)
  current_app.db.session.add(ponto)
  current_app.db.session.commit()

  result = ponto_schema.dump(Ponto.query.get(ponto.id))

  return ponto_schema.jsonify(ponto), 201

@ponto_blueprint.route('/pontos', methods=['GET'])
def mostrar():
  result = Ponto.query.all()
  return PontoSchema(many=True).jsonify(result), 200

@ponto_blueprint.route('/pontos/<identificador>', methods=['GET'])
def mostrar_usuario(identificador):
  result = Ponto.query.filter_by(user_id = identificador)
  return PontoSchema(many=True).jsonify(result), 200
