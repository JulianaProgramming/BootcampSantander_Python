# Arquivo principal da aplicação FastAPI para a Workout API
# Responsável por registrar rotas, ciclo de vida e paginação
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, add_pagination, paginate
from contextlib import asynccontextmanager

from database.database import engine, Base
from routers import api, centro_treinamento, categoria

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas no banco de dados ao iniciar a aplicação
    Base.metadata.create_all(bind=engine)
    yield
    # Limpeza ao encerrar a aplicação

app = FastAPI(
    title="Workout API",
    description="API para gerenciamento de competição de crossfit",
    version="1.0.0",
    lifespan=lifespan
)

# Adiciona os routers
app.include_router(api.router)
app.include_router(centro_treinamento.router)
app.include_router(categoria.router)

# Adiciona paginação
add_pagination(app)

@app.get("/")
async def root():
    return {"message": "Workout API - Competição de Crossfit"}