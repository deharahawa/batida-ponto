# Registro de Ponto

Criação de um sistema simples para controle de entrada e saída de uma empresa. 
O sistema deve permitir o cadastro de usuários e o registro de ponto dos
mesmos.

## Requisitos
- flask-rest-jsonapi
- flask-sqlalchemy
- flask-migrate

Para instalar basta rodar 
```
pip3 install -r requirements.txt
```

## Configurar ambiente virtual
```sh
python3 -m venv .venv
source .venv/bin/activate
```

## Como rodar o app
```sh
export FLASK_APP=app
export FLASK_DEBUG=True

flask run
```
## Como fazer as migrations
```sh
flask db init
flask db migrate
flask db upgrade
```

## Endpoints Usuario
```sh
CREATE
GET http://localhost:5000/mostrar

READ
POST http://localhost:5000/cadastrar

UPDATE
POST http://localhost:5000/modificar/<id do usuario>

DELETE
GET http://localhost:5000/deletar/<id do usuario>
```

## Endpoints Ponto
```sh
DELETE
GET http://localhost:5000/limpar

Mostrar somente horas trabalhadas por usuário
GET http://localhost:5000/pontos-user/<id do usuario>

READ todos os pontos
GET http://localhost:5000/pontos

Mostrar todas as batidas de pontos do usuario 
mais horas trabalhadas
GET http://localhost:5000/pontos/<id do usuario>

CREATE
POST http://localhost:5000/ponto
```