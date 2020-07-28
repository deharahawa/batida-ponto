from flask import Blueprint, request, jsonify, current_app
from .serializer import UserSchema
from .models import User
from datetime import datetime

user_blueprint = Blueprint('usuarios', __name__)

@user_blueprint.route('/cadastrar', methods=['POST'])
def cadastrar():
  """
  Cadastra um user na base 
  """
  # Instancia o Schema
  user_schema = UserSchema()
  # Faz o load dos dados da request
  user, error = user_schema.load(request.json)
  # Verifica se houve erro no load
  if error:
    return jsonify(error), 401
  # Pega a data atual no formato UTC
  now = datetime.now()
  # Cria o user
  user = User(nome_completo=user['nome_completo'], cpf=user['cpf'], email=user['email'], data_cadastro=now)
  # Salva as alteracoes no banco
  current_app.db.session.add(user)
  current_app.db.session.commit()

  return user_schema.jsonify(user), 201

@user_blueprint.route('/mostrar', methods=['GET'])
def mostrar():
  """
  Mostra todos os usuarios 
  """
  # Realiza a query de todos os usuarios
  result = User.query.all()
  return UserSchema(many=True).jsonify(result), 200


@user_blueprint.route('/modificar/<identificador>', methods=['POST'])
def modificar(identificador):
  """
  Possibilita modificar um usuario sem mexer no id e na data 
  """
  # Instancia o Schema
  user_schema = UserSchema()
  # Faz a query para o user especifico
  query = User.query.filter(User.id == identificador)
  # Faz o update
  query.update(request.json)
  # Salva a alteracao
  current_app.db.session.commit()
  return user_schema.jsonify(query.first())

@user_blueprint.route('/deletar/<identificador>', methods=['GET'])
def deletar(identificador):
  """
  Deleta um usuario 
  """
  # Faz a query em busca de um user especifico
  User.query.filter(User.id == identificador).delete()
  # Salva as alteracoes
  current_app.db.session.commit()
  return jsonify('Deletado')