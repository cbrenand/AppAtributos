import os
import requests
from flask import Flask, request, jsonify, redirect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações do Tiny
TINY_CLIENT_ID = os.getenv("tiny-api-d4c818007ad48771afe75f79652f7c2bf3268447-1733157799")
TINY_CLIENT_SECRET = os.getenv("zECJh5uKoOilY0IMkaPy1qiMD3AWaUYq")
TINY_REDIRECT_URI = os.getenv("http://127.0.0.1:5000/callback")
TINY_API_TOKEN = os.getenv("e94b48205ec0e02e25eb855a32564acc08045cf4bda3f12da1d19a0329bc0f05")
TINY_AUTH_URL = "https://api.tiny.com.br/oauth/authorize"
TINY_TOKEN_URL = "https://api.tiny.com.br/oauth/token"

# Configurações do Mercado Livre
ML_CLIENT_ID = os.getenv("3970896740233001")
ML_CLIENT_SECRET = os.getenv("pXS7hT8dJ3B4ApIcT6p1BzhTBxKluQ9u")
ML_REDIRECT_URI = os.getenv("http://127.0.0.1:5000/ml/callback")
ML_AUTH_URL = "https://appatributos.onrender.com/auth"
ML_TOKEN_URL = "https://api.mercadolibre.com/oauth/token"

# Variável para armazenar tokens
tokens = {}

@app.route("/")
def home():
    return "Bem-vindo ao AppAtributos! Acesse /auth para autenticar no Tiny ou /ml/auth para autenticar no Mercado Livre."

# Fluxo de autenticação do Tiny
@app.route("/auth")
def auth_tiny():
    return redirect(f"{TINY_AUTH_URL}?response_type=code&client_id={TINY_CLIENT_ID}&redirect_uri={TINY_REDIRECT_URI}")

@app.route("/callback")
def callback_tiny():
    code = request.args.get("code")
    response = requests.post(TINY_TOKEN_URL, data={
        "grant_type": "authorization_code",
        "client_id": TINY_CLIENT_ID,
        "client_secret": TINY_CLIENT_SECRET,
        "code": code,
        "redirect_uri": TINY_REDIRECT_URI
    })
    tokens["tiny"] = response.json().get("access_token")
    return "Autenticação do Tiny concluída!"

# Fluxo de autenticação do Mercado Livre
@app.route("/ml/auth")
def auth_ml():
    return redirect(f"{ML_AUTH_URL}?response_type=code&client_id={ML_CLIENT_ID}&redirect_uri={ML_REDIRECT_URI}")

@app.route("/ml/callback")
def callback_ml():
    code = request.args.get("code")
    response = requests.post(ML_TOKEN_URL, data={
        "grant_type": "authorization_code",
        "client_id": ML_CLIENT_ID,
        "client_secret": ML_CLIENT_SECRET,
        "code": code,
        "redirect_uri": ML_REDIRECT_URI
    })
    tokens["ml"] = response.json().get("access_token")
    return "Autenticação do Mercado Livre concluída!"

# Exemplo de endpoint para buscar produtos do Tiny
@app.route("/produtos/<sku>", methods=["GET"])
def buscar_produto_tiny(sku):
    if "tiny" not in tokens:
        return "Erro: Não autenticado no Tiny. Por favor, autentique-se em /auth.", 401
    headers = {"Authorization": f"Bearer {tokens['tiny']}"}
    response = requests.get(f"https://api.tiny.com.br/produto/{sku}", headers=headers)
    return jsonify(response.json())

# Exemplo de endpoint para buscar anúncios do Mercado Livre
@app.route("/anuncios/<id>", methods=["GET"])
def buscar_anuncio_ml(id):
    if "ml" not in tokens:
        return "Erro: Não autenticado no Mercado Livre. Por favor, autentique-se em /ml/auth.", 401
    headers = {"Authorization": f"Bearer {tokens['ml']}"}
    response = requests.get(f"https://api.mercadolibre.com/items/{id}", headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
