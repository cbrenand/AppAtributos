# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import requests
from config import TINY_API_KEY, SQLALCHEMY_DATABASE_URI  # type: ignore
from database import db
from models.product import Produto  # Importa o modelo Produto sem redefini-lo
import pandas as pd
from celery import Celery  # type: ignore
from services.tiny import buscar_produtos, buscar_detalhes_produto, criar_atributo_personalizado

# Inicializa o App Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configuração do Celery (usando Redis como backend)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Criação da tabela dentro do contexto da aplicação
with app.app_context():
    db.create_all()

# Rota inicial
@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "healthy"}), 200

# Rota para consultar produtos no Tiny
@app.route('/tiny/produtos', methods=['GET'])  # type: ignore
def consultar_produtos_tiny():
    """
    Consulta todos os produtos cadastrados no Tiny, página por página.
    """
    pagina = request.args.get("pagina", 1, type=int)
    produtos = buscar_produtos(pagina)
    if produtos:
        return jsonify(produtos)
    return jsonify({"error": "Nenhum produto encontrado"}), 404

# Rota para consultar detalhes de um produto específico no Tiny
@app.route('/tiny/produto/<sku>', methods=['GET'])  # type: ignore
def consultar_detalhes_produto_tiny(sku):
    """
    Consulta os detalhes de um produto específico no Tiny pelo SKU.
    """
    produto = buscar_detalhes_produto(sku)
    if produto:
        return jsonify(produto)
    return jsonify({"error": "Produto não encontrado"}), 404

# Rota para criar um atributo personalizado no Tiny
@app.route('/tiny/atributo', methods=['POST'])  # type: ignore
def criar_atributo_tiny():
    """
    Cria um atributo personalizado no Tiny.
    """
    dados = request.json
    nome = dados.get("nome")
    tipo = dados.get("tipo", "texto")
    valores = dados.get("valores", [])
    resultado = criar_atributo_personalizado(nome, tipo, valores)
    if "retorno" in resultado and "status" in resultado["retorno"] and resultado["retorno"]["status"] == "OK":
        return jsonify({"message": "Atributo criado com sucesso!"}), 201
    return jsonify({"error": "Erro ao criar atributo"}), 400

# Rota para consultar produto pelo SKU usando o Tiny
@app.route('/consultar_produto_sku/<sku>')
def consultar_produto_sku(sku):
    url = "https://api.tiny.com.br/api2/produtos.pesquisa"
    params = {
        "token": TINY_API_KEY,
        "formato": "json",
        "pesquisa": sku
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "retorno" in data and "produtos" in data["retorno"]:
        produto = data["retorno"]["produtos"][0]["produto"]
        return jsonify(produto)
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

# Função para enviar todos os dados do produto para o Tiny
def atualizar_produto_no_tiny(produto):
    url = "https://api.tiny.com.br/api2/produto.alterar"
    data = {
        "token": TINY_API_KEY,
        "formato": "json",
        "produto": produto
    }
    response = requests.post(url, json=data)
    return response.json()

# Função para processar produtos em lotes
@celery.task
def processar_lote_produtos(produtos):
    for produto in produtos:
        atualizar_produto_no_tiny(produto)

# Rota para atualizar produtos em massa
@app.route('/atualizar_produtos_em_massa', methods=['POST'])
def atualizar_produtos_em_massa():
    if 'file' not in request.files:
        return jsonify({"error": "Arquivo não enviado"}), 400

    file = request.files['file']
    produtos_df = pd.read_csv(file)
    produtos = produtos_df.to_dict(orient='records')

    lote_size = 500
    lotes = [produtos[i:i + lote_size] for i in range(0, len(produtos), lote_size)]

    for lote in lotes:
        processar_lote_produtos.delay(lote)

    return jsonify({"message": "Atualização em massa iniciada"}), 202

# Rota para consultar produtos com pendências nos marketplaces
@app.route('/produtos_pendentes_marketplaces', methods=['GET'])
def produtos_pendentes_marketplaces():
    url = "https://api.tiny.com.br/api2/produtos.pendencias_marketplaces"
    params = {
        "token": TINY_API_KEY,
        "formato": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "retorno" in data and "produtos" in data["retorno"]:
        produtos_pendentes = data["retorno"]["produtos"]
        return jsonify(produtos_pendentes), 200
    else:
        return jsonify({"message": "Nenhum produto com pendências encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
