import pytest
from fastapi import status

def test_criar_produto_fitness(cliente, limpar_banco):
    dados_produto = {
        "nome": "Whey Protein",
        "preco": 129.90,
        "descricao": "Proteína de alta qualidade",
        "categoria": "proteina",
        "estoque": 25,
        "marca": "Growth",
        "peso": 900.0,
        "tipo": "suplemento"
    }
    
    resposta = cliente.post("/produtos/", json=dados_produto)
    assert resposta.status_code == status.HTTP_201_CREATED
    assert resposta.json()["nome"] == "Whey Protein"
    assert "id" in resposta.json()

def test_listar_produtos(cliente, limpar_banco):
    dados_produto = {
        "nome": "BCAA",
        "preco": 89.90,
        "descricao": "Aminoácidos essenciais",
        "categoria": "aminoacidos",
        "estoque": 20,
        "marca": "Max Titanium",
        "peso": 300.0,
        "tipo": "suplemento"
    }
    cliente.post("/produtos/", json=dados_produto)
    
    resposta = cliente.get("/produtos/")
    assert resposta.status_code == status.HTTP_200_OK
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["nome"] == "BCAA"

def test_obter_produto_por_id(cliente, limpar_banco):
    dados_produto = {
        "nome": "Glutamina",
        "preco": 59.90,
        "descricao": "Suplemento de glutamina",
        "categoria": "recuperacao",
        "estoque": 18,
        "marca": "IntegralMedica",
        "peso": 250.0,
        "tipo": "suplemento"
    }
    resposta_criar = cliente.post("/produtos/", json=dados_produto)
    produto_id = resposta_criar.json()["id"]
    
    resposta = cliente.get(f"/produtos/{produto_id}")
    assert resposta.status_code == status.HTTP_200_OK
    assert resposta.json()["nome"] == "Glutamina"

def test_excluir_produto(cliente, limpar_banco):
    dados_produto = {
        "nome": "Shaker",
        "preco": 24.90,
        "descricao": "Shaker para suplementos",
        "categoria": "acessorios",
        "estoque": 30,
        "marca": "BlackSkull",
        "peso": 150.0,
        "tipo": "acessorio"
    }
    resposta_criar = cliente.post("/produtos/", json=dados_produto)
    produto_id = resposta_criar.json()["id"]
    
    resposta = cliente.delete(f"/produtos/{produto_id}")
    assert resposta.status_code == status.HTTP_204_NO_CONTENT
    
    resposta_busca = cliente.get(f"/produtos/{produto_id}")
    assert resposta_busca.status_code == status.HTTP_404_NOT_FOUND