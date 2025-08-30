from pydantic import BaseModel

class CentroTreinamentoCreate(BaseModel):
    nome: str
    endereco: str
    proprietario: str
    # Schemas Pydantic para centro de treinamento

class CentroTreinamentoResponse(CentroTreinamentoCreate):
    id: int
    class Config:
        orm_mode = True
