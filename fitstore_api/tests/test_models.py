import pytest
from pydantic import ValidationError
from src.models.fitness_product import FitnessProduct

def test_criar_produto_valido():
    dados_produto = {
        "nome": "Creatina 300g",
        "preco": 79.90,
        "descricao": "Creatina monohidratada pura",
        "categoria": "creatina",
        "estoque": 30,
        "marca": "IntegralMedica",
        "peso": 300.0,
        "tipo": "suplemento"
    }
    
    produto = FitnessProduct(**dados_produto)
    assert produto.nome == "Creatina 300g"
    assert produto.preco == 79.90
    assert produto.tipo == "suplemento"

def test_criar_produto_sem_peso():
    dados_produto = {
        "nome": "Corda de Pular",
        "preco": 49.90,
        "descricao": "Corda para exercícios",
        "categoria": "cardio",
        "estoque": 15,
        "marca": "Nakamura",
        "tipo": "equipamento"
    }
    
    produto = FitnessProduct(**dados_produto)
    assert produto.peso is None

def test_criar_produto_nome_curto():
    dados_produto = {
        "nome": "AB",
        "preco": 29.90,
        "descricao": "Produto teste",
        "categoria": "teste",
        "estoque": 10,
        "marca": "Teste",
        "tipo": "suplemento"
    }
    
    with pytest.raises(ValidationError):
        FitnessProduct(**dados_produto)