from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    descricao: str
    categoria: str
    estoque: int
    marca: str
    peso: Optional[float] = None
    tipo: str

class ProdutoCriar(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: str