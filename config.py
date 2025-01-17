# -*- coding: utf-8 -*-
# config.py

# Configurações para o Tiny ERP
TINY_CLIENT_ID = "tiny-api-d4c818007ad48771afe75f79652f7c2bf3268447-1733157799"
TINY_CLIENT_SECRET = "zECJh5uKoOiIY0IMkaPy1qiMD3AWaUYq"
TINY_REDIRECT_URI = "http://127.0.0.1:5000/callback"
TINY_API_TOKEN = "e94b48205ec0e02e25eb855a32564acc08045cf4bda3f12da1d19a0329bc0f05"

# URL base da API do Tiny
BASE_URL = "https://api.tiny.com.br/oauth/v3/token"

# Credenciais Mercado Livre
MERCADO_LIVRE_APP_ID = "3970896740233001"
MERCADO_LIVRE_SECRET = "pXS7hT8dJ3B4ApIcT6p1BzhTBxKluQ9u"
REDIRECT_URI = "http://127.0.0.1:5000/ml/callback"  # URL configurada no app

# Configuração do SQLAlchemy (Banco de Dados)
SQLALCHEMY_DATABASE_URI = 'sqlite:///produtos.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuração do Celery (Backend do Redis para tarefas assíncronas)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'