from flask import Blueprint, request, jsonify, current_app
from .serializer import UserSchema
from .models import User
from datetime import datetime
from json import JSONEncoder
import json

user_blueprint = Blueprint('usuarios', __name__)

@user_blueprint.route('/cadastrar', methods=['POST'])
def cadastrar():
  user_schema = UserSchema()

  user, error = user_schema.load(request.json)

  if error:
    return jsonify(error), 401

  now = datetime.now()

  user = User(nome_completo=user['nome_completo'], cpf=user['cpf'], email=user['email'], data_cadastro=now)
  
  current_app.db.session.add(user)
  current_app.db.session.commit()

  return user_schema.jsonify(user), 201

@user_blueprint.route('/mostrar', methods=['GET'])
def mostrar():
  result = User.query.all()
  return UserSchema(many=True).jsonify(result), 200


@user_blueprint.route('/modificar/<identificador>', methods=['POST'])
def modificar(identificador):
    user_schema = UserSchema()
    query = User.query.filter(User.id == identificador)
    query.update(request.json)
    current_app.db.session.commit()
    return user_schema.jsonify(query.first())

@user_blueprint.route('/deletar/<identificador>', methods=['GET'])
def deletar(identificador):
    User.query.filter(User.id == identificador).delete()
    current_app.db.session.commit()
    return jsonify('Deletado')