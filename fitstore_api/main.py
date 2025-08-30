from fastapi import FastAPI
from src.routes.fitness_routes import router as produtos_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="FitStore API",
    description="API para gerenciamento de produtos de loja fitness",
    version="2.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(produtos_router)

@app.get("/")
async def pagina_inicial():
    return {"mensagem": "Bem-vindo à FitStore API - Sua loja fitness digital"}

@app.get("/saude")
async def verificar_saude():
    return {"status": "ativo", "mensagem": "API funcionando corretamente"}

@app.get("/sobre")
async def sobre():
    return {
        "api": "FitStore",
        "versao": "2.0.0",
        "descricao": "Sistema de gerenciamento de produtos fitness"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)