# -*- coding: utf-8 -*-
# config.py

# Chave da API do Tiny
TINY_API_KEY = "332226d25500bcca177fbfb7ad368c45c1ed9ca9"

# URL base da API do Tiny
BASE_URL = "https://api.tiny.com.br/api2"

# Configuração do SQLAlchemy (Banco de Dados)
SQLALCHEMY_DATABASE_URI = 'sqlite:///produtos.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuração do Celery (Backend do Redis para tarefas assíncronas)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'