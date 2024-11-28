import requests
from config import TINY_API_KEY, BASE_URL  # type: ignore # Certifique-se de que estão definidos no config.py

def buscar_produtos(pagina=1):
    """
    Busca todos os produtos cadastrados no Tiny, página por página.
    """
    url = f"{BASE_URL}/produtos.pesquisa"
    params = {
        "token": TINY_API_KEY,
        "formato": "json",
        "pagina": pagina
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na comunicação com a API do Tiny: {e}")
        return {"error": "Erro na comunicação com o Tiny"}
    except ValueError:
        print(f"Erro ao processar a resposta do Tiny: {response.text}")
        return {"error": "Resposta inválida do Tiny"}

def buscar_detalhes_produto(sku):
    """
    Busca os detalhes de um produto específico no Tiny pelo SKU.
    """
    url = f"{BASE_URL}/produto.obter"
    params = {
        "token": TINY_API_KEY,
        "formato": "json",
        "pesquisa": sku
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na comunicação com a API do Tiny: {e}")
        return {"error": "Erro na comunicação com o Tiny"}
    except ValueError:
        print(f"Erro ao processar a resposta do Tiny: {response.text}")
        return {"error": "Resposta inválida do Tiny"}

def criar_atributo_personalizado(nome, tipo="texto", valores=None):
    """
    Cria um atributo personalizado no Tiny.
    """
    url = f"{BASE_URL}/atributos.incluir"
    data = {
        "token": TINY_API_KEY,
        "formato": "json",
        "atributo": {
            "nome": nome,
            "tipo": tipo,
            "valores": valores or []
        }
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na comunicação com a API do Tiny: {e}")
        return {"error": "Erro na comunicação com o Tiny"}
    except ValueError:
        print(f"Erro ao processar a resposta do Tiny: {response.text}")
        return {"error": "Resposta inválida do Tiny"}

def listar_produtos_pendentes_marketplaces():
    """
    Lista produtos com pendências nos marketplaces.
    """
    url = f"{BASE_URL}/produtos.pendencias_marketplaces"
    params = {
        "token": TINY_API_KEY,
        "formato": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na comunicação com a API do Tiny: {e}")
        return {"error": "Erro na comunicação com o Tiny"}
    except ValueError:
        print(f"Erro ao processar a resposta do Tiny: {response.text}")
        return {"error": "Resposta inválida do Tiny"}

def atualizar_produto(produto):
    """
    Atualiza os dados de um produto no Tiny.
    """
    url = f"{BASE_URL}/produto.alterar"
    data = {
        "token": TINY_API_KEY,
        "formato": "json",
        "produto": produto
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na comunicação com a API do Tiny: {e}")
        return {"error": "Erro na comunicação com o Tiny"}
    except ValueError:
        print(f"Erro ao processar a resposta do Tiny: {response.text}")
        return {"error": "Resposta inválida do Tiny"}