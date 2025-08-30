import pytest
import os
import asyncio
from fastapi.testclient import TestClient
from main import app

# Configurar ambiente de teste
os.environ["TESTING"] = "True"

@pytest.fixture(scope="session")
def event_loop():
    """Cria uma event loop para os testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def cliente():
    """Fixture para o cliente de teste"""
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
async def limpar_banco():
    """Limpa o banco de dados antes de cada teste"""
    from src.database.mongo_connection import get_database
    db = get_database()
    await db.produtos_fitness.delete_many({})
    yield
    await db.produtos_fitness.delete_many({})