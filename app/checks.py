from flask import Blueprint, request, jsonify, current_app
from .serializer import PontoSchema
from .models import Ponto, User
from datetime import datetime
from marshmallow import ValidationError
import re


ponto_blueprint = Blueprint('checks', __name__)

def get_horas(dado):
  """
  Usa regex para pegar as horas no formato UTC
  """
  horas = re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}', dado)
  return horas


def get_date(dado):
  """
  Usa regex para pegar a data no formato UTC
  """
  date = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', dado)
  return date


def get_ano_mes_dia(dado):
  """
  Usa regex para separar ano, mes e dia
  """
  ano, mes, dia = re.split('[^0-9]+', dado)
  return int(ano), int(mes), int(dia)


def get_hora_minutos_segs(dado):
  """
  Usa regex para separar hora, minutos e segundos
  """
  hora, minutos, segs = re.split('[^0-9]+', dado)
  return int(hora), int(minutos), int(segs)


@ponto_blueprint.route('/ponto', methods=['POST'])
def cadastrar():
  # Instancia PontoSchema
  ponto_schema = PontoSchema()

  json_data = request.json
  # Checa se existem dados vindo na request
  if not json_data:
    return {"message": "Sem dados informados"}, 400
  # Verificar se ha error ao realizar o load
  try:
    data, errors = ponto_schema.load(json_data)
  except ValidationError as err:
    return err.messages, 422
  # Pega o user que esta batendo o ponto
  user = User.query.filter_by(id = data['user_id']).first()

  # Puxa todos os pontos batidos do usuario
  ponto_anterior = Ponto.query.filter(Ponto.user_id == data['user_id'])
  # Pega o ponto anterior para verificar se o usuario nao esta batendo o mesmo tipo de ponto 2 vezes
  ponto_anterior = PontoSchema(many=True).jsonify(ponto_anterior)
  # Converte para json
  ponto_anterior_json = ponto_anterior.json
  # Verifica se ja ha um ponto batido, senao nao ha anterior
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
  # Pega o horario atual
  now = datetime.now()

  if user is None:
    # Cadastra um usuario para o ponto caso nao exista na base
    user = User(nome_completo="Nao identificado", cpf="0", email='nao@identificado.com', data_cadastro=now)
  # Cria o ponto
  ponto = Ponto(user=user, user_id=data['user_id'], tipo_batida=data['tipo_batida'], data_batida=now)
  # Salva as alteracoes no banco
  current_app.db.session.add(ponto)
  current_app.db.session.commit()

  return ponto_schema.jsonify(ponto), 201

@ponto_blueprint.route('/pontos', methods=['GET'])
def mostrar():
  """
  Seleciona todos os pontos batidos por todos os usuarios
  """
  result = Ponto.query.all()
  return PontoSchema(many=True).jsonify(result), 200


@ponto_blueprint.route('/pontos/<identificador>', methods=['GET'])
def mostrar_usuario(identificador):
  """
  Mostra todos os pontos de um usuario especifico 
  """
  # Faz a query usando o user_id
  result = Ponto.query.filter_by(user_id = identificador)
  # Chama a funcao que calcula o total de horas para determinado usuario
  horas_trabalhadas = calcula_horas(identificador)
  # Pega o result da query feita anteriormente
  result = PontoSchema(many=True).jsonify(result)

  # Faz o append das horas trabalhadas no último ponto retornado
  result.json[len(result.json)-1]['horas_trabalhadas'] = horas_trabalhadas.get('horas trabalhadas')

  return jsonify(result.json), 200


@ponto_blueprint.route('/pontos-user/<identificador>', methods=['GET'])
def calcula_horas(identificador):
  """
  Calcula as horas trabalhadas 
  """
  # Calcula as horas trabalhadas pelo user
  data = Ponto.query.filter(Ponto.user_id == identificador)
  # Pega o result da query
  result_json = PontoSchema(many=True).jsonify(data)
  # Cria listas para guardar entradas e saidas
  entrada = []
  saida = []
  # Varre os campos do result da query para separar o que sao batidas de ponto de entrada e saida
  for field in result_json.json:
    if field['tipo_batida'] == 1:
      entrada.append(field['data_batida'])
    else:
      saida.append(field['data_batida'])
  
  # Precisa pegar o total de horas trabalhadas
  horas_total = []


  for i in range(len(saida)):
    # Nao deve dar problemas porque contamos as saidas, se o funcionario deu entrada e ainda nao saiu o vetor de saidas vai ser automaticamente menor que o de entradas
    # Pega a data de entrada
    date_entrada = get_date(entrada[i])
    ano_entrada, mes_entrada, dia_entrada = get_ano_mes_dia(date_entrada[0])
    # Pega a data de saida
    date_saida = get_date(saida[i])
    ano_saida, mes_saida, dia_saida = get_ano_mes_dia(date_saida[0])
    # Faz algumas verificacoes para nao realizar comparacoes que nao fazem sentido
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
          # Caso a diferenca entre os minutos nao complete uma hora e reinicie a contagem por ter virado a hora
          # Por exemplo de 23:59 ate 09:05, temos 6 minutos e aqui eh possivel realizar esse calculo
          minutos_trabalhados = 60 - mins_entrada
          minutos_trabalhados += mins_saida
          # desconta porque a hora nao é completa
          hora_saida -= 1
        elif mins_entrada <= mins_saida:
          # Calcula normalmente os minutos trabalhados
          minutos_trabalhados = mins_saida - mins_entrada
        # Calcula o tempo ate a meia noite
        hora_entrada_mins = (24*60) - ((hora_entrada*60) + mins_entrada)
        if (hora_entrada_mins + minutos_trabalhados) >= 60:
          while((hora_entrada_mins + minutos_trabalhados) >= 60):
            # Faz a conversao das horas ate a meia noite e sobram os minutos trabalhados que serao calculados como fracao de hora
            minutos_trabalhados -= 60
            hora_saida += 1
        # Computa as horas trabalhadas + a fracao de hora
        horas_trabalhadas = hora_saida + (minutos_trabalhados/60)

        horas_total.append(horas_trabalhadas)
      else:
        # Entao foi no mesmo dia e o for vai tratar ainda
        continue
    if dia_saida == dia_entrada:
      # Caso de entrada e saida no mesmo dia
      if mins_entrada > mins_saida:
        # Caso a diferenca entre os minutos nao complete uma hora e reinicie a contagem por ter virado a hora
        # Por exemplo de 10:45 ate 11:10, temos 25 minutos e aqui eh possivel realizar esse calculo
        minutos_trabalhados = 60 - mins_entrada
        minutos_trabalhados += mins_saida
        # desconta porque a hora nao é completa
        hora_saida -= 1
      elif mins_entrada <= mins_saida:
        minutos_trabalhados = mins_saida - mins_entrada
      
      # Computa as horas trabalhadas subtraindo a hora de saida da hora de entrada + fracoes de minutos
      horas_trabalhadas = (hora_saida-hora_entrada) + (minutos_trabalhados/60)

      horas_total.append(horas_trabalhadas)

  soma_horas = 0.0
  for horas in horas_total:
    # Faz o somatorio das horas totais de todos os dias ou periodos
    soma_horas += horas

  return {"horas trabalhadas": ("%.2f horas" % soma_horas)}


@ponto_blueprint.route('/limpar/', methods=['GET'])
def deletar():
    """
    Limpa todos os pontos 
    """
    # Pega todas as batidas de ponto e deleta
    Ponto.query.filter().delete()
    # Salva as alteracoes no banco
    current_app.db.session.commit()
    return jsonify('Limpa a base')