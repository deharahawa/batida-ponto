from flask import Blueprint, request, jsonify, current_app
from .serializer import PontoSchema
from .models import Ponto, User
from datetime import datetime
from marshmallow import ValidationError
import re


ponto_blueprint = Blueprint('checks', __name__)

def get_horas(dado):
  horas = re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}', dado)
  return horas


def get_date(dado):
  date = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', dado)
  return date


def get_ano_mes_dia(dado):
  ano, mes, dia = re.split('[^0-9]+', dado)
  return int(ano), int(mes), int(dia)


def get_hora_minutos_segs(dado):
  hora, minutos, segs = re.split('[^0-9]+', dado)
  return int(hora), int(minutos), int(segs)


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

  # Puxa todos os pontos do usuario
  ponto_anterior = Ponto.query.filter(Ponto.user_id == data['user_id'])

  ponto_anterior = PontoSchema(many=True).jsonify(ponto_anterior)
  # Converte para json
  ponto_anterior_json = ponto_anterior.json

  if len(ponto_anterior_json) > 0:
    # Guarda o tipo de batida de ponto anterior
    tipo_batida_memory = 0
    # Salva realmente o tipo de batida anterior
    tipo_batida_memory = ponto_anterior_json[len(ponto_anterior_json)-1]['tipo_batida']   
    # Confere se o usuário nao esta batendo ponto em duplicata
    if tipo_batida_memory != data['tipo_batida']:
      tipo_batida_memory = data['tipo_batida']
    else:
      return {"message":"Ponto já batido"}

  if user is None:
    user = User(nome_completo="Nao identificado", cpf="0", email='nao@identificado.com', data_cadastro=now)

  ponto = Ponto(user=user, user_id=data['user_id'], tipo_batida=data['tipo_batida'], data_batida=now)

  current_app.db.session.add(ponto)
  current_app.db.session.commit()

  # result = ponto_schema.dump(Ponto.query.get(ponto.id))

  return ponto_schema.jsonify(ponto), 201

@ponto_blueprint.route('/pontos', methods=['GET'])
def mostrar():
  result = Ponto.query.all()
  return PontoSchema(many=True).jsonify(result), 200


@ponto_blueprint.route('/pontos/<identificador>', methods=['GET'])
def mostrar_usuario(identificador):
  result = Ponto.query.filter_by(user_id = identificador)
  horas_trabalhadas = calcula_horas(identificador)

  result = PontoSchema(many=True).jsonify(result)

  # Faz o append no último ponto retornado
  result.json[len(result.json)-1]['horas_trabalhadas'] = horas_trabalhadas.get('horas trabalhadas')

  return jsonify(result.json), 200


@ponto_blueprint.route('/pontos-user/<identificador>', methods=['GET'])
def calcula_horas(identificador):
  data = Ponto.query.filter(Ponto.user_id == identificador)
  result_json = PontoSchema(many=True).jsonify(data)
  # Cria listas para guardar entradas e saidas
  entrada = []
  saida = []
  for field in result_json.json:
    if field['tipo_batida'] == 1:
      entrada.append(field['data_batida'])
    else:
      saida.append(field['data_batida'])
  
  # Precisa pegar o total de horas trabalhadas
  horas_total = []

  counter_entradas = 0

  for i in range(len(saida)):
    # Nao deve dar problemas porque contamos as saidas, se o funcionario deu entrada e ainda nao saiu o vetor de saidas vai ser automaticamente menor que o de entradas
    # Pega a data de entrada
    date_entrada = get_date(entrada[i])
    ano_entrada, mes_entrada, dia_entrada = get_ano_mes_dia(date_entrada[0])
    # Pega a data de saida
    date_saida = get_date(saida[i])
    ano_saida, mes_saida, dia_saida = get_ano_mes_dia(date_saida[0])
    if ano_saida != ano_entrada:
      continue
    if mes_saida != mes_entrada:
      continue
    if dia_entrada > dia_saida:
      continue

    # Pega hora de entrada e saida
    time_entrada = get_horas(entrada[i])
    time_saida = get_horas(saida[i])

    hora_entrada, mins_entrada, segs_entrada = get_hora_minutos_segs(time_entrada[0])
    hora_saida, mins_saida, segs_saida = get_hora_minutos_segs(time_saida[0])
    if (dia_saida - dia_entrada) == 1:
      # Caso de um turno noturno
      if hora_entrada > hora_saida:
        if mins_entrada > mins_saida:
          minutos_trabalhados = 60 - mins_entrada
          minutos_trabalhados += mins_saida
          # desconta porque a hora nao é completa
          hora_saida -= 1
        elif mins_entrada <= mins_saida:
          minutos_trabalhados = mins_saida - mins_entrada
        hora_entrada_mins = (24*60) - ((hora_entrada*60) + mins_entrada)
        if (hora_entrada_mins + minutos_trabalhados) >= 60:
          minutos_trabalhados -= 60
          hora_saida += 1

        horas_trabalhadas = hora_saida + (minutos_trabalhados/60)

        horas_total.append(horas_trabalhadas)
      else:
        # Entao foi no mesmo dia e o for vai tratar ainda
        continue
    if dia_saida == dia_entrada:

      if mins_entrada > mins_saida:
        minutos_trabalhados = 60 - mins_entrada
        minutos_trabalhados += mins_saida
        # desconta porque a hora nao é completa
        hora_saida -= 1
      elif mins_entrada <= mins_saida:
        minutos_trabalhados = mins_saida - mins_entrada
      hora_entrada_mins = (24*60) - ((hora_entrada*60) + mins_entrada)
      if (hora_entrada_mins + minutos_trabalhados) >= 60:
        minutos_trabalhados -= 60
        hora_saida += 1

      horas_trabalhadas = (hora_saida-hora_entrada) + (minutos_trabalhados/60)

      horas_total.append(horas_trabalhadas)

  soma_horas = 0.0
  for horas in horas_total:
    soma_horas += horas

  return {"horas trabalhadas": ("%.2f horas" % soma_horas)}


@ponto_blueprint.route('/limpar/', methods=['GET'])
def deletar():
    Ponto.query.filter().delete()
    current_app.db.session.commit()
    return jsonify('Limpa a base')