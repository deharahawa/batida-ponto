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

flask run
```
## Como fazer as migrations
```sh
flask db init
flask db migrate
flask db upgrade
```