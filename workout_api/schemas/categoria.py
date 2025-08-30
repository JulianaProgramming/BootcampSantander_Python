# Schemas Pydantic para validação e serialização de dados de categoria
from pydantic import BaseModel

class CategoriaCreate(BaseModel):
    nome: str

class CategoriaResponse(CategoriaCreate):
    id: int
    class Config:
        orm_mode = True
