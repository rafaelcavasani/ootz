# Projeto

Esse é um projeto de uma API REST para cadastro de produtos e seus kits.

Foi utilizado para o desenvolvimento:

- Django
- Django Rest FrameWork
- MySQL

# Documentação

[Postman](https://documenter.getpostman.com/view/7778735/TVRg6Umz)

## Como Rodar com Docker

Faça o clone do projeto e digite os seguintes comandos, dentro da pasta do projeto, no terminal:

Suba os containers Django e MySQL:

```
docker-compose build
docker-compose up -d
```

Acesse o bash do container da API para executar os comandos abaixo:

```
docker exec -it ootz_api bash
```

Crie as tabelas do banco de dados:

```
python manage.py migrate
```

Crie um usuário para autenticação na API:

```
python manage.py createsuperuser
```

## Como Rodar Localmente

Pré-requisitos de ambiente:

- Python
- VirtualEnv
- MySQL

Altere a variável DB_HOST do arquivo `.env` para `localhost` ou o host que seu MySQL está executando.
Crie um novo schema no MySQL com nome `ootz`.
Crie um novo usuário com as permissões necessárias para o schema criado conforme as variáveis `DB_USER` e `DB_PASSWORD` do arquivo `.env`.

Crie uma virtual env na pasta do projeto:

`virtualenv venv` ou `python -m venv venv`

Instale as dependências do python:

```
pip install -r requirements.txt
```

Crie as tabelas do banco de dados:

```
python manage.py migrate
```

Crie um usuário para autenticação na API:

```
python manage.py createsuperuser
```

Suba a API:

```
python manage.py runserver
```
