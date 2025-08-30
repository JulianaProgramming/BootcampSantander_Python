import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Verificar se estamos em ambiente de teste
TESTING = os.getenv("TESTING", "False").lower() == "true"

if TESTING:
    # Usar mongomock para testes
    from mongomock import AsyncMongoClient
    client = AsyncMongoClient()
    DB_NAME = "test_fitstore_db"
else:
    # Usar MongoDB real para produção
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "fitstore_db")
    client = AsyncIOMotorClient(MONGODB_URL)

database = client[DB_NAME]

def get_database():
    return database